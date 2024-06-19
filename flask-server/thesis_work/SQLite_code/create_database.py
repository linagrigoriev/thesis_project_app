import sqlite3

conn = sqlite3.connect('university_timetable.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Professors (
             professor_id TEXT PRIMARY KEY,
             professor_name TEXT)''')

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
             professor1_id TEXT,
             professor2_id TEXT,
             seminar_laboratory TEXT,
             study_program_id TEXT,
             short_name TEXT,
             FOREIGN KEY (professor1_id) REFERENCES Professors(professor_id),
             FOREIGN KEY (professor2_id) REFERENCES Professors(professor_id),
             FOREIGN KEY (study_program_id) REFERENCES Study_Programs(study_program_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS Groups_Structure (
             group_id TEXT PRIMARY KEY,
             study_program_id TEXT,
             num_group INTEGER,
             FOREIGN KEY (study_program_id) REFERENCES Study_Programs(study_program_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS Subgroups_Structure (
             subgroup_id TEXT PRIMARY KEY,
             study_program_id TEXT,
             num_subgroup INTEGER,
             FOREIGN KEY (study_program_id) REFERENCES Study_Programs(study_program_id))''')

professors_data = [
    ('P1', 'lect. dr. Vlad Sorin'),
    ('P2', 'conf. dr. Boghean Carmen'),
    ('P3', 'lect. dr. ing. Balan Ionut'),
    ('P4', 'lect. dr. Cozorici Angela'),
    ('P5', 'lect. dr. State Mihaela'),
    ('P6', 'conf. dr. Lupan Mariana'),
    ('P7', 'conf. dr. Socaciu Tiberiu'),
    ('P8', 'lect. dr. ing. Sfichi Stefan'),
    ('P9', 'as. dr. Cosmulese Gabriela'),
    ('P10', 'lect. dr. Bores Ana-Maria'),
    ('P11', 'lect. dr. Grigoras-Ichim Claudia'),
    ('P12', 'conf. dr. Boghean Florin'),
    ('P13', 'lect. dr. Vlad Mariana'),
    ('P14', 'as. dr. Cosmulese Gabriela'),
    ('P15', 'lect. dr. Ciubotariu Marius'),
    ('P16', 'drd. Brinzaru Simona'),
    ('P17', 'conf. dr. Tulvinschi Mihaela'),
    ('P18', 'conf. dr. Kicsi Rozalia'),
    ('P19', 'conf. dr. Mihalciuc Camelia'),
    ('P20', 'conf. dr. Vancea Romulus'),
    ('P21', 'lect. dr. Hurjui Marcela'),
    ('P22', 'conf. dr. Baesu Camelia'),
    ('P23', 'lect. dr. Colomeischi Tudor'),
    ('P24', 'lect. dr. Macovei Anamaria'),
    ('P25', 'dr. Ilas Constantin'),
    ('P26', 'as. drd. colab. Scheuleac Adelina'),
    ('P27', 'lect. dr. Ichim Cristinel'),
    ('P28', 'conf. dr. Cibotaru Irina'),
    ('P29', 'drd. Brinzaru Simona'),
    ('P30', 'lect. dr. Ciubotariu Marius')
]

courses_data = [
    ('IE321', 'Proiectarea sistemelor informatice', 'P1', 'P1', 'L', 'IE3', 'PSI'),
    ('IE322', 'Strategii investiţionale în afaceri', 'P6', 'P4', 'S', 'IE3', 'INVEST'),
    ('IE323', 'Statistică macroeconomică', 'P5', 'P5', 'S', 'IE3',  'Stat macro'),
    ('IE324', 'Dispozitive şi aplicaţii mobile', 'P3', 'P3', 'L', 'IE3', 'Disp apl mob'),
    # ('IE325', 'Securitatea sistemelor informatice', 'P7', 'P7', 'IE3', 'L', 'Sec sist inform'),
    # ('IE326', 'Geopolitică', 'P2', 'P2', 'IE3', 'S', 'Geopol'),
    ('IE327', 'Grafică și programare pe internet', 'P8', 'P8', 'L', 'IE3', 'Gr prg Int'),
    ('FB321', 'Comunicare și raportare financiară', 'P11', 'P11', 'S', 'FB3', 'Com rap fin'),
    ('FB322', 'Instituții financiar-bancare internaționale', 'P9', 'P9', 'S', 'FB3', 'Inst fin b inte'),
    ('FB323', 'Gestiune bancară', 'P13', 'P13', 'S', 'FB3', 'Gest banc'),
    ('FB324', 'Audit financiar', 'P10', 'P10', 'S', 'FB3', 'Aud fin'),
    ('FB325', 'Fiscalitate', 'P17', 'P29', 'S', 'FB3', 'Fisc'),
    ('FB326', 'Controlling', 'P12', 'P30', 'S', 'FB3', 'CTRL'),
    # ('FB327', 'Analiză financiară', 'P14', 'FB3', 'Anal fin'),
    # ('AF321', 'Tranzacții și tehnici comerciale', 'P18', 'AF3', 'TrTehnCom'),
    # ('AF322', 'Fiscalitate', 'P17', 'AF3', 'Fisc'),
    # ('AF323', 'Contabilitate managerială', 'P19', 'AF3', 'CtMng'),
    # ('AF324', 'Managementul producției', 'P21', 'AF3', 'Mng prod'),
    # ('AF325', 'Baze de date', 'P3', 'AF3', 'BzDt'),
    # ('AF326', 'Tehnica negocierilor în afaceri', 'P14', 'AF3', 'Tehn neg af'),
    # ('AF327', 'Contabilitatea grupurilor de societăți', 'P13', 'AF3', 'Contab grup'),
    # ('AI321', 'Geopolitică', 'P2', 'AI3', 'Geopol'),
    # ('AI322', 'Negocieri în afaceri internaționale', 'P22', 'AI3', 'NegAI'),
    # ('AI323', 'Investiții internaționale', 'P6', 'AI3', 'Invest int'),
    # ('AI324', 'Burse internaționale de mărfuri', 'P4', 'AI3', 'Burse'),
    # ('AI325', 'Gestiunea riscului în economia globală', 'P5', 'AI3', 'Gest risc'),
    # ('AI326', 'Asigurări internaționale', 'P18', 'AI3', 'Asig int'),
    # ('IE221', 'Probabilități și statistică matematică', 'P17', 'IE2', 'Pr st mat'),
    # ('IE222', 'Multimedia', 'P8', 'IE2', 'Multim'),
    # ('IE223', 'Programare orientată pe obiect', 'P7', 'IE2', 'POO'),
    # ('IE224', 'Cercetări operaționale', 'P24', 'IE2', 'C op'),
    # ('IE225', 'Pimba engleză', 'P25', 'IE2', 'Pb eng'),
    # ('IE226', 'Educaţie fizică şi sport', 'P26', 'IE2', 'EDF'),
    # ('IE227', 'Programarea aplicaţiilor Windows', 'P8', 'IE2', 'Pr Wind'),
    # ('FB221', 'Contabilitate manageriala', 'P19', 'FB2', 'CtMang'),
    # ('FB222', 'Contabilitate bancară', 'P13', 'FB2', 'Cont Banc'),
    # ('FB223', 'Finanțe publice', 'P27', 'FB2', 'FinP'),
    # ('FB224', 'Econometrie', 'P24', 'FB2', 'Ec.metrie'),
    # ('FB225', 'Finanțe personale', 'P10', 'FB2','Fin pers'),
    # ('FB226', 'Finanţe corporative', 'P28', 'FB2', 'Fin corp'),
    # ('FB227', 'Educaţie fizică şi sport', 'P26', 'IE2', 'EDF'),
]

groups_structure_data = [
    ('IE3S1', 'IE3', 20),
    ('IE3S2', 'IE3', 20),
    ('FB3S1', 'FB3', 27),
    ('FB3S2', 'FB3', 28),
    ('AF3S1', 'AF3', 16),
    ('AF3S2', 'AF3', 17),
    ('AI3S1', 'AI3', 29),
    ('IE2S1', 'IE2', 26),
    ('IE2S2', 'IE2', 26),
    ('FB2S1', 'FB2', 22),
    ('FB2S2', 'FB2', 22),
    ('FB2S3', 'FB2', 23),
]

subgroups_structure_data = [
    ('IE3L1', 'IE3', 14),
    ('IE3L2', 'IE3', 13),
    ('IE3L3', 'IE3', 13),
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

c.executemany("INSERT INTO Professors VALUES (?, ?)", professors_data)
c.executemany("INSERT INTO Rooms VALUES (?, ?, ?)", rooms_data)
c.executemany("INSERT INTO Study_Programs VALUES (?, ?)", study_programs_data)
c.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?, ?, ?, ?)", courses_data)
c.executemany("INSERT INTO Groups_Structure VALUES (?, ?, ?)", groups_structure_data)
c.executemany("INSERT INTO Subgroups_Structure VALUES (?, ?, ?)", subgroups_structure_data)

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
