import sqlite3
import time
from Student import Student

connection = sqlite3.connect('studentDB.db')
cursor = connection.cursor()

def main():
    createTable()
    insertStudents()
    welcome()
    connection.close()

def welcome():
    #Shows main menu, gives you six options.
    try:
        selection = int(input("Welcome, please select the task you would like to complete:\n"
        "1. Display all students and all their attributes\n"
        "2. Create students\n"
        "3. Update students\n"
        "4. Delete students by student ID\n"
        "5. Search by major, GPA, or advisor\n"
                              "6. Quit \n"))
    #Input validation
    except ValueError:
        print("That is not a valid option.")
        time.sleep(1)
        welcome()

    #Task selection
    if selection == 1:
        view()
    elif selection == 2:
        createStudents()
    elif selection == 3:
        updateStudents()
    elif selection == 4:
        deleteStudent()
    elif selection == 5:
        displayStudent()
    elif selection == 6:
        quit()
    else:
        print("That is not a valid option")
        time.sleep(2)
        welcome()

def createTable():
    #Create a table in the database called Student if it doesnt already exist.
    cursor.execute("Create table if not exists Student("
        "studentid integer primary key AUTOINCREMENT,"
        "firstname varchar(25),"
        "lastname varchar(25),"
        "gpa numeric,"
        "major varchar(10),"
        "facultyadvisor varchar(25))"
    )
    connection.commit()

def insertStudents():
    #Inserting 'students' into the table.
    cursor.execute("INSERT INTO Student('firstname', 'lastname', 'gpa', 'major', 'facultyadvisor')"
                   " VALUES (?,?,?,?,?)",
                   ('harry', 'flu', '3.5', 'Psy', 'Bob'))
                   #('eric', 'loaf', '3.0', 'SW', 'Fred'))
                   #('donk', 'dunn', '2.0', 'Acting', 'Sheila'))
                   #('ryan', 'kap', '3.0', 'SW', 'Bob'))
    connection.commit()

def view():
    #View all student records in the table
    cursor.execute("Select * from Student")
    connection.commit()
    print(cursor.fetchall())
    print("Students shown, returning to menu.")
    time.sleep(4)
    welcome()

def createStudents():
    #Prompted for all information necesssary to add a student
    firstname = input("Please enter the students first name.")
    lastname = input("Please enter the students last name.")
    gpa = input("Please enter the students GPA.")
    major = input("Please enter the students major")
    facultyadvisor = input("Please enter the students faculty advisor")
    #Concatenated to see if string has any numbers in it. If yes = bad
    concatenated = firstname + lastname + major + facultyadvisor
    try:
        #Try to turn gpa to a float, if it doesnt work its not a valid gpa.
        myGpa = float(gpa)
        #If no numbers in concatenated string we good to keep going
        if not any(char.isdigit() for char in concatenated):
            #If strings are not empty we good to keep going
            if firstname and lastname and gpa and major and facultyadvisor:
                #If gpa is in bounds we good to keep going
                if myGpa > 0 and myGpa <= 4:
                    #Insert record
                    stu = Student(firstname, lastname, gpa, major, facultyadvisor)
                    cursor.execute("INSERT INTO Student('firstname', 'lastname', 'gpa', 'major', 'facultyadvisor')"
                                   " VALUES (?,?,?,?,?)",
                                   (stu.getStudentTuple()))
                    connection.commit()
                    print("Record created, returning to menu")
                    time.sleep(3)
                    welcome()
                else:
                    print("You did not enter a valid GPA, try again.")
                    time.sleep(2)
                    createStudents()
            else:
                print("Theres an error in your input(s), try again.")
                createStudents()
        else:
            print("You can not enter numbers for certain values, try again.")
            time.sleep(1)
            createStudents()
    except ValueError:
        print("Not a GPA, try again")
        time.sleep(3)
        createStudents()


