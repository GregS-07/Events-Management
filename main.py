import PySimpleGUI as sg
import sqlite3
import re

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
        name TEXT UNIQUE NOT NULL,
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

def isTimeFormat(time_string):
    time_regex = r'^[0-2][0-9]:[0-5][0-9]$'
    return bool(re.match(time_regex, time_string))

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

def getDepartments():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT department, SUM(hours) AS total_hours
                    FROM staff
                    GROUP BY department;
        """)
        result = cursor.fetchall()
    return result

def addStaff(name, department):
    if name and department:
        with sqlite3.connect("database.db") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO staff (name, department) VALUES (?, ?)", (name, department))
                conn.commit()
            except:
                sg.popup("Make sure you aren't attempting to enter a duplicate value", title="Invalid Input")
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def addEvent(name, date, start, end):
    if name and date and start and end:
        with sqlite3.connect("database.db") as conn:
            if isTimeFormat(start) and isTimeFormat(end):
                cursor = conn.cursor()
                cursor.execute("INSERT INTO events (name, date, start, end) VALUES (?, ?, ?, ?)", (name, date, start, end))
                conn.commit()
            else:
                sg.popup("Make sure all inputs follow the correct formats.", title="Format")
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")

def assign(type, person, event, hours):
    if type and person and event and hours:
        with sqlite3.connect("database.db") as conn:
            if isTimeFormat(hours):
                cursor = conn.cursor()
                cursor.execute("INSERT INTO assignedEvents (eventName, name, type, hours) VALUES (?, ?, ?, ?)", (event, person, type, hours))
                conn.commit()
            else:
                sg.popup("Make sure you follow all the format requirements")
    else:
        sg.popup("Make sure all fields are filled in", title="Empty Fields")

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

def unassign(name):
    if name:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assignedEvents WHERE name = ?", (name,))
            conn.commit()
            refreshWindow()
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

def getAssignedHours():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM assignedEvents
            ORDER BY eventName
        ''')
    
    return cursor.fetchall()

studentsLayout = [
    [sg.Text("Students Database", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Add Student", [
        [sg.Text("Student"), sg.Input(key="-STUDENT_NAME-")],
        [sg.Text("Course"), sg.Input(key="-STUDENT_COURSE-")],
        [sg.Button("Add", key="-STUDENT_ADD-")],
    ])],
    [sg.Table(values=getStudents(), headings=["Table ID", "Name", "Course", "Hours Worked"], justification="left", auto_size_columns=True, key="-STUDENTS_TABLE-", col_widths=[10, 50, 50, 20])],
    [sg.Frame("Delete Student", [
        [sg.Text("Student"), sg.Input(key="-DELETE_STUDENT_NAME-")],
        [sg.Button("Delete", key="-DELETE_STUDENT-")],
    ])],
]


staffLayout = [
    [sg.Text("Staff Database", font=("Helvetica", 14, "underline"))],
    [sg.Frame("Add Staff", [
        [sg.Text("Staff"), sg.Input(key="-STAFF_NAME-")],
        [sg.Text("Department"), sg.Input(key="-STAFF_DEPARTMENT-")],
        [sg.Button("Add", key="-STAFF_ADD-")],
    ])],
    [sg.Table(values=getStaff(), headings=["Table ID", "Name", "Department", "Hours Worked"], justification = "left", auto_size_columns = True, key="-STAFF_TABLE-", col_widths=[10, 200, 50, 20])],
    [sg.Frame("Remove Staff", [
        [sg.Text("Staff"), sg.Input(key="-DELETE_STAFF_NAME-")],
        [sg.Button("Remove", key="-DELETE_STAFF-")],
    ])],
    [sg.Frame("Departments", [
        [sg.Table(values = getDepartments(), headings=["Department", "Hours"], justification = "left", auto_size_columns = True, key="-DEPARTMENT_TABLE-")]
    ])]
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
    [sg.Table(values=getEvents(), headings=["Table ID", "Name", "Date", "Start", "End"], justification = "left", auto_size_columns = True, key="-EVENTS_TABLE-", col_widths=[10, 200, 20, 20, 20])],
    [sg.Frame("Remove Event", [
        [sg.Text("Name"), sg.Input(key="-DELETE_EVENT_NAME-")],
        [sg.Button("Delete", key="-DELETE_EVENT-")],
    ])],


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
    [sg.Frame("Assigned Hours", [
        [sg.Table(values = getAssignedHours(), headings=["Table ID", "Event", "Person", "Type", "Hours"], key="-ASSIGN_TABLE-", auto_size_columns = True, justification="left", col_widths=[10, 50, 50, 20, 20])]
    ])],
    [sg.Frame("Unassign All", [
        [sg.Text("Name"), sg.Input(key="-UNASSIGN_NAME-")],
        [sg.Button("Unassign", key="-UNASSIGN-")]
    ])],
    [sg.Frame("Unassign Specific", [
        [sg.Text("Name"), sg.Input(key="-UNASSIGN_NAME_S-")],
        [sg.Text("Event"), sg.Combo(values=getOptions()[2], key="-UNASSIGN_EVENT_S-")],
        [sg.Button("Unassign", key="-UNASSIGN_S-")]
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

def createWindow():
    return sg.Window("Application", layout)

window = createWindow()

def updateHours():
    # with sqlite3.connect("database.db") as conn:
    #     cursor = conn.cursor()

    #     print("before updating")
    #     for row in getStaff():
            
    #         print(row)

    #     cursor.execute('''
    #         SELECT name, SUM(CAST(SUBSTR(hours, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(hours, 4, 2) AS INTEGER)) AS total_minutes
    #         FROM assignedEvents
    #         GROUP BY name
    #     ''')

    #     results = cursor.fetchall()

    #     for person, total_minutes in results:
    #         total_hours = f'{total_minutes // 60:02d}:{total_minutes % 60:02d}'

    #         cursor.execute("UPDATE students SET hours = ? WHERE name = ?", (total_hours, person))

    #         cursor.execute("UPDATE staff SET hours = ? WHERE name = ?", (total_hours, person))

    #     conn.commit()

    #     print("after updating")
    #     for row in getStaff():
    #         print(row)

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        print("before updating")
        for row in getStaff():
            print(row)
        
        cursor.execute('''
            SELECT name, SUM(CAST(SUBSTR(hours, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(hours, 4, 2) AS INTEGER)) AS total_minutes
            FROM assignedEvents
            GROUP BY name
        ''')

        results = cursor.fetchall()

        for person, total_minutes in results:
            total_hours = f'{total_minutes // 60:02d}:{total_minutes % 60:02d}'

            cursor.execute("UPDATE students SET hours = ? WHERE name = ?", (total_hours, person))

            cursor.execute("UPDATE staff SET hours = ? WHERE name = ?", (total_hours, person))

        conn.commit()
    
        print("after updating")
        for row in getStaff():
            print(row)

def unassignS(name, event):
    if name and event:
        with sqlite3.connect("database.db") as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM assignedEvents WHERE name = ? AND eventName = ?", (name, event))
                conn.commit()
                refreshWindow()
            except: 
                sg.popup("Make sure the fields are valid", title="Invalid Input")
    else:
        sg.popup("Make sure all fields are filled in.", title="Empty Field")
    
updateHours()

def refreshWindow():
    updateHours()
    window['-STAFF_TABLE-'].update(values=getStaff())
    window['-STUDENTS_TABLE-'].update(values=getStudents())
    window['-EVENTS_TABLE-'].update(values=getEvents())
    window['-ASSIGN_TABLE-'].update(values=getAssignedHours())
    window["-ASSIGN_EVENT-"].update(values=getOptions()[2])
    window["-UNASSIGN_EVENT_S-"].update(values=getOptions()[2])
    window["-DEPARTMENT_TABLE-"].update(values=getDepartments())

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
        refreshWindow()

    if event == "-ASSIGN-":
        assign(values["-ASSIGN_TYPE-"], values["-ASSIGN_PERSON-"], values["-ASSIGN_EVENT-"], values["-ASSIGN_HOURS-"])
        refreshWindow()

    if event == "-UNASSIGN-":
        unassign(values["-UNASSIGN_NAME-"])


    if event == "-UNASSIGN_S-":
        unassignS(values["-UNASSIGN_NAME_S-"], values["-UNASSIGN_EVENT_S-"])


window.close()