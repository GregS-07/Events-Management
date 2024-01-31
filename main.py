import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        hours INTEGER DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        hours INTEGER DEFAULT 0
    )
''')

conn.commit()
cursor.close()
conn.close()

def addStudent(name, course):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
        conn.commit()

def getStudents():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
    return result

def addStaff(name, department):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO staff (name, department) VALUES (?, ?)", (name, department))
        conn.commit()

def getStaff():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff")
        result = cursor.fetchall()
    return result

def removeStaff(name):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM staff WHERE name = ?", (name,))
        conn.commit()

def removeStudent(name):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE name = ?", (name,))
        conn.commit()

studentsLayout = [
    [sg.Text("Students Database", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Add Student", [
        [sg.Text("Student"), sg.Input(key="-STUDENT_NAME-")],
        [sg.Text("Course"), sg.Input(key="-STUDENT_COURSE-")],
        [sg.Button("Add", key="-STUDENT_ADD-")],
    ])],
    [sg.Frame("Delete Student", [
        [sg.Text("Student"), sg.Input(key="-DELETE_STUDENT_NAME-")],
        [sg.Button("Delete", key="-DELETE_STUDENT-")],
    ])],
    [sg.Table(values=getStudents(), headings=["Table ID", "Name", "Course", "Hours Worked"], justification="left", auto_size_columns=True, key="-STUDENTS_TABLE-")],
]


staffLayout = [
    [sg.Text("Staff Database", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Add Staff", [
        [sg.Text("Staff"), sg.Input(key="-STAFF_NAME-")],
        [sg.Text("Department"), sg.Input(key="-STAFF_DEPARTMENT-")],
        [sg.Button("Add", key="-STAFF_ADD-")],
    ])],
    [sg.Frame("Remove Staff", [
        [sg.Text("Staff"), sg.Input(key="-DELETE_STAFF_NAME-")],
        [sg.Button("Remove", key="-DELETE_STAFF-")],
    ])],
    [sg.Table(values=getStaff(), headings=["Table ID", "Name", "Department", "Hours Worked"], justification = "left", auto_size_columns = True, key="-STAFF_TABLE-")]
]


layout = [
    [
        sg.TabGroup([
            [sg.Tab("Students", studentsLayout)],
            [sg.Tab("Staff", staffLayout)],
            [sg.Tab("Events", [[sg.Text("Events Database")]])],  
        ])
    ]
]

window = sg.Window("Application", layout)

def refreshWindow():
    window['-STAFF_TABLE-'].update(values=getStaff())
    window['-STUDENTS_TABLE-'].update(values=getStudents())

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-STUDENT_ADD-":
        addStudent(values["-STUDENT_NAME-"], values["-STUDENT_COURSE-"])
        refreshWindow()

    if event == "-STAFF_ADD-":
        addStaff(values["-STAFF_NAME-"], values["-STAFF_DEPARTMENT-"])
        refreshWindow()

    if event == "-DELETE_STUDENT-":
        removeStudent(values["-DELETE_STUDENT_NAME-"])
        refreshWindow()

    if event == "-DELETE_STAFF-":
        removeStaff(values["-DELETE_STAFF_NAME-"])
        refreshWindow()

window.close()