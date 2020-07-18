/* single column: name
incldue: stars in "Toy Story" */

SELECT name
FROM people
JOIN stars
ON people.id = stars.person_id    /* this id should be in people and stars */
AND stars.movie_id = (SELECT id FROM movies WHERE title = "Toy Story");  /* the id of the movie they star in should match that of Toy Story */