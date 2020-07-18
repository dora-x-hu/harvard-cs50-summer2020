/* single column, single row
includes: average rating of all movies released in 2012 */
/*SELECT (SUM(rating*votes)/SUM(votes)) FROM ratings
WHERE movie_id = (SELECT id FROM movies WHERE year = 2012);
*/

SELECT AVG(rating)
FROM ratings
JOIN movies
ON ratings.movie_id = movies.id
AND movies.year = 2012;