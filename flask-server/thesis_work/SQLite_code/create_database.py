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

c.execute('''CREATE TABLE IF NOT EXISTS TimeSlots (
             start_time TEXT,
             slot_id TEXT PRIMARY KEY,
             end_time TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Days (
             day_id TEXT PRIMARY KEY,
             day_name TEXT)''')

professors_data = [
    ('P1', 'lect. dr. Vlad Sorin'),
    ('P2', 'conf. dr. Boghean Carmen'),
    ('P3', 'lect. dr. ing. Balan Ionuț'),
    ('P4', 'lect. dr. Cozorici Angela'),
    ('P5', 'lect. dr. State Mihaela'),
    ('P6', 'conf. dr. Lupan Mariana'),
    ('P7', 'conf. dr. Socaciu Tiberiu'),
    ('P8', 'lect. dr. ing. Sfichi Ștefan'),
    ('P9', 'as. dr. Cosmulese Gabriela'),
    ('P10', 'lect. dr. Bores Ana-Maria'),
    ('P11', 'lect. dr. Grigoraș-Ichim Claudia'),
    ('P12', 'conf. dr. Boghean Florin'),
    ('P13', 'lect. dr. Vlad Mariana'),
    ('P14', 'drd. Melega Anatol'),
    ('P15', 'lect. dr. Ciubotariu Marius'),
    ('P16', 'drd. Brînzaru Simona'),
    ('P17', 'conf. dr. Tulvinschi Mihaela'),
    ('P18', 'conf. dr. Kicsi Rozalia'),
    ('P19', 'conf. dr. Mihalciuc Camelia'),
    ('P20', 'conf. dr. Vancea Romulus'),
    ('P21', 'lect. dr. Hurjui Marcela'),
    ('P22', 'conf. dr. Băeșu Camelia'),
    ('P23', 'lect. dr. Colomeischi Tudor'),
    ('P24', 'lect. dr. Macovei Anamaria'),
    ('P25', 'dr. Ilaș Constantin'),
    ('P26', 'as. drd. colab. Scheuleac Adelina'),
    ('P27', 'lect. dr. Ichim Cristinel'),
    ('P28', 'conf. dr. Cibotaru Irina'),
    ('P29', 'lect. dr. Pașcu Paul'),
    ('P30', 'lect. dr. Cioban Gabriela-Liliana'),
    ('P31', 'as. dr. Danileț Alexandra'),
    ('P32', 'drd. Anichiti Alexandru'),
    ('P33', 'lect. dr. Bejinaru Ruxandra'),
]

courses_data = [
    ('IE321', 'Proiectarea sistemelor informatice', 'P1', 'P1', 'L', 'IE3', 'PSI'),
    ('IE322', 'Strategii investiţionale în afaceri', 'P6', 'P4', 'S', 'IE3', 'INVEST'),
    ('IE323', 'Statistică macroeconomică', 'P5', 'P5', 'S', 'IE3', 'Stat macro'),
    ('IE324', 'Dispozitive şi aplicaţii mobile', 'P3', 'P3', 'L', 'IE3', 'Disp apl mob'),
    ('IE325', 'Securitatea sistemelor informatice', 'P7', 'P7', 'L', 'IE3', 'Sec sist inform'),
    ('IE326', 'Geopolitică', 'P2', 'P2', 'S', 'IE3', 'Geopol'),
    ('IE327', 'Grafică și programare pe internet', 'P8', 'P8', 'L', 'IE3', 'Gr prg Int'),
    ('IE328', 'Educaţie fizică şi sport', 'P26', 'P26', 'OL', 'IE3', 'EDF'),
    ('FB321', 'Comunicare și raportare financiară', 'P11', 'P11', 'S', 'FB3', 'Com rap fin'),
    ('FB322', 'Instituții financiar-bancare internaționale', 'P9', 'P9', 'S', 'FB3', 'Inst fin b inte'),
    ('FB323', 'Gestiune bancară', 'P13', 'P13', 'S', 'FB3', 'Gest banc'),
    ('FB324', 'Audit financiar', 'P10', 'P10', 'S', 'FB3', 'Aud fin'),
    ('FB325', 'Fiscalitate', 'P17', 'P16', 'S', 'FB3', 'Fisc'),
    ('FB326', 'Controlling', 'P12', 'P15', 'S', 'FB3', 'CTRL'),
    ('FB327', 'Analiză financiară', 'P9', 'P9', 'S', 'FB3', 'Anal fin'),
    ('AF321', 'Tranzacții și tehnici comerciale', 'P18', 'P31', 'S', 'AF3', 'TrTehnCom'),
    ('AF322', 'Fiscalitate', 'P17', 'P16', 'S', 'AF3', 'Fisc'),
    ('AF323', 'Contabilitate managerială', 'P19', 'P14', 'S', 'AF3', 'CtMng'),
    ('AF324', 'Managementul producției', 'P21', 'P21', 'S', 'AF3', 'Mng prod'),
    ('AF325', 'Baze de date', 'P3', 'P29', 'L', 'AF3', 'BzDt'),
    ('AF326', 'Tehnica negocierilor în afaceri', 'P9', 'P20', 'S', 'AF3', 'Tehn neg af'),
    ('AF327', 'Contabilitatea grupurilor de societăți', 'P13', 'P13', 'S', 'AF3', 'Contab grup'),
    ('AI321', 'Geopolitică', 'P2', 'P2', 'S', 'AI3', 'Geopol'),
    ('AI322', 'Negocieri în afaceri internaționale', 'P22', 'P4', 'S', 'AI3', 'NegAI'),
    ('AI323', 'Investiții internaționale', 'P6', 'P21', 'S', 'AI3', 'Invest int'),
    ('AI324', 'Burse internaționale de mărfuri', 'P4', 'P4', 'S', 'AI3', 'Burse'),
    ('AI325', 'Gestiunea riscului în economia globală', 'P5', 'P5', 'S', 'AI3', 'Gest risc'),
    ('AI326', 'Asigurări internaționale', 'P18', 'P30', 'S', 'AI3', 'Asig int'),
    ('IE221', 'Probabilități și statistică matematică', 'P23', 'P23', 'S', 'IE2', 'Pr st mat'),
    ('IE222', 'Multimedia', 'P8', 'P8', 'L', 'IE2', 'Multim'),
    ('IE223', 'Programare orientată pe obiect', 'P7', 'P7', 'L', 'IE2', 'POO'),
    ('IE224', 'Cercetări operaționale', 'P24', 'P24', 'L', 'IE2', 'C op'),
    ('IE225', 'Limba engleză', 'P25', 'P25', 'OS', 'IE2', 'Pb eng'),
    ('IE226', 'Educaţie fizică şi sport', 'P26', 'P26', 'OL', 'IE2', 'EDF'),
    ('IE227', 'Programarea aplicaţiilor Windows', 'P8', 'P8', 'L', 'IE2', 'Pr Wind'),
    ('FB221', 'Contabilitate manageriala', 'P19', 'P14', 'S', 'FB2', 'CtMang'),
    ('FB222', 'Contabilitate bancară', 'P13', 'P13', 'S', 'FB2', 'Cont Banc'),
    ('FB223', 'Finanțe publice', 'P27', 'P14', 'S', 'FB2', 'FinP'),
    ('FB224', 'Econometrie', 'P24', 'P32', 'L', 'FB2', 'Ec.metrie'),
    ('FB225', 'Finanțe personale', 'P10', 'P10', 'S', 'FB2','Fin pers'),
    ('FB226', 'Finanţe corporative', 'P28', 'P28', 'S', 'FB2', 'Fin corp'),
    ('FB227', 'Educaţie fizică şi sport', 'P26', 'P26', 'OL', 'IE2', 'EDF')
    # ('AF221', 'Tranzacții și tehnici comerciale', 'P18', 'P31', 'S', 'AF2', 'TrTehnCom'),
    # ('AF222', 'Fiscalitate', 'P17', 'P16', 'S', 'AF2', 'Fisc'),
    # ('AF223', 'Contabilitate managerială', 'P19', 'P14', 'S', 'AF2', 'CtMng'),
    # ('AF224', 'Managementul producției', 'P21', 'P21', 'S', 'AF2', 'Mng prod'),
    # ('AF225', 'Baze de date', 'P3', 'P29', 'L', 'AF2', 'BzDt'),
    # ('AF226', 'Tehnica negocierilor în afaceri', 'P9', 'P20', 'S', 'AF2', 'Tehn neg af'),
    # ('AF227', 'Contabilitatea grupurilor de societăți', 'P13', 'P13', 'S', 'AF2', 'Contab grup'),
    # ('AF228', 'Marketing internațional', 'P33', 'P33', 'S', 'AF2', 'MK internaț'),
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
    ('AF3L1', 'AF3', 14),
    ('AF3L2', 'AF3', 12),
    ('AF3L3', 'AF3', 13),
    ('AF3L4', 'AF3', 13),
    ('AF3L5', 'AF3', 17),
    ('AI3L1', 'AI3', 15),
    ('AI3L2', 'AI3', 14),
    ('IE2L1', 'IE2', 13),
    ('IE2L2', 'IE2', 13),
    ('IE2L3', 'IE2', 13),
    ('IE2L4', 'IE2', 13),
    ('FB2L1', 'FB2', 13),
    ('FB2L2', 'FB2', 13),
    ('FB2L3', 'FB2', 14),
    ('FB2L4', 'FB2', 13),
    ('FB2L5', 'FB2', 14),
]

rooms_data = [
    ('R1', 'E001', 70),
    ('R2', 'E002', 55),
    ('R3', 'E003', 40),
    ('R4', 'E004', 30),
    ('R5', 'E005', 60),
    ('R6', 'E006', 75),
    ('R7', 'E007', 60),
    ('R8', 'E008', 70),
    ('R9', 'E009', 55),
    ('R10', 'E010', 40),
    ('R11', 'E101', 30),
    ('R12', 'E102', 60),
    ('R13', 'E103', 75),
    ('R14', 'E104', 60),
    # ('R15', 'E105', 60),
    # ('R16', 'E106', 75),
    # ('R17', 'E107', 70),
    # ('R18', 'E108', 55),
    # ('R19', 'E109', 40),
    # ('R20', 'E110', 50),
    # ('R21', 'E201', 30),
    # ('R22', 'E202', 60),
    # ('R23', 'E203', 75),
    # ('R24', 'E204', 60),
    # ('R25', 'E205', 60),
    # ('R26', 'E206', 75),
    # ('R27', 'E207', 70),
    # ('R28', 'E208', 55),
    # ('R29', 'E209', 40),
    # ('R30', 'E210', 50),
]

study_programs_data = [
    ('IE3', 40),
    ('FB3', 67),
    ('AF3', 33),
    ('AI3', 29),
    ('IE2', 52),
    ('FB2', 55),
]

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

c.executemany("INSERT INTO Professors VALUES (?, ?)", professors_data)
c.executemany("INSERT INTO Rooms VALUES (?, ?, ?)", rooms_data)
c.executemany("INSERT INTO Study_Programs VALUES (?, ?)", study_programs_data)
c.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?, ?, ?, ?)", courses_data)
c.executemany("INSERT INTO Groups_Structure VALUES (?, ?, ?)", groups_structure_data)
c.executemany("INSERT INTO Subgroups_Structure VALUES (?, ?, ?)", subgroups_structure_data)
c.executemany("INSERT INTO TimeSlots VALUES (?, ?, ?)", time_slots_data)
c.executemany("INSERT INTO Days VALUES (?, ?)", days_data)

conn.commit()
conn.close()

print("Database populated successfully.")