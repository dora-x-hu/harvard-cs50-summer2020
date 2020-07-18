/* single column, single row
includes: average rating of all movies released in 2012 */

SELECT AVG(rating)  /* gets average rating */
FROM ratings
JOIN movies         /* uses info from movies table */
ON ratings.movie_id = movies.id   /* this movie has a rating */
AND movies.year = 2012;           /* and was released in 2012 */