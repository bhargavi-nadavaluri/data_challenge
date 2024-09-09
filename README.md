## Code Functionality Overview

This project scrapes business data from a North Dakota government API, processes the data, and visualizes relationships between businesses, registered agents, and owners using network graphs. The project consists of five main components:

### 1. Finding API's from the Webapp 
First tried searching the name as `X` by using `starts with` and `actice entities only` in advanced options then extracted the endpoint in the network section using web dev tools (`businesses_api.png`)

Business Endpoint : https://firststop.sos.nd.gov/api/Records/businesssearch

Second step is to get the details endpoint by selecting one of the company and then extracted the API in network section using web dev tools `businesses_details_api.png`)

Business Details Endpoint: https://firststop.sos.nd.gov/api/FilingDetail/business/{business_id}/false


### 2. Item Definition (`items.py`)
The `NdBusinessesItem` class defines the structure of the items to be scraped. Each item represents a business with the following fields:

- **business_id**: Unique identifier for the business.
- **business_name**: Name of the business.
- **filing_type**: Type of business filing.
- **owner_name**: Name of the business owner.
- **commercial_registered_agent**: Commercial registered agent associated with the business.
- **registered_agent**: Registered agent associated with the business.

Additionally, the `__setitem__` method allows dynamic creation of fields that may not be predefined.

### 3. Data Pipeline (`pipelines.py`)
The `NdBusinessesPipeline` class processes the scraped items by collecting them into a list and saving them to a JSON file when the spider finishes.

- **open_spider**: Initializes an empty list to store items when the spider opens.
- **close_spider**: Writes the collected items to a JSON file located at `data/nd_businesses.json`.
- **process_item**: Adds each item to the list of scraped data during the spider's execution.

### 4. Scrapy Spider (`spiders/nd_business_spider.py`)
The `NdBusinessSpider` class defines the scraping logic for extracting business data from the North Dakota API.

- **start_requests**: Sends a POST request to search for businesses whose names start with the letter "X". The search is restricted to active businesses.
- **parse**: Parses the initial response, extracting business IDs and sending new requests to fetch detailed business information.
- **parse_business_detail**: Extracts detailed information about each business, including agents and owners, and saves it into an `NdBusinessesItem`.

### 5. Graph Visualization (`graph_builder.py`)
The `build_graph_from_json` function generates a network graph based on the scraped business data. It visualizes relationships between businesses, their registered agents, and their owners.

- **Graph Construction**: Builds a graph using the business names as nodes. It adds edges between businesses and agents or owners if such relationships are present.
- **Graph Visualization**: The graph is plotted using `matplotlib` and `networkx`, with different colors representing different node types (company[skyblue], agent[orange], owner[lightgreen]). The graph is saved as `nd_businesses.png`.
