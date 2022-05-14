# GeoRepo

## :ballot_box_with_check: Project activity


[![Build and Test](https://github.com/unicef-drp/gis-geo-repository/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/unicef-drp/gis-geo-repository/actions/workflows/build-and-test.yaml)
[![codecov](https://codecov.io/gh/unicef-drp/gis-geo-repository/branch/develop/graph/badge.svg)](https://codecov.io/gh/unicef-drp/gis-geo-repository/)
[![Build and Test React Application](https://github.com/unicef-drp/gis-geo-repository/actions/workflows/frontend-test.yaml/badge.svg)](https://github.com/unicef-drp/gis-geo-repository/actions/workflows/frontend-test.yaml)

## :arrow_down: Quick Installation Guide

For deployment we use docker so you need to have docker running on the host.

```
git clone git@github.com:unicef-drp/gis-geo-repository.git
cd gis-geo-repository/deployment
cp .env.example .env
cp docker-compose.override.template.yml docker-compose.override.yml
cd ../
make build
make devweb
# Wait a few seconds for the DB to start before to do the next command
make migrate
make collectstatic
```

The website will be available at `http://localhost:61102`
