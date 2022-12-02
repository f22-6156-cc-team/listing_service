import json
from datetime import datetime

from flask import Flask, Response, request
from flask_cors import CORS
import re
from models.Listing import ListingQueryModel
import boto3
import os
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required)

camel_pat = re.compile(r'([A-Z])')
under_pat = re.compile(r'_([a-z])')

def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)
def underscore_to_camel(name):
    return under_pat.sub(lambda x: x.group(1).upper(), name)
def convert_json(d, convert):
    # takes a json and a convert function
    # returns the transformed json
    new_d = {}
    for k, v in d.items():
        new_d[convert(k)] = convert_json(v,convert) if isinstance(v,dict) else v
    return new_d

# Create the Flask application object.
application = app = Flask(__name__)
SNS_CLIENT = boto3.client('sns', region_name='us-east-1')
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(application)

def send_new_listing_notif(listing):
    # sends a notification to SNS on new listing created
    message = "New Listing {} just came up! Check it out! Only with ${}".format(listing.listing_id, listing.price)
    response = SNS_CLIENT.publish(
        TargetArn=os.environ.get("SNS_ARN"),
        Message=json.dumps({'default': message}),
        MessageStructure='json'
    )
    print(response)
    pass

@app.get("/api/health")
@app.get("/")
def get_health():
    t = str(datetime.now())
    msg = {
        "code": 0,
        "msg": "ok",
        "t": t
    }

    result = Response(json.dumps(msg), status=200,
                      content_type="application/json")

    return result


@app.route("/api/listings", methods=["GET"])
@jwt_required()
def get_all_listings():
    try:
        with ListingQueryModel() as lqm:
            listings = lqm.get_all_listing()
            listings = serialize(listings)
            # print(listings)
            listings = [convert_json(l, underscore_to_camel) for l in listings]
            rsp = Response(json.dumps(listings), status=200,
                           content_type="application/json")
            return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp

@app.route("/api/listings", methods=["POST"])
@jwt_required()
def create_listing():
    try:
        listing_info = convert_json(request.get_json(), camel_to_underscore)
        with ListingQueryModel() as lqm:
            listing = lqm.add_listing(listing_info)
            # FIXME: should not send in development
            # send SNS
            send_new_listing_notif(listing)
            rsp = Response(
                json.dumps(convert_json(serialize(listing),underscore_to_camel)), 
                status=200,
                content_type="application/json")
            return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


@app.route("/api/listing/<lid>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def listing_info_id(lid):
    def get_listing_by_id(lid):
        with ListingQueryModel() as lqm:
            return lqm.get_listing_by_id(lid)
    try:
        current_uid = get_jwt_identity()
        # listing = get_listing_by_id(lid)
        # if listing:
        #     listing_uid = listing.author_user_id
        #     current_uid = get_jwt_identity()
        #     if listing.author_user_id != current_uid:
        #         return Response("Inconsistent user", status=401,
        #                     content_type="text/plain")
        # else:
        #     return Response("listing not found", status=404,
        #                        content_type="text/plain")
        
        if request.method == "GET":
            listing = get_listing_by_id(lid)
            if listing:
                rsp = Response(
                    json.dumps(convert_json(serialize(listing),underscore_to_camel)), 
                    status=200,
                    content_type="application/json")
                return rsp
            else:
                rsp = Response("listing not found", status=404,
                               content_type="text/plain")
                return rsp

        elif request.method == "PUT":
            listing_info = convert_json(request.get_json(), camel_to_underscore)
            with ListingQueryModel() as lqm:
                lqm.update_listing_by_id(lid, listing_info)
                listing = get_listing_by_id(lid)
                if listing.author_user_id != current_uid:
                    return Response("Inconsistent user", status=401,
                                content_type="text/plain")
                rsp = Response(
                    json.dumps(convert_json(serialize(listing),underscore_to_camel)), 
                    status=200,
                    content_type="application/json")
                return rsp

        elif request.method == "DELETE":
            listing = get_listing_by_id(lid)
            if listing:
                if listing.author_user_id != current_uid:
                    return Response("Inconsistent user", status=401,
                                content_type="text/plain")
                with ListingQueryModel() as lqm:
                    lqm.delete_listing_by_id(lid)
                    rsp = Response("listing with lid {} is successfully deleted.".format(lid), status=200,
                               content_type="application/json")
                    return rsp
            else:
                rsp = Response("listing with lid {} not found".format(lid), status=404,
                               content_type="text/plain")
                return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp
    pass


def serialize(listings):
    # helper method to serialize listings
    ls = listings
    SINGLE = False
    if not isinstance(listings, list):
        ls = [listings]
        SINGLE = True
    res = []
    ts = '2023/11/22'
    f = '%Y/%m/%d'
    datetime.strptime(ts, f)
    for l in ls:
        r = {
            "listing_id": l.listing_id,
            "is_active": l.is_active,
            "listing_name": l.listing_name,
            "listing_address": l.listing_address,
            "current_residents_num": l.current_residents_num,
            "total_residents_num": l.total_residents_num,
            "author_user_id": l.author_user_id,
            "price": l.price,
            "location_area": l.location_area,
            "start_date": l.start_date.strftime(f),
            "end_date": l.end_date.strftime(f),
            "listing_total_size": l.listing_total_size,
            "listing_size": l.listing_size,
            "floor": l.floor,
            "has_elevator": l.has_elevator,
            "is_pet_friendly": l.is_pet_friendly,
            "is_smoking_friendly": l.is_smoking_friendly,
            "washer_dryer_location": l.washer_dryer_location,
            "has_maintenance": l.has_maintenance,
            "has_gym": l.has_gym

        }
        if SINGLE:
            return r
        res.append(r)
    return res


if __name__ == "__main__":
    app.run(host="localhost", port=7001, debug=True)
