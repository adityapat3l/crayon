# Crayon

Webscraper for Pinnbet and Maxbet odds.
DBT modelling

# Setup

1. Created `.env` file
2. Create the following entries:
    - AIRFLOW_UID
    - DATABASE_URL
3. Setup `~/.dbt/profiles.yml` folder with the correct credentials
4. Run `export DBT_PROFILES_DIR=~/.dbt`

# Run

```
docker-compose -f docker-compose.yml up --build -d
docker exec crayon_crayon_1 python -m project.api.fetch_maxbet
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


# AWS

To give access to readonly on root
```
chmod +x ~/.ssh/crayon-dev.pem
```

To copy folder over over
```
scp -i ~/.ssh/crayon-dev.pem -r ~/.ssh/id_rsa_ec2.pub ec2-user@ec2-3-85-101-145.compute-1.amazonaws.com:~/.ssh/
```


SSH into instance
```
ssh -i ~/.ssh/crayon-dev.pem ec2-user@ec2-3-85-101-145.compute-1.amazonaws.com:~/.ssh/
```


```
sudo systemctl start docker
sudo chmod 777 /var/run/docker.sock
```