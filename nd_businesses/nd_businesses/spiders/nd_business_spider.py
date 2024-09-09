import scrapy
import json
from nd_businesses.items import NdBusinessesItem

class NdBusinessSpider(scrapy.Spider):
    name = 'nd_business_spider'
    allowed_domains = ['firststop.sos.nd.gov']
    start_urls = ['https://firststop.sos.nd.gov/api/Records/businesssearch']

    def start_requests(self):
        url = 'https://firststop.sos.nd.gov/api/Records/businesssearch'
        search_data = {"SEARCH_VALUE": "X", "STARTS_WITH_YN": "true", "ACTIVE_ONLY_YN": "true"}
        
        # Make the initial POST request
        yield scrapy.Request(
            url=url, 
            method="POST", 
            headers={'Content-Type': 'application/json'}, 
            body=json.dumps(search_data),
            callback=self.parse
        )

    def parse(self, response):
        try:
            businesses = json.loads(response.body)
            rows = businesses.get('rows', {})
        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response")
            return
        
        for business_id, business in rows.items():
            detail_url = f'https://firststop.sos.nd.gov/api/FilingDetail/business/{business_id}/false'
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_business_detail,
                meta={'business_id': business_id,'business_name': business.get('TITLE', 'Unknown')[0]},
                method='GET',
                headers={'accept':'*/*','authorization':'undefined'}
            )

    def parse_business_detail(self, response):
        business_id = response.meta['business_id']
        business_name = response.meta['business_name']

        try:
            business_details = json.loads(response.body)
            drawer_details = business_details.get("DRAWER_DETAIL_LIST", [])
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON response for business ID: {business_id}")
            return
        
        item = NdBusinessesItem()
        item['business_id'] = business_id
        item['business_name'] = business_name
        
        for detail in drawer_details:
            label = detail.get('LABEL', '').replace(' - ','_').replace(' ', '_').lower()
            value = detail.get('VALUE', '')
            item[label] = value
        
        yield item