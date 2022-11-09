drop database if exists listing;
create database listing;

# API Documentation is here:
# https://github.com/f22-6156-cc-team/f22_cc_api_doc/blob/main/listing_api_v1.yaml

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