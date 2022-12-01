# from models.BaseModel import Base, BaseQueryModel
from .BaseModel import BaseQueryModel, Base
from sqlalchemy import Column, Integer

class Listing(Base):
    __tablename__ = 'listing'
    __table_args__ = {'autoload': True}


class ListingQueryModel(BaseQueryModel):

    def get_all_listing(self):
        return self.session.query(Listing).filter(Listing.is_active == True).all()

    def get_listing_by_id(self, lid):
        l = self.session.query(Listing).filter(
            Listing.listing_id == lid).filter(Listing.is_active == True).first()
        return l

    def get_last_listing_id(self):
        l = self.session.query(Listing).order_by(Listing.listing_id.desc()).first()
        return l.listing_id

    def add_listing(self, listing_info=None):
        # print("lid : {}".format(lid))
        # print("lid : %d" % lid)

        # FIXME: why update an existed listing in creating method
        # inactive_listing = self.session.query(Listing).filter(
        #     Listing.listing_id == lid).filter(Listing.is_active == False).first()
        # if inactive_listing:
        #     inactive_listing.is_active = True
        #     if listing_info:
        #         for key, value in listing_info.items():
        #             setattr(inactive_listing, key, value)
        #     self.session.commit()
        # else:

        # FIXME: not a secure way to get latest listing id
        listing_id = self.get_last_listing_id() + 1
        l = Listing(
            listing_id=listing_id,
            is_active=True
        )
        
        if listing_info:
            for key, value in listing_info.items():
                setattr(l, key, value)
        self.session.add(l)
        self.session.commit()
        return l


    def update_listing_by_id(self, lid, listing_info=None):
        listing = self.session.query(Listing).filter(
            Listing.listing_id == lid).filter(Listing.is_active == True).first()
        if listing_info:
            for key, value in listing_info.items():
                setattr(listing, key, value)
        self.session.commit()

    def delete_listing_by_id(self, lid):
        l = self.session.query(Listing).filter(
            Listing.listing_id == lid).filter(Listing.is_active == True).first()
        l.is_active = False
        self.session.commit()
