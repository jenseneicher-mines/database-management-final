DROP TABLE IF EXISTS breweries CASCADE;
DROP TABLE IF EXISTS beers CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;


SELECT 'Make sure you ran load_data.sql before running this script' AS '';

-- Create tables
CREATE TABLE breweries(
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE beers(
	id INTEGER PRIMARY KEY,
	brewery_id INTEGER REFERENCES breweries(id),
	name TEXT,
	style TEXT,
	abv NUMERIC(3,1)
);

CREATE TABLE reviews(
	reviewer_name TEXT,
	beer_id INTEGER REFERENCES beers(id),
	overall NUMERIC(2,1),
	aroma NUMERIC(2,1),
	palate NUMERIC(2,1),
	taste NUMERIC(2,1),
	appearance NUMERIC(2,1)
	--,PRIMARY KEY(reviewer_name, beer_id)
);

-- Move data into tables
INSERT INTO breweries(id, name) 
	SELECT DISTINCT brewery_id, brewery_name FROM beer_master;
INSERT INTO beers(id, brewery_id, name, style, abv)
	SELECT DISTINCT beer_id, brewery_id, beer_name, beer_style, beer_abv FROM beer_master;
INSERT INTO reviews(beer_id, overall, aroma, appearance, reviewer_name, palate, taste) 
	SELECT DISTINCT bm1.beer_id, bm1.review_overall, bm1.review_aroma, bm1.review_appearance, 
	bm1.review_profilename, bm1.review_palate, bm1.review_taste FROM beer_master AS bm1 
		--WHERE (bm1.review_overall, bm1.review_aroma) 
		--= (SELECT bm2.review_overall, bm2.review_aroma 
		--	FROM beer_master AS bm2 
		--	WHERE bm1.beer_id = bm2.beer_id 
		--	AND bm1.review_profilename = bm2.review_profilename 
		--	ORDER BY bm2.beer_id ASC LIMIT 1);
