# monisenforest-docker

Data summarization and visualization tool for permanent forest plot observations (tree census and litterfall survey) of the Monitoring Sites 1000.

## Features

- FastAPI with Python 3
- Vue.js with vuetify, router, vuex
- Postgres
- SqlAlchemy with Alembic for migrations
- Traefik for reverse proxy

## Getting Started

Docker and docker-compose are required.

Clone the repository:

```bash
git clone https://github.com/kohyamat/monisenforest-docker
cd monisenforest-docker
```

Build and run the app with docker-compose:

```bash
docker-compose up -d --build
```

Run the alembic migrations:

```bash
docker-compose run --rm backend alembic upgrade head
```

Enter http://localhost/ in a browser to see the application running.

## About Monitoring Sites 1000

The [Monitoring Sites 1000](http://www.biodic.go.jp/moni1000/), also called 'moni1000' or 'moni-sen', is a nationwide ecosystem monitoring project in Japan led by the Ministry of the Environment. The monitoring covers a wide range of ecosystems, including alpine areas, forests, grasslands, satoyama, lakes, marshes, coastal areas, coral reefs, and small islands. Since the launch of the project in 2003, a massive amount of observation data has been accumulated with the cooperation of researchers and citizens. Permanent forest plot observations have been conducted as part of the [Forests & Grasslands Survey](http://moni1000-forest.jwrc.or.jp/) of the project.

## Datasets of the Monitoring Sites 1000

The data collected by the Monitoring Sites 1000 project is publicly available and can be be found [here](http://www.biodic.go.jp/moni1000/findings/data/). Tree census data and litterfall monitoring data can be obtained from the following:

- [Tree census data](http://www.biodic.go.jp/moni1000/findings/data/index_file.html) from 61 forest plots (ca. 1 ha each) in 49 sites in Japan (Ishihara et al. 2011, Ecol. Res.).
- [Litterfall and seedfall monitoring data](http://www.biodic.go.jp/moni1000/findings/data/index_file_LitterSeed.html) from 21 forest plots in 20 sites in Japan (Suzuki et al. 2012, Ecol. Res.).

## Screenshot
![image](https://user-images.githubusercontent.com/6261781/139201606-6bd85137-c116-4ddc-9f2a-e86770a9f521.jpg)
