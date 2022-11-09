import json
from datetime import datetime

from flask import Flask, Response, request
from flask_cors import CORS

from models.Listing import ListingQueryModel

# Create the Flask application object.
app = Flask(__name__)

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
    with ListingQueryModel as lqm:
        listings = lqm.get_all_listing()
        rsp = Response(json.dumps(listings), status=200,
                       content_type="application/json")
        return rsp


@app.route("/api/listing/<lid>", methods=["GET", "POST", "PUT", "DELETE"])
def listing_info_id(lid):
    def get_listing_by_id(lid):
        with ListingQueryModel as lqm:
            return lqm.get_listing_by_id(lid)

    try:
        if request.method == "GET":
            listing = get_listing_by_id(lid)
            if listing:
                rsp = Response(json.dumps(listing), status=200,
                               content_type="application/json")
                return rsp
            else:
                rsp = Response("listing not found", status=404,
                               content_type="text/plain")
                return rsp

        elif request.method == "POST" or request.method == "PUT":
            listing_info = request.get_json()
            if request.method == "POST":
                ListingQueryModel.add_user_contacts_by_user_id(lid, listing_info)
            else:
                ListingQueryModel.update_user_contacts_by_user_id(lid, listing_info)

            listing = get_listing_by_id(lid)

            rsp = Response(json.dumps(listing), status=200,
                           content_type="application/json")
            return rsp

        elif request.method == "DELETE":
            listing = get_listing_by_id(lid)
            if listing:
                ListingQueryModel.delete_listing_by_id(lid)
                rsp = Response("ok", status=200,
                               content_type="application/json")
                return rsp
            else:
                rsp = Response("user not found", status=404,
                               content_type="text/plain")
                return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)

