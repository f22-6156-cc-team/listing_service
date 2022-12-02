DROP DATABASE IF EXISTS listing;
CREATE DATABASE listing;

# API Documentation is here:
# https://github.com/f22-6156-cc-team/f22_cc_api_doc/blob/main/listing_api_v1.yaml

DROP TABLE IF EXISTS listing.listing;
CREATE TABLE listing.listing
(
    listing_id            INT          NOT NULL AUTO_INCREMENT,
    is_active             BOOLEAN      NOT NULL,
    listing_name          VARCHAR(256) NOT NULL,
    listing_address       VARCHAR(256) NOT NULL,
    current_residents_num INT          NULL,
    total_residents_num   INT          NULL,
    author_user_id        VARCHAR(256) NOT NULL,
    price                 INT          NULL,
    # below are listing descriptions
    location_area         VARCHAR(256) NOT NULL,
    start_date            DATE         NOT NULL,
    end_date              DATE         NOT NULL,
    listing_total_size    INT          NULL,
    listing_size          INT          NULL,
    floor                 INT          NULL,
    has_elevator          BOOLEAN      NULL,
    is_pet_friendly       BOOLEAN      NULL,
    is_smoking_friendly   BOOLEAN      NULL,
    washer_dryer_location VARCHAR(256) NULL,
    has_maintenance       BOOLEAN      NULL,
    has_gym               BOOLEAN      NULL,
    CONSTRAINT listing_pk
        PRIMARY KEY (listing_id)
);

INSERT INTO listing.listing (listing_id, is_active, listing_name, listing_address, current_residents_num,
                             total_residents_num, author_user_id, price, location_area, start_date, end_date,
                             listing_total_size, listing_size, floor, has_elevator, is_pet_friendly,
                             is_smoking_friendly, washer_dryer_location, has_maintenance, has_gym)
VALUES (1, TRUE, 'listing A', 'test address A', 2, 4, 9223372036854775807, 1000, '10027', '2022/11/11', '2023/11/11',
        3000, 1000, 2, TRUE,
        TRUE, TRUE, '2nd floor', TRUE, TRUE),
       (2, TRUE, 'listing B', 'test address B', 3, 7, 9223372036854775807, 3000, '10025', '2022/10/10', '2023/10/10',
        500, 400, 9, TRUE,
        FALSE, TRUE, 'NA', TRUE, TRUE),
       (3, TRUE, 'listing B', 'test address C', 3, 7, 9223372036854775807, 3000, '10025', '2022/10/10', '2023/10/10',
        500, 400, 9, TRUE,
        FALSE, TRUE, 'NA', TRUE, TRUE),
       (4, TRUE, 'listing B', 'test address D', 3, 7, 2, 3000, '10025', '2022/10/10', '2023/10/10', 500, 400, 9, TRUE,
        FALSE, TRUE, 'NA', TRUE, TRUE),
       (5, TRUE, 'listing B', 'test address B', 3, 7, 2, 3000, '10025', '2022/10/10', '2023/10/10', 500, 400, 9, TRUE,
        FALSE, TRUE, 'NA', TRUE, TRUE);

CREATE UNIQUE INDEX listing_listing_id_uindex
    ON listing.listing (listing_id);