/* two columns: title, rating
include: all movies released in 2010
order: descending by rating; secondary: by title */
/*SELECT title FROM movies WHERE year = 2010
JOIN ratings
ON

rating FROM ratings WHERE movie_id = (id FROM movies WHERE year = 2010)
ORDER BY LOWER(title);
*/



SELECT title, rating
FROM movies
JOIN ratings
ON movies.id = ratings.movie_id
AND movies.year = 2010
ORDER BY ratings.rating DESC, LOWER(movies.title)