/* single column: titles ofmovies with release year on or after 2018; alphabetical order*/
SELECT title FROM movies WHERE year >= 2018
ORDER BY LOWER(title);