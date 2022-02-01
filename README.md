![Logo](refbee-logo.png?raw=true "Logo")

# Which Publications' Metadata Are in Which Bibliographic Databases? A System for Exploration

We present **RefBee**, an online system that retrieves the metadata of all publications for a given author from the various bibliographic databases and indicates which publications are missing in which database. Our system supports the following data sources:
* Wikidata, 
* ORCID, 
* Google Scholar, 
* VIAF, 
* DBLP, 
* Dimensions, 
* Microsoft Academic, 
* Semantic Scholar, and 
* DNB/GNB. 

It is available online at **http://km.aifb.kit.edu/services/refbee/**. 

Our system not only can serve as assistance tool for more than 4.7 million researchers of any discipline and publication's language, but also incentivizes the usage and population of Wikidata in the scholarly field. 

## How to Use: Build and run using Docker
```
docker build -t refbee-s:latest .
docker run -d -p 5000:5000 refbee-s:latest
```
