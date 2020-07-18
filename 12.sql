/* single column: title of movie
include: movies that have Johnny Depp and Helena Bonham Carter listed as stars
*/

SELECT title
FROM movies
JOIN stars
ON movies.id = stars.movie_id;
JOIN people
ON stars.person_id = (id FROM people where)