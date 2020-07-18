/* single column: name(of person)
include: people who starred in movies released in 2004
order: birth year
*/

SELECT name
FROM people
WHERE id IN (SELECT person_id FROM stars
    WHERE movie_id IN (SELECT id FROM movies
        WHERE year = 2004))
ORDER BY birth;