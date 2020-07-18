/* single column: name(of person)
include: people who starred in movies released in 2004
order: birth year
*/

SELECT name
FROM people
JOIN stars     /* info from the stars table */
ON people.id = stars.person_id    /* this person appears in the stars table */
AND stars.movie_id = (id FROM movies WHERE year = 2004)   /* the movie they star in came out in 2004 */
ORDER BY people.birth;    /* order by the person's birth date */