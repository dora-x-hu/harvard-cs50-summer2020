/* single column: names(of people who are stars)
includes: people who starred in movies that Kevin Bacon(1958) also starred in
*exclude Kevin Bacon himself


SELECT name
FROM people
JOIN stars as st1
    JOIN stars as st2
    ON st1.movie_id = st2.movie_id
    AND st2.person_id = (id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)
    AND st1.person_id != (id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)
ON people.id = st1.person_id;
*/

SELECT name FROM people
WHERE id = (SELECT person_id FROM stars
    WHERE movie_id = (SELECT movie_id FROM stars
        WHERE person_id = (SELECT id FROM people
            WHERE name = "Kevin Bacon" AND birth = 1958)))
AND (name != "Kevin Bacon" OR birth != 1958);