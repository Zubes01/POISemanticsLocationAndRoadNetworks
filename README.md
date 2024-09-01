# POI Semantics, Location and Road Networks

### Implementation in Python 3.7. Please check requirements.txt for package dependencies

## Dataset Collection Pipeline:

### Preparation
In settings.py, set the USER_AGENT variable to your identification/website. Install the packages as specified in requirements.txt

You may also need to install the requirements for spacy by using "python -m spacy download en_core_web_sm"

### Reviews
1. Edit TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorSpider.py by changinge the start_urls, preUrl, and sufUrl variables.
2. Collect reviews using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorSpider.py by navigating to TripAdvisorCrawler/tripAdvisorCrawler/spiders and executing "scrapy crawl tripAdvisor -o ../../attractionCityNameTripAdvisor.csv"
3. Change the city variable in LDAPreparePoI.py to the city name you chose in the last step.
3. Clean review text and generate categories using LDA by running LDAPreparePoI.py

### POI
1. Edit TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorAddress.py, changing the start_urls, city, preUrl, and sufUrl variables to match your desired page.
2. Collect attractions and addresses using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorAddress.py by navigating to TripAdvisorCrawler/tripAdvisorCrawler/spiders and executing "scrapy crawl tripAdvisorAddress -o ../../attractionMemphisAddress.csv"
3. Translate addresses into coordinates using geocode.py by navigating back to the root directory, changing the long_city and short_city variables in geocode.py, then executing geocode.py
4. Move the resulting file, something like "attractionCityLngLat.csv" to the PoINetwork folder.
4. Attach PoI to the Open Street Map road network using PoIOSMNetwork.py by changing the city_name, state_name, and short_name variables in the file and executing it

### Combining them together
1. Use ParallelContractNetwork.py to add category information to PoI on the road network and contract the network. This is done by changing the city_name and num_pois variables in ParallelContractNetwork.py and executing the file.

## Integrated Datasets:
### Attraction Addresses
- TripAdvisorCrawler/attractionChicagoAddress.csv
- TripAdvisorCrawler/attractionNYAddress.csv
### Attraction Reviews
- TripAdvisorCrawler/attractionChicagoTripAdvisor.csv
- TripAdvisorCrawler/attractionNYTripAdvisor.csv
### Attraction Coordinates
- PoI_Network/attractionChicagoLngLat.csv
- PoI_Network/attractionNYLngLat.csv
### Attraction LDA Category Outputs
- LDA_Model_6/ChicagoDivVector.csv
- LDA_Model_6/NYDivVector.csv