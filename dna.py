import csv
import sys

# if incorrect number of command-line arguments
if(len(sys.argv) != 3):
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# list of STRs
strs = list()
strCount = 0
lineCount = 0
# list of ppl whose DNA sequences we're looking at
people = []
name = ""
# open the csv file for reading
with open(sys.argv[1]) as csv_file:
    reader = csv.reader(csv_file, delimiter = ',')
    # goes through each row in the file
    for row in reader:
        index = 0
        # a list of str counts for a single person
        counts = []
        # WHAT TO DO FOR 1ST LINE OF CSV FILE (LIST OF STRS)
        if lineCount == 0:
            # goes through each item in each row
            for item in row:
                if strCount > 0:
                    strs.append(item)
                strCount += 1
        # DEALING WITH ALL THE NUMBERS OF STRS FOR EACH PERSON
        else:
            for item in row:
                # if looking at the name of the person
                if index == 0:
                    name = item
                    index += 1
                else:
                    counts.append(item)
            person = (name, counts)
            people.append(person)
        lineCount += 1

file = open(sys.argv[2], "r")
dna = file.read()
file.close()




maxStr = []
for stri in strs:
    index = 0
    consecutive = 0
    max = 0
    while index <= len(dna)-len(stri):
        sample = ""
        for i in range(len(stri)):
            sample += dna[index+i]
        if sample == stri:
            consecutive += 1
            index += len(stri)
        else:
            if consecutive > max:
                max = consecutive
            consecutive = 0
            index += 1
    maxStr.append(max)








# check to see which person matches the max array!
personIndex = 0
for person in people:
    index = 0
    thisTheOne = True
    for maxCount in maxStr:
        if str(maxCount) == person[1][index]:
            index += 1
            continue
        else:
            thisTheOne = False
            break
    if thisTheOne == True:
        for namey in person:
            print(f"{namey}")
            break
        exit(0)
    personIndex += 1
print("No match")
exit(0)
