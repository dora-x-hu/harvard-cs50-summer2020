/* two columns: title, rating
include: all movies released in 2010
order: descending by rating; secondary: by title */
SELECT title FROM movies WHERE year = 2010 ORDER BY LOWER(title),
rating FROM ratings WHERE movie_id = (id FROM movies WHERE year = 2010);