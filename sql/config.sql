drop database if exists listing;
create database listing;

drop table if exists listing.listing;
CREATE TABLE listing.listing
(
    listing_id             INT          NOT NULL,
    is_active              BOOLEAN      NOT NULL,
    listing_name           VARCHAR(256) NOT NULL,
    listing_address        VARCHAR(256) NOT NULL,
    current_residents_num  INT          NOT NULL,
    total_residents_num    INT          NULL,
    author_user_id         INT          NOT NULL,
    # below are listing descriptions
    location_area          VARCHAR(256) NOT NULL,
    start_date             DATE         NOT NULL,
    end_date               DATE         NOT NULL,
    listing_total_size     INT          NOT NULL,
    listing_size           INT          NOT NULL,
    floor                  INT          NULL,
    has_elevator           BOOLEAN      NULL,
    is_pet_friendly        BOOLEAN      NULL,
    is_smoking_friendly    BOOLEAN      NULL,
    washer_dryer_location  VARCHAR(256) NULL,
    has_maintenance        BOOLEAN      NULL,
    has_gym                BOOLEAN      NULL,
    CONSTRAINT listing_pk
        PRIMARY KEY (listing_id)
);

CREATE UNIQUE INDEX listing_listing_id_uindex
    ON listing.listing (listing_id);

# CREATE TABLE listing.listing_description
# (
#     listing_description_id INT          NOT NULL,
#     listing_id             INT          NOT NULL,
#     location_area          VARCHAR(256) NOT NULL,
#     start_date             DATE         NOT NULL,
#     end_date               DATE         NOT NULL,
#     listing_total_size     INT          NOT NULL,
#     listing_size           INT          NOT NULL,
#     floor                  INT          NULL,
#     has_elevator           BOOLEAN      NULL,
#     is_pet_friendly        BOOLEAN      NULL,
#     is_smoking_friendly    BOOLEAN      NULL,
#     washer_dryer_location  VARCHAR(256) NULL,
#     has_maintenance        BOOLEAN      NULL,
#     has_gym                BOOLEAN      NULL,
#     CONSTRAINT listing_description_pk
#         PRIMARY KEY (listing_id)
# );
#
# CREATE UNIQUE INDEX listing_description_listing_id_uindex
#     ON listing.listing_description (listing_id);
#
#
#
# alter table listing.listing
#     add constraint listing_listing_description_null_null_fk
#         foreign key (listing_id, listing_description_id) references listing.listing_description (listing_id, listing_description_id);
