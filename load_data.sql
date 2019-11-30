DROP TABLE IF EXISTS beer_master CASCADE;


-- Create gross big all data table
CREATE TABLE beer_master(
        brewery_id INTEGER, 
        brewery_name TEXT,
        review_overall NUMERIC(2,1), 
        review_aroma NUMERIC(2,1), 
        review_appearance NUMERIC(2,1), 
        review_profilename TEXT, 
        beer_style TEXT, 
        review_palate NUMERIC(2,1), 
        review_taste NUMERIC(2,1), 
        beer_name TEXT, 
        beer_abv NUMERIC(3,1), 
        beer_id INTEGER
);

-- Read data in from csv
SELECT "PLEASE MANUALLY ENTER IN THIS COMMAND: (database gets angry when I try to do it)" AS ""; 
SELECT "\COPY beer_master(brewery_id,brewery_name,review_overall,review_aroma,review_appearance,review_profilename,beer_style,review_palate,review_taste,beer_name,beer_abv,beer_id) FROM 'beer_reviews.csv' DELIMITER ',' CSV HEADER;" AS ''; 
