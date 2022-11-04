import json
from datetime import datetime

from flask import Flask, Response, request
from flask_cors import CORS

from models.Listing import ListingQueryModel

# Create the Flask application object.
application = app = Flask(__name__)

CORS(app)


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
def get_all_listings():
    try:
        with ListingQueryModel() as lqm:
            listings = lqm.get_all_listing()
            listings = serialize(listings)
            rsp = Response(json.dumps(listings), status=200,
                           content_type="application/json")
            return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


@app.route("/api/listing/<lid>", methods=["GET", "POST", "PUT", "DELETE"])
def listing_info_id(lid):
    def get_listing_by_id(lid):
        with ListingQueryModel() as lqm:
            return lqm.get_listing_by_id(lid)

    try:
        if request.method == "GET":
            listing = get_listing_by_id(lid)
            if listing:
                rsp = Response(json.dumps(serialize(listing)), status=200,
                               content_type="application/json")
                return rsp
            else:
                rsp = Response("listing not found", status=404,
                               content_type="text/plain")
                return rsp

        elif request.method == "POST" or request.method == "PUT":
            listing_info = request.get_json()
            with ListingQueryModel() as lqm:
                if request.method == "POST":
                    lqm.add_listing_by_id(lid=lid, listing_info=listing_info)
                else:
                    lqm.update_listing_by_id(lid=lid, listing_info=listing_info)

                listing = get_listing_by_id(lid)
                rsp = Response(json.dumps(serialize(listing)), status=200,
                               content_type="application/json")
                return rsp

        elif request.method == "DELETE":
            listing = get_listing_by_id(lid)
            if listing:
                ListingQueryModel().delete_listing_by_id(lid)
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
        res.append({
            "listingId": l.listing_id,
            "isActive": l.is_active,
            "listingName": l.listing_name,
            "listingAddress": l.listing_address,
            "currentResidentsNum": l.current_residents_num,
            "totalResidentsNum": l.total_residents_num,
            "authorUserId": l.author_user_id,
            "price": l.price,
            "locationArea": l.location_area,
            "startDate": l.start_date.strftime(f),
            "endDate": l.end_date.strftime(f),
            "listingTotalSize": l.listing_total_size,
            "listingSize": l.listing_size,
            "floor": l.floor,
            "hasElevator": l.has_elevator,
            "isPetFriendly": l.is_pet_friendly,
            "isSmokingFriendly": l.is_smoking_friendly,
            "washerDryerLocation": l.washer_dryer_location,
            "hasMaintenance": l.has_maintenance,
            "hasGym": l.has_gym

        })
    return res


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