def updateStudents():
    studentid = input("To update a students information, enter their student ID.")

    #I want to test that this studentID exists so I select all records that match
    # the ID and if the results are blank, I know there is no ID match.

    cursor.execute("""Select * from Student where studentid = (?)""",(studentid,))
    all_rows = cursor.fetchall()
    if (len(all_rows) == 0):
        print("Not a valid ID, try again\n")
        time.sleep(2)
        updateStudents()

    #User can change major, advisor or both
    selection = int(input("1. Update Major\n2. Update Advisor\n3. Both"))
    if (selection == 1):
        major = input("What is the students new major?")
        #Input validation, no numbers in major.
        if not any(char.isdigit() for char in major):
            cursor.execute("""update Student set major = (?) where studentid = (?)""",(major, studentid))
            connection.commit()
        else:
            print("Your major should not have numbers in it, try again.")
            updateStudents()
    elif (selection == 2):
        advisor = input("Who is the students new advisor?")
        # Input validation, no numbers in advisor.
        if not any(char.isdigit() for char in advisor):
            cursor.execute("""update Student set facultyadvisor = (?) where studentid = (?)""",(advisor, studentid))
            connection.commit()
        else:
            print("Your advisor should not have numbers in it, try again.")
            updateStudents()
    elif (selection ==3):
        advisor = input("Who is the students new advisor?")
        major = input("What is the students new major?")
        # Input validation, no numbers in both.
        concatenated = advisor + major
        if not any(char.isdigit() for char in concatenated):
            cursor.execute("""update student set facultyadvisor = (?), major = (?) where studentid = (?)""",(advisor,major,studentid))
            connection.commit()
        else:
            print("None of your entries should include numbers, try again.")
            updateStudents()
    else:
        print("Not a valid option.")
        updateStudents()

    print("Record(s) updated, returning to menu")
    time.sleep(3)
    welcome()

#https://stackoverflow.com/questions/1307378/python-mysql-update-statement
#I find the three quotes easier to deal with so I began using it for delete

def deleteStudent():
    studentid = input("Please enter a valid student ID.")
    #Input validation, student id is a number.
    #If you enter a student id that is not in the table it wont delete anything.
    if studentid.isdigit():
        cursor.execute("""delete from Student where studentid = (?)""",(studentid,))
        connection.commit()
        print("If found, record was deleted, returning to menu")
        time.sleep(3)
        welcome()
    else:
        print("You did not enter a student ID, try again.")
        time.sleep(1)
        deleteStudent()


def displayStudent():
    major = input("Please enter a major. Leave blank if you do not wish to search by major.")
    gpa = input("Please enter a GPA. Leave blank if you do not wish to search by GPA.")
    try:
        #input validation, gpa needs to be a float
        myGpa = float(gpa)
    except ValueError:
        print("You did not enter a valid GPA, try again.")
        displayStudent()
        #input validation, gpa needs to be in bounds.
    if myGpa > 4 or myGpa < 0:
        print("You did not enter a valid GPA, try again.")
        displayStudent()

    else:
        advisor = input("Please enter an advisor. Leave blank if you do not wish to search by advisor.")
        concatenated = major + advisor
        #input validation, no numbers should be in major or advisor
        if not any(char.isdigit() for char in concatenated):
            #We display different results based on which fields are left blank
            if not major and not gpa and advisor:
                #do advisor
                cursor.execute("""select * from Student where facultyadvisor = (?)""", (advisor,))
                connection.commit()
                print(cursor.fetchall())
            elif not major and not advisor and gpa:
                #do gpa
                cursor.execute("""select * from Student where gpa = (?)""", (gpa,))
                connection.commit()
                print(cursor.fetchall())
            elif not gpa and not advisor and major:
                #do major
                cursor.execute("""select * from Student where major = (?)""", (major,))
                connection.commit()
                print(cursor.fetchall())
            elif not major and advisor and gpa:
                #do advisor and gpa
                cursor.execute("""select * from Student where facultyadvisor = (?) and gpa = (?)""", (advisor, gpa,))
                connection.commit()
                print(cursor.fetchall())
            elif not gpa and major and advisor:
                #do major and advisor
                cursor.execute("""select * from Student where facultyadvisor = (?) and major = (?)""", (advisor, major,))
                connection.commit()
                print(cursor.fetchall())
            elif not advisor and major and gpa:
                cursor.execute("""select * from Student where major = (?) and gpa = (?)""", (major, gpa,))
                connection.commit()
                print(cursor.fetchall())
                #do major and gpa
            elif major and gpa and advisor:
                cursor.execute("""select * from Student where facultyadvisor = (?) and gpa = (?) and major = (?)""", (advisor, gpa, major,))
                connection.commit()
                print(cursor.fetchall())
            else:
                print("Not a valid choice, try again")
                displayStudent()
            print("If table is empty, no matching records were found.")
            time.sleep(3)
            welcome()
        else:
            print("Your major or advisor should not have numbers in it, try again.")
            displayStudent()

main()




