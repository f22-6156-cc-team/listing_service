# Listing MicroService

## How to build and run locally
1. set up DB configs in `.env`
1. execute script `sql/config.sql` to initialize the database
2. run `export FLASK_APP=application`
3. run `flask run`

The application should be running on `localhost:5000`.

## How to deploy
Listing microservice is deployed on AWS elasticBeanstalk, and its database is using RDS.

## Some important debugging tips about deploying
1. when deploying, make sure the unzipping the file has `application.py` in it directly. If you are using `PyCharm` this might not be the case because of the `/src` directory.
2. Make sure the naming is strictly `application.py` and inside the app, use `application = app = Flask(..)`, and this is following rules of EBS.
3. Remember to configure ENV variables on EBS too.


