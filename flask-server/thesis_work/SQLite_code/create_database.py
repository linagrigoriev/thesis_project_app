import sqlite3

conn = sqlite3.connect('university_timetable.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Lecturers (
             lecturer_id TEXT PRIMARY KEY,
             lecturer_name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Rooms (
             room_id TEXT PRIMARY KEY,
             room_name TEXT,
             capacity INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS Study_Programs (
             study_program_id TEXT PRIMARY KEY,
             num_study_program INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS Courses (
             course_id TEXT PRIMARY KEY,
             course_name TEXT,
             lecturer_id TEXT,
             study_program_id TEXT,
             short_name TEXT,
             FOREIGN KEY (lecturer_id) REFERENCES Lecturers(lecturer_id),
             FOREIGN KEY (study_program_id) REFERENCES Study_Programs(study_program_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS Groups_Structure (
             group_id TEXT PRIMARY KEY,
             study_program_id TEXT,
             num_group INTEGER,
             FOREIGN KEY (study_program_id) REFERENCES Study_Programs(study_program_id))''')

lecturers_data = [
    ('L1', 'lect. dr. Vlad Sorin'),
    ('L2', 'conf. dr. Boghean Carmen'),
    ('L3', 'lect. dr. ing. Balan Ionut'),
    ('L4', 'lect. dr. Cozorici Angela'),
    ('L5', 'lect. dr. State Mihaela'),
    ('L6', 'conf. dr. Lupan Mariana'),
    ('L7', 'conf. dr. Socaciu Tiberiu'),
    ('L8', 'lect. dr. ing. Sfichi Stefan'),
    ('L9', 'as. dr. Cosmulese Gabriela'),
    ('L10', 'lect. dr. Bores Ana-Maria'),
    ('L11', 'lect. dr. Grigoras-Ichim Claudia'),
    ('L12', 'conf. dr. Boghean Florin'),
    ('L13', 'lect. dr. Vlad Mariana'),
    ('L14', 'as. dr. Cosmulese Gabriela'),
    ('L15', 'lect. dr. Ciubotariu Marius'),
    ('L16', 'drd. Brinzaru Simona'),
    ('L17', 'conf. dr. Tulvinschi Mihaela'),
    ('L18', 'conf. dr. Kicsi Rozalia'),
    ('L19', 'conf. dr. Mihalciuc Camelia'),
    ('L20', 'conf. dr. Vancea Romulus'),
    ('L21', 'lect. dr. Hurjui Marcela'),
    ('L22', 'conf. dr. Baesu Camelia'),
    ('L23', 'lect. dr. Colomeischi Tudor'),
    ('L24', 'lect. dr. Macovei Anamaria'),
    ('L25', 'dr. Ilas Constantin'),
    ('L26', 'as. drd. colab. Scheuleac Adelina'),
    ('L27', 'lect. dr. Ichim Cristinel'),
    ('L28', 'conf. dr. Cibotaru Irina')
]

courses_data = [
    ('IE321', 'Proiectarea sistemelor informatice', 'L1', 'IE3', 'PSI'),
    ('IE322', 'Strategii investiţionale în afaceri', 'L6', 'IE3', 'INVEST'),
    ('IE323', 'Statistică macroeconomică', 'L5', 'IE3', 'Stat macro'),
    ('IE324', 'Dispozitive şi aplicaţii mobile', 'L3', 'IE3', 'Disp apl mob'),
    # ('IE325', 'Securitatea sistemelor informatice', 'L7', 'IE3', 'Sec sist inform'),
    # ('IE326', 'Geopolitică', 'L2', 'IE3', 'Geopol'),
    ('IE327', 'Grafică și programare pe internet', 'L8', 'IE3', 'Gr prg Int'),
    ('FB321', 'Comunicare și raportare financiară', 'L11', 'FB3', 'Com rap fin'),
    ('FB322', 'Instituții financiar-bancare internaționale', 'L9', 'FB3', 'Inst fin b inte'),
    ('FB323', 'Gestiune bancară', 'L13', 'FB3', 'Gest banc'),
    # ('FB324', 'Audit financiar', 'L10', 'FB3', 'Aud fin'),
    # ('FB325', 'Fiscalitate', 'L17', 'FB3', 'Fisc'),
    # ('FB326', 'Controlling', 'L12', 'FB3', 'CTRL'),
    ('FB327', 'Analiză financiară', 'L14', 'FB3', 'Anal fin'),
    # ('AF321', 'Tranzacții și tehnici comerciale', 'L18', 'AF3', 'TrTehnCom'),
    ('AF322', 'Fiscalitate', 'L17', 'AF3', 'Fisc'),
    ('AF323', 'Contabilitate managerială', 'L19', 'AF3', 'CtMng'),
    ('AF324', 'Managementul producției', 'L21', 'AF3', 'Mng prod'),
    ('AF325', 'Baze de date', 'L3', 'AF3', 'BzDt'),
    # ('AF326', 'Tehnica negocierilor în afaceri', 'L14', 'AF3', 'Tehn neg af'),
    ('AF327', 'Contabilitatea grupurilor de societăți', 'L13', 'AF3', 'Contab grup'),
    ('AI321', 'Geopolitică', 'L2', 'AI3', 'Geopol'),
    ('AI322', 'Negocieri în afaceri internaționale', 'L22', 'AI3', 'NegAI'),
    ('AI323', 'Investiții internaționale', 'L6', 'AI3', 'Invest int'),
    ('AI324', 'Burse internaționale de mărfuri', 'L4', 'AI3', 'Burse'),
    ('AI325', 'Gestiunea riscului în economia globală', 'L5', 'AI3', 'Gest risc'),
    # ('AI326', 'Asigurări internaționale', 'L18', 'AI3', 'Asig int'),
    # ('IE221', 'Probabilități și statistică matematică', 'L17', 'IE2', 'Pr st mat'),
    ('IE222', 'Multimedia', 'L8', 'IE2', 'Multim'),
    ('IE223', 'Programare orientată pe obiect', 'L7', 'IE2', 'POO'),
    # ('IE224', 'Cercetări operaționale', 'L24', 'IE2', 'C op'),
    # ('IE225', 'Limba engleză', 'L25', 'IE2', 'Lb eng'),
    # ('IE226', 'Educaţie fizică şi sport', 'L26', 'IE2', 'EDF'),
    # ('IE227', 'Programarea aplicaţiilor Windows', 'L8', 'IE2', 'Pr Wind'),
    # ('FB221', 'Contabilitate manageriala', 'L19', 'FB2', 'CtMang'),
    ('FB222', 'Contabilitate bancară', 'L13', 'FB2', 'Cont Banc'),
    # ('FB223', 'Finanțe publice', 'L27', 'FB2', 'FinP'),
    ('FB224', 'Econometrie', 'L24', 'FB2', 'Ec.metrie'),
    # ('FB225', 'Finanțe personale', 'L10', 'FB2','Fin pers'),
    ('FB226', 'Finanţe corporative', 'L28', 'FB2', 'Fin corp'),
    # ('FB227', 'Educaţie fizică şi sport', 'L26', 'IE2', 'EDF'),
]

groups_structure_data = [
    ('IE3G1', 'IE3', 20),
    ('IE3G2', 'IE3', 20),
    ('FB3G1', 'FB3', 27),
    ('FB3G2', 'FB3', 28),
    ('AF3G1', 'AF3', 16),
    ('AF3G2', 'AF3', 17),
    ('AI3G1', 'AI3', 29),
    ('IE2G1', 'IE2', 26),
    ('IE2G2', 'IE2', 26),
    ('FB2G1', 'FB2', 22),
    ('FB2G2', 'FB2', 22),
    ('FB2G3', 'FB2', 23),
]

rooms_data = [
    ('R1', 'Room A', 70),
    ('R2', 'Room B', 55),
    ('R3', 'Room C', 40),
    ('R4', 'Room D', 30),
    # ('R5', 'Room E', 60),
    # ('R6', 'Room F', 75),
    # ('R7', 'Room G', 60),
]

study_programs_data = [
    ('IE3', 40),
    ('FB3', 67),
    ('AF3', 33),
    ('AI3', 29),
    ('IE2', 52),
    ('FB2', 55),
]

c.executemany("INSERT INTO Lecturers VALUES (?, ?)", lecturers_data)
c.executemany("INSERT INTO Rooms VALUES (?, ?, ?)", rooms_data)
c.executemany("INSERT INTO Study_Programs VALUES (?, ?)", study_programs_data)
c.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?, ?)", courses_data)
c.executemany("INSERT INTO Groups_Structure VALUES (?, ?, ?)", groups_structure_data)

c.execute('''CREATE TABLE IF NOT EXISTS TimeSlots (
             start_time TEXT,
             slot_id TEXT PRIMARY KEY,
             end_time TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Days (
             day_id TEXT PRIMARY KEY,
             day_name TEXT)''')

time_slots_data = [
    ("1", "8", "10"),  # Slot 1: 8:00 - 10:00
    ("2", "10", "12"),  # Slot 2: 10:00 - 12:00
    ("3", "12", "14"),  # Slot 3: 12:00 - 14:00
    ("4", "14", "16"),  # Slot 4: 14:00 - 16:00
    ("5", "16", "18"),  # Slot 5: 16:00 - 18:00
    ("6", "18", "20")   # Slot 6: 18:00 - 20:00
]

days_data = [
    ("1", "Luni"),
    ("2", "Marti"),
    ("3", "Miercuri"),
    ("4", "Joi"),
    ("5", "Vineri")
]

c.executemany("INSERT INTO TimeSlots VALUES (?, ?, ?)", time_slots_data)

c.executemany("INSERT INTO Days VALUES (?, ?)", days_data)

conn.commit()
conn.close()

print("Database populated successfully.")
