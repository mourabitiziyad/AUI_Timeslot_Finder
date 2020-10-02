import pdfplumber
from bs4 import BeautifulSoup
from pathlib import Path
import os

def read_scrape_professors():
    professors = []
    path = Path(__file__).parent / "professors.txt"
    with open(path, 'r',  encoding='utf-8') as reader:
        professors = reader.readlines()
    for i in range(len(professors)):
        soup = BeautifulSoup(professors[i], 'lxml')
        professors[i] = soup.text
        string = professors[i]
        string = string[:-1]
        string = string[:string.index(',')]
        professors[i] = string
    return professors

prof_LNames = read_scrape_professors()

M, T, W, R, F = [], [], [], [], []
p = Path(__file__).parent / 'Schedules'
files = os.listdir(p)
for f in files:
    print(f)
    path = Path(__file__).parent / "./Schedules" / f
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        # print(first_page.chars[0])
        text = page.extract_text()
        text = text.split('\n')
    count = 0
    trimmed_text = []
    for i in text:
        if count:
            trimmed_text.append(i)
        if "Course:" in i:
            count = 1
        else:
            count = 0

    schedules = []

    for i in range(len(trimmed_text)):
        string = trimmed_text[i]
        for m in prof_LNames:
            if m in string:
                string = string[string.index(m)+len(m):]
                if string[0] == ' ':
                    string = string[1:]
                trimmed_text[i] = string

    print(trimmed_text)
    for i in trimmed_text:
        counter = 0
        days = ''
        for letter in i:
            if letter == " ":
                counter = 5
            elif letter == 'M' and counter < 5:
                days += "M"
                counter += 1
            elif letter == "T" and counter < 5:
                days += "T"
                counter += 1
            elif letter == "W" and counter < 5:
                days += "W"
                counter += 1
            elif letter == "R" and counter < 5:
                days += "R"
                counter += 1
            elif letter == "F" and counter < 5:
                days += "F"
                counter += 1
            if letter == ':':
                colon = i.index(letter)
                # print(i[colon-2:colon+3], i[colon+4:colon+6])
                if i[colon+4:colon+6] == "AM" or i[colon-2:colon] == "12":
                    start_time = i[colon-2:colon] + i[colon+1:colon+3]
                    # print(start_time)
                elif i[colon+4:colon+6] == "PM":
                    start_time = str(int(i[colon-2:colon])+12) + i[colon+1:colon+3]
                    # print(start_time)
                colon_2 = i.index(letter)+19
                # print(i[colon_2-2:colon_2+3], i[colon_2+4:colon_2+6])
                if i[colon_2+4:colon_2+6] == "AM" or i[colon_2-2:colon_2] == "12":
                    end_time = i[colon_2-2:colon_2] + i[colon_2+1:colon_2+3]
                    # print(end_time)
                elif i[colon_2+4:colon_2+6] == "PM":
                    end_time = str(int(i[colon_2-2:colon_2])+12) + i[colon_2+1:colon_2+3]
                    # print(end_time)

                for i in days:
                    if i == "M":
                        M.append([start_time, end_time])
                    elif i == "T":
                        T.append([start_time, end_time])
                    elif i == "W":
                        W.append([start_time, end_time])
                    elif i == "R":
                        R.append([start_time, end_time])
                    elif i == "F":
                        F.append([start_time, end_time])
                break
            
M.sort()
T.sort()
W.sort()
R.sort()
F.sort()

print("checking: ", os.listdir(p))

def free_time_finder(schedules):
    try:
        for i in range(len(schedules)):
            if (len(schedules) == 1):
                print("any other time is free other than: ", schedules)
                break
            if(len(schedules) == 0):
                print("The entire day is free!")
                break
            if (schedules[i][1] < schedules[i+1][0]):
                print("there is freetime between: ", schedules[i][1], "and", schedules[i+1][0])
    except IndexError:
        print("there is freetime after: ", schedules[-1][1])


print("Monday: \n")
free_time_finder(M)
print("\n")
print("Tuesday: \n")
free_time_finder(T)
print("\n")
print("Wednesday: \n")
free_time_finder(W)
print("\n")
print("Thursday: \n")
free_time_finder(R)
print("\n")
print("Friday: \n")
free_time_finder(F)