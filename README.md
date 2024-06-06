# POI Semantics, Location and Road Networks

### Implementation in Python 3.7. Please check requirements.txt for package dependencies

## Dataset Collection Pipeline:

### POI
1. Collect attractions and addresses using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorAddress.py
2. Translate addresses into coordinates using geocode.py
3. Attach PoI to the Open Street Map road network using PoIOSMNetwork.py

### Reviews
1. Collect reviews using TripAdvisorCrawler/TripAdvisorCrawler/spiders/tripAdvisorSpider.py
2. Clean review text and generate categories using LDA using LDAPreparePoI.py

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