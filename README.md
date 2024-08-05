# POI Semantics, Location and Road Networks

### Implementation in Python 3.7. Please check requirements.txt for package dependencies

## Dataset Collection Pipeline:

### Preparation
In settings.py, set the USER_AGENT variable to your identification/website.

### Reviews
1. Edit TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorSpider.py by changinge the start_urls, preUrl, and sufUrl variables.
2. Collect reviews using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorSpider.py
3. Clean review text and generate categories using LDA using LDAPreparePoI.py

### POI
1. Edit TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorAddress.py, changing the start_urls, city, preUrl, and sufUrl variables to match your desired page.
2. Collect attractions and addresses using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorAddress.py
3. Translate addresses into coordinates using geocode.py
4. Attach PoI to the Open Street Map road network using PoIOSMNetwork.py

### Combining them together
1. Use ParallelContractNetwork.py to add category information to PoI on the road network and contract the network.

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