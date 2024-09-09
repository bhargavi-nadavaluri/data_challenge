import os
import json
from scrapy.utils.project import get_project_settings

class NdBusinessesPipeline:
    def open_spider(self, spider):
        # Prepare to collect all items in a list
        self.items = []

    def close_spider(self, spider):
        settings = get_project_settings()
        output_path = settings.get('JSON_OUTPUT_PATH', 'data/nd_businesses.json')

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open the JSON file in write mode and save all items at once
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        # Add each item to the list
        self.items.append(dict(item))
        return item