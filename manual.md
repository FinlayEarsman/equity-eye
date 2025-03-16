## Build steps

For this project I was working in two different environments, locally and on the SoCS IDA cluster. To deploy them has different workflows.

## Local deployment
First, begin by cloning the repo:
```
$ git clone https://stgit.dcs.gla.ac.uk/2450322e/level-4-project.git
```

Then, inside of `src/equity-eye` there is a `docker-compose.yml` file that will build and deploy the containers. 

To do this you first run 
```
$ docker-compose build
``` 
from the `src/equity-eye` directory, once this completes you then run 
```
$ docker-compose up
``` 
which deploys the containers.

To deploy the frontend navigate to `./client/frontend` and run:
```
$ npm install & npm run serve
```

The Django REST API can be accessed via `http://localhost:8000` and the Vue.js frontend client via `http://localhost:8080`.

### Database populating
To populate the database with the S&P 500 securities, inside of the `agg_collector` container, a script called `create_assets.py` can be ran, which will do this.

To scrape news articles, inside the `article_collector` container, a script called `main_scraper.py` can be ran which will query [Google's newsapi](https://newsapi.org/docs/endpoints/everything) and then scrape the articles returned by this and insert them to the Django database. An API key will be needed for it to work.

## Cluster deployment
To deploy on the IDA cluster, you simply need to copy the various Kubernetes config files in `src/miscellaneous/cluster` onto the cluster using the web interface. Kubernetes will from there handle the deployment and running of the containers.

After declaring the route to the `client` service, you can access the Vue.js frontend from your browser.

### Database populating
In a similar manner to above, the database needs to be populated.

To create the assets, you could alter the agg_collector cronjob slightly to run the `create_assets.py` script instead of `fetch_new_aggregates.py`. The period at which it runs at will also need to be temporarily shortened. After this it can be returned to its previous state.

The article_collector cronjob will be setup to run weekly, this can be changed as desired.