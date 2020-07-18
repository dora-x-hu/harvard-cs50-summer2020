/* single column: movie titles
include: movies starring Chadwick Boseman, top 5 ratings
order: descending
*/

SELECT title     /* movie titles are what we output */
FROM movies
JOIN stars       /* but we also need to know which people are stars */
ON movies.id = stars.movie_id  /* this movie is in the stars table */
JOIN people
ON stars.person_id = people.id /* and the person we're looking for is a star in said movie */
AND people.name = "Chadwick Boseman"
JOIN ratings                   /* we need to know ratings to rank them */
ON movies.id = ratings.movie_id
ORDER BY ratings.rating DESC
LIMIT 5;