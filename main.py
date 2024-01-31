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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        date TEXT NOT NULL CHECK (date LIKE '__-__-____'),
        start TEXT NOT NULL CHECK (start LIKE '__:__'),
        end TEXT NOT NULL CHECK (end LIKE '__:__')
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignedEvents (
        id INTEGER PRIMARY KEY,
        eventName TEXT NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        hours TEXT NOT NULL CHECK (hours LIKE '__:__')
    )
''')

conn.commit()
cursor.close()
conn.close()

def addStudent(name, course):
    with sqlite3.connect("database.db") as conn:
        if name and course:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
            conn.commit()
        else:
            sg.popup("Make sure all fields are filled in.", title="Empty Field")

def getStudents():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
    return result

def getEvents():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        result = cursor.fetchall()
    return result

def addStaff(name, department):
    if name and department:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO staff (name, department) VALUES (?, ?)", (name, department))
            conn.commit()
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def addEvent(name, date, start, end):
    if name and date and start and end:
        with sqlite3.connect("database.db") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO events (name, date, start, end) VALUES (?, ?, ?, ?)", (name, date, start, end))
                conn.commit()
            except:
                sg.popup("Make sure all inputs follow the correct formats.", title="Format")
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def assign(type, person, event, hours):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assignedEvents (eventName, name, type, hours) VALUES (?, ?, ?, ?)", (event, person, type, hours))
        conn.commit()



def getStaff():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff")
        result = cursor.fetchall()
    return result

def removeStaff(name):
    if name:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM staff WHERE name = ?", (name,))
            conn.commit()
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def removeStudent(name):
    if name:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE name = ?", (name,))
            conn.commit()
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def removeEvent(name):
    if name:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE name = ?", (name,))
            conn.commit()
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def getOptions():
    options = []
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students")
        options.append([item[0] for item in cursor.fetchall()])

        cursor.execute("SELECT name FROM staff")
        options.append([item[0] for item in cursor.fetchall()])

        cursor.execute("SELECT name FROM events")
        options.append([item[0] for item in cursor.fetchall()])

    return options

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

eventsLayout = [
    [sg.Text("Events Database", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Add Event", [
        [sg.Text("Name"), sg.Input(key="-EVENT_NAME-")],
        [sg.Text("Date"), sg.Input(key="-EVENT_DATE-"), sg.CalendarButton("Pick Date", target="-EVENT_DATE-", format="%d-%m-%Y")],
        [sg.Text("Starting Time (HH:MM)"), sg.Input(key="-EVENT_START-")],
        [sg.Text("End Time (HH:MM)"), sg.Input(key="-EVENT_END-")],
        [sg.Button("Add", key="-EVENT_ADD-")],
    ])],
    [sg.Frame("Remove Event", [
        [sg.Text("Name"), sg.Input(key="-DELETE_EVENT_NAME-")],
        [sg.Button("Delete", key="-DELETE_EVENT-")],
    ])],
    [sg.Table(values=getEvents(), headings=["Table ID", "Name", "Date", "Start", "End"], justification = "left", auto_size_columns = True, key="-EVENTS_TABLE-")]

]

assignLayout = [
    [sg.Text("Assign Event", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Assign", [
        [sg.Text("Type & Name"), sg.Combo(["Staff", "Student"], key="-ASSIGN_TYPE-", enable_events=True, readonly=True)],
        [sg.Combo(["Pick a type"], key="-ASSIGN_PERSON-")],
        [sg.Text("Event"), sg.Combo(getOptions()[2], key="-ASSIGN_EVENT-")],
        [sg.Text("Hours (HH:MM)"), sg.Input(key="-ASSIGN_HOURS-")],
        [sg.Button("Assign", key="-ASSIGN-")],
    ])],

    
]

layout = [
    [
        sg.TabGroup([
            [sg.Tab("Students", studentsLayout)],
            [sg.Tab("Staff", staffLayout)],
            [sg.Tab("Events", eventsLayout)],  
            [sg.Tab("Assign", assignLayout)]
        ])
    ]
]

window = sg.Window("Application", layout)

def refreshWindow():
    window['-STAFF_TABLE-'].update(values=getStaff())
    window['-STUDENTS_TABLE-'].update(values=getStudents())
    window['-EVENTS_TABLE-'].update(values=getEvents())

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

    if event == "-EVENT_ADD-":
        addEvent(values["-EVENT_NAME-"], values["-EVENT_DATE-"], values["-EVENT_START-"], values["-EVENT_END-"])
        refreshWindow()

    if event == "-DELETE_STUDENT-":
        removeStudent(values["-DELETE_STUDENT_NAME-"])
        refreshWindow()

    if event == "-DELETE_STAFF-":
        removeStaff(values["-DELETE_STAFF_NAME-"])
        refreshWindow()

    if event == "-DELETE_EVENT-":
        removeEvent(values["-DELETE_EVENT_NAME-"])
        refreshWindow()

    if event == "-ASSIGN_TYPE-":
        match values["-ASSIGN_TYPE-"]:
            case "Student":
                window["-ASSIGN_PERSON-"].update(values=getOptions()[0])
            case "Staff":
                window["-ASSIGN_PERSON-"].update(values=getOptions()[1])

    if event == "-ASSIGN-":
        assign(values["-ASSIGN_TYPE-"], values["-ASSIGN_PERSON-"], values["-ASSIGN_EVENT-"], values["-ASSIGN_HOURS-"])


window.close()