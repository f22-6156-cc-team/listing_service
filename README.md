# Listing MicroService

## Mysql
```bash
docker pull mysql:latest
docker images
docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
docker ps
```

Connect
```bash
mysql -u root -p -h 127.0.0.1
```

Init
```bash
source ./sql/config.sql
```

Check
```bash
SHOW DATABASES;
use listing;
SHOW TABLES;
SELECT * FROM listing;
```

## How to build and run locally
1. install deps `python3 -m pip install -r requirements.txt`
2. execute script `sql/config.sql` to initialize the database
3. run `flask run`

The application should be running on `localhost:5000`.

## How to deploy
Listing microservice is deployed on AWS elasticBeanstalk, and its database is using RDS.

## Some important debugging tips about deploying
1. when deploying, make sure the unzipping the file has `application.py` in it directly. If you are using `PyCharm` this might not be the case because of the `/src` directory.
2. Make sure the naming is strictly `application.py` and inside the app, use `application = app = Flask(..)`, and this is following rules of EBS.
3. Remember to configure ENV variables on EBS too.


