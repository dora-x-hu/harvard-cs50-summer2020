from cs50 import get_string

def main():
    excerpt = get_string("Text: ")
    grade = calculate(excerpt)
    if(grade - int(grade) > int(grade) + 1 - grade):
        intgrade = int(grade) + 1
    else:
        intgrade = int(grade)
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {intgrade}")

def calculate(text):
    i = 0
    letters = 0.0
    words = 1.0
    sentences = 0.0
    spaces = 0
    n = len(text)
    while i < n:
        if text[i] == ' ':
            spaces += 1
        if (ord(text[i]) >= 65 and ord(text[i]) <= 90) or (ord(text[i]) >= 97 and ord(text[i]) <= 122):
            letters += 1
        if text[i] == '.' or text[i] == '?' or text[i] == '!':
            sentences += 1
        if ((ord(text[i]) >= 65 and ord(text[i]) <= 90) or (ord(text[i]) >= 97 and ord(text[i]) <= 122)) and spaces == 1:
            words += 1
            spaces = 0
        i += 1
    L = letters/words * 100
    S = sentences/words * 100
    thisGrade =  0.0588 * L - 0.296 * S - 15.8
    return thisGrade

main()