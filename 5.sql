/* 2 columns: title, release year;
includes: Harry Potter movies
sort by: chronological order */
SELECT title, year FROM movies
WHERE title LIKE "Harry Potter%"
ORDER BY year;