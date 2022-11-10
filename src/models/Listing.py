# from models.BaseModel import Base, BaseQueryModel
from src.models.BaseModel import BaseQueryModel, Base


class Listing(Base):
    __tablename__ = 'listing'
    __table_args__ = {'autoload': True}


class ListingQueryModel(BaseQueryModel):

    def get_all_listing(self):
        return self.session.query(Listing).all()

    def get_listing_by_id(self, lid):
        l = self.session.query(Listing).filter(
            Listing.listing_id == lid).filter(Listing.is_active == True).first()
        return l

    def add_listing_by_id(self, lid, listing_info=None):
        print("lid : {}".format(lid))
        # print("lid : %d" % lid)
        inactive_listing = self.session.query(Listing).filter(
            Listing.listing_id == lid).filter(Listing.is_active == False).first()
        if inactive_listing:
            inactive_listing.is_active = True
            if listing_info:
                for key, value in listing_info.items():
                    setattr(inactive_listing, key, value)
            self.session.commit()
        else:
            l = Listing(
                listing_id=lid,
                is_active=True
            )
            print("no inactive listing!")
            if listing_info:
                for key, value in listing_info.items():
                    setattr(l, key, value)
            self.session.add(l)
            self.session.commit()

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
