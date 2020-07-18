/* two columns: title, rating
include: all movies released in 2010
order: descending by rating; secondary: by title */

SELECT title, rating    /* output title and rating */
FROM movies             /* we need info from movies and ratings */
JOIN ratings
ON movies.id = ratings.movie_id  /* their commonality is the id of the movie */
AND movies.year = 2010           /* which was released in 2010 */
ORDER BY ratings.rating DESC, LOWER(movies.title)  /* descending order by rating, additionally by title */