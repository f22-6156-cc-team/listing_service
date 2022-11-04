# from UserContacts import UserContactsQueryModel
# from Email import EmailQueryModel
# from Phone import PhoneQueryModel
# from Address import AddressQueryModel
#
from Listing import ListingQueryModel

if __name__ == '__main__':
    uid = '18'
    lid = '19'
    lqm = ListingQueryModel()
    lqm.add_listing_by_id(lid, {
        "is_active": True,
        "listing_name": "test",
        "listing_address": "123 test St",
        "current_residents_num": 2,
        "total_residents_num": 4,
        "author_user_id": uid,
        "location_area": "NY",
        "start_date": "11/10/22",
        "end_date": "1/10/23",
        "listing_total_size": 1000,
        "listing_size": 200
    })
    print(lqm.get_listing_by_id(lid))
    print(lqm.update_listing_by_id(lid, {
        "listing_name" : "another one"
    }))
    print(lqm.delete_listing_by_id(lid))
