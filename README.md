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


# Airflow

```
# initialize the database tables
airflow db init

# print the list of active DAGs
airflow dags list

# prints the list of tasks in the "tutorial" DAG
airflow tasks list tutorial

# prints the hierarchy of tasks in the "tutorial" DAG
airflow tasks list tutorial --tree
```


## Jupyter

```shell
docker exec -it crayon-crayon-1 /bin/bash
jupyter notebook --ip 0.0.0.0 --allow-root
```