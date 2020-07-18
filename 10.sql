/* single column: name(of person)
include: directors of movies with rating >= 9.0
*/

SELECT name
FROM people      /* names from people table */
JOIN directors   /* with info from directors table */
ON people.id = directors.person_id    /* people who are directors */
JOIN ratings     /* info from ratings table */
ON directors.movie_id = ratings.movie_id     /* this director's movie has a rating */
AND ratings.rating >= 9.0;                   /* and that rating is at least 9.0 */