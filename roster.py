import sys
import cs50

# check for correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: python roster.py house")
    exit(1)

db = cs50.SQL("sqlite:///students.db")

thisHouse = str(sys.argv[1])

if thisHouse == "Gryffindor":
    # puts the students from the given house into a list of dicts
    thisList = db.execute("SELECT * FROM students WHERE house = 'Gryffindor' ORDER BY last, first")
elif thisHouse == 'Ravenclaw':
    thisList = db.execute("SELECT * FROM students WHERE house = 'Ravenclaw' ORDER BY last, first")
elif thisHouse == 'Hufflepuff':
    thisList = db.execute("SELECT * FROM students WHERE house = 'Hufflepuff' ORDER BY last, first")
else:
    thisList = db.execute("SELECT * FROM students WHERE house = 'Slytherin' ORDER BY last, first")



for row in thisList:
    if(row["middle"] == None):
        print(f"{row['first']} {row['last']}, born {row['birth']}")
        continue
    print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")

# SQL query
# SELECT first, middle, last
# FROM students
# WHERE house = sys.argv[1]
# ORDER BY last, first