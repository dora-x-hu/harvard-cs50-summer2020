import sys
import csv
import cs50

# checks for correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

#
open(f"students.db", "w").close()
db = cs50.SQL(f"sqlite:///students.db")

db.execute("CREATE table students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# opens input csv file for reading:
with open(sys.argv[1], "r") as csv_file:
    reader = csv.DictReader(csv_file, delimiter = ",")

    # go through every row in the reader
    for row in reader:

        ## keep track of the number of spaces to determien whether they have a middle name
        #numSpace = 0
        #index = 0
        #names = []
        #start = 0

        # go through the string that is a character's full name
        #for char in row["name"]:
        #    if char == " ":
        #        numSpace += 1
        #        names.append(row["name"][start:index])
        #        start = index + 1
        #    index += 1
        #names.append(row["name"][start:index])

        #firstName = names[0]

        #if numSpace == 1:
        #    lastName = names[1]
        #    middleName = 'NULL'
        #else:
        #    lastName = names[2]
        #    middleName = names[1]

        names = row["name"].split(" ")
        firstName = names[0]
        if(len(names)==2):
            middleName = None
            lastName = names[1]
        else:
            middleName = names[1]
            lastName = names[2]

        birthYear = int(row["birth"])

        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?);", firstName, middleName, lastName, row["house"], birthYear)