/* single column, single row
includes: average rating of all movies released in 2012 */
SELECT (SUM(rating)/COUNT(rating)) FROM ratings
WHERE movie_id = (SELECT id FROM movies WHERE year = 2012);