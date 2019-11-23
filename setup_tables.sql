DROP TABLE IF EXISTS brewery CASCADE;
DROP TABLE IF EXISTS beer CASCADE;
DROP TABLE IF EXISTS review CASCADE;


SELECT 'Make sure you ran load_data.sql before running this script' AS '';

-- Create tables
CREATE TABLE brewery(
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE beer(
	id INTEGER PRIMARY KEY,
	brewery_id INTEGER REFERENCES brewery(id),
	name TEXT,
	style TEXT,
	abv NUMERIC(3,1)
);

CREATE TABLE review(
	reviewer_name TEXT,
	beer_id INTEGER REFERENCES beer(id),
	overall NUMERIC(2,1),
	aroma NUMERIC(2,1),
	palate NUMERIC(2,1),
	taste NUMERIC(2,1),
	appearance NUMERIC(2,1)
);

-- Move data into tables

INSERT INTO Review (beer_id, rating, aroma, appearance, reviewer_name, palate, taste) SELECT (review_overall, review_aroma, review_appearance, review_profilename, review_palate, review_taste) FROM beer_master;
INSERT INTO Beer(id, brewery_id, style, name) SELECT (beer_beerid, beer_style, beer_name) FROM beer_master;
INSERT INTO Brewery(id, name) SELECT (brewery_id, brewery_name) FROM beer_master;
