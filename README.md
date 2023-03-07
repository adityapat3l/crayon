# Crayon

Webscraper for Pinnbet and Maxbet odds.
DBT modelling


# Run

```
docker-compose -f docker-compose.yml up --build -d
docker exec crayon_crayon_1 python -m project.models.maxbet
```

or hit endpoint

```
localhost:5000/run_scrapes?website_name=maxbet
```