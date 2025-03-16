# Equity-Eye

This system was developed to allow financial traders access to historical news articles to identify the causes of price changes over an assets history.

The system also allows traders to review how the market sentiment of an asset shifts over time through the use of news.

## Directory structure
Inside of `equity-eye/`:
* docker-compose.yml - for deploying the system locally through docker-compose
* `.env` files
* `app/` directory - contains files relating to Django application
* `client/` directory - contains files relating to frontend client
* `nginx/` directory - contains files for nginx
* `scraper/` directory - contains the files for the two scrapers I make use of
* `miscellaneous/cluster` directory - contains Kubernetes config files used to deploy remotely
* `miscellaneous/extra_script` directory - contains extra scripts that were used during development.

## Requirements (for running locally)

* Python 3.7+
* Docker
* NPM
* Git (if cloning)
* Tested on linux

## Accessing the system

Currently the system is deployed on the University of Glasgow's network at: [equity-eye.ida.dcs.gla.ac.uk](http://equity-eye.ida.dcs.gla.ac.uk/)

Note: you must too be on the network to access it.


More deployment instructions can be found in `manual.md`.

