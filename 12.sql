/* single column: title of movie
include: movies that have Johnny Depp and Helena Bonham Carter listed as stars
*/

SELECT title
FROM movies
WHERE id IN
    (SELECT movie_id FROM stars
    WHERE person_id IN
        (SELECT id FROM people
        WHERE name = "Johnny Depp"))
AND id IN
    (SELECT movie_id FROM stars
    WHERE person_id IN
        (SELECT id FROM people
        WHERE name = "Helena Bonham Carter"));