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
    ('L1', 'Dr. Smith'),
    ('L2', 'Prof. Johnson'),
    ('L3', 'Ms. Davis'),
    ('L4', 'Dr. Happy'),
    ('L5', 'Mrs. Daria'),
    ('L6', 'Prof. Ramona-Maria'),
    ('L7', 'Dr. Tren'),
    ('L8', 'Mr. Scott'),
    ('L9', 'Prof. Anderson'),
    ('L10', 'Prof. Thompson'),
    ('L11', 'Dr. White'),
    ('L12', 'Prof. Martinez'),
    ('L13', 'Dr. Lee'),
    ('L14', 'Prof. Garcia'),
    ('L15', 'Dr. Martinez'),
    ('L16', 'Prof. Robinson'),
    ('L17', 'Dr. Harris'),
    ('L18', 'Prof. Clark'),
    ('L19', 'Dr. Lewis'),
    ('L20', 'Prof. King'),
    ('L21', 'Dr. Hill'),
    ('L22', 'Prof. Allen'),
    ('L23', 'Dr. Young'),
    ('L24', 'Prof. Phillips'),
    ('L25', 'Dr. Campbell'),
    ('L26', 'Prof. Nelson')
]

courses_data = [
    ('IE321', 'Proiectarea sistemelor informatice', 'L8', 'IE3', 'Proi sist inf'),
    ('IE322', 'Strategii investiţionale în afaceri', 'L2', 'IE3', 'Str invest în af'),
    ('IE323', 'Statistică macroeconomică', 'L3', 'IE3', 'St macr'),
    ('IE324', 'Dispozitive şi aplicaţii mobile', 'L4', 'IE3', 'Disp și apl mob'),
    # ('IE325', 'Securitatea sistemelor informatice', 'L5', 'IE3'),
    # ('IE326', 'Geopolitică', 'L6', 'IE3'),
    ('IE327', 'Grafică și programare pe internet', 'L7', 'IE3', 'Gr și prog pe int'),
    ('FB321', 'Comunicare și raportare financiară', 'L8', 'FB3', 'Com și rap fin'),
    ('FB322', 'Instituții financiar-bancare internaționale', 'L9', 'FB3', 'Inst fin-banc int'),
    ('FB323', 'Gestiune bancară', 'L10', 'FB3', 'Gest banc'),
    # ('FB324', 'Audit financiar', 'L10', 'FB3'),
    # ('FB325', 'Fiscalitate', 'L11', 'FB3'),
    # ('FB326', 'Controlling', 'L12', 'FB3'),
    ('FB327', 'Analiză financiară', 'L13', 'FB3', 'Anal fin'),
    ('AF321', 'Tranzacții și tehnici comerciale', 'L3', 'AF3', 'Tranz și tehn com'),
    ('AF322', 'Fiscalitate', 'L3', 'AF3', 'Fisc'),
    ('AF323', 'Contabilitate managerială', 'L13', 'AF3', 'Cont man'),
    ('AF324', 'Managementul producției', 'L9', 'AF3', 'Manag prod'),
    ('AF325', 'Baze de date', 'L4', 'AF3', 'Baze de date'),
    # ('AF326', 'Etică în afaceri', 'L14', 'AF3', 'Et în af'),
    # ('AF327', 'Contabilitatea grupurilor de societăți', 'L13', 'AF3', 'Cont gr de soc'),
    ('AI321', 'Geopolitică', 'L6', 'AI3', 'Geop'),
    ('AI322', 'Negocieri în afaceri internaționale', 'L8', 'AI3', 'Neg în afac intern'),
    ('AI323', 'Investiții internaționale', 'L10', 'AI3', 'Inv int'),
    ('AI324', 'Burse internaționale de mărfuri', 'L3', 'AI3', 'Burs int de mărf'),
    ('AI325', 'Gestiunea riscului în economia globală', 'L15', 'AI3', 'Gest risc în ec gen'),
    # ('AI326', 'Dezvoltare locală și regională', 'L6', 'AI3', 'Dezv loc și reg'),
    # ('AI327', 'Organizații economice internaționale', 'L16', 'AI3', 'Org ec int'),
    # ('IE221', 'Probabilități și statistică matematică', 'L17', 'IE2', 'Probab și stat matem'),
    # ('IE222', 'Multimedia', 'L7', 'IE2'),
    ('IE223', 'Programare orientată pe obiect', 'L5', 'IE2', 'Progr or pe ob'),
    # ('IE224', 'Bazele cercetărilor operaționale', 'L17', 'IE2'),
    # ('IE225', 'Comunicare în limbă străină pentru afaceri', 'L18', 'IE2'),
    ('IE226', 'Educaţie fizică şi sport', 'L19', 'IE2', 'Ed fiz'),
    # ('IE227', 'Programarea aplicaţiilor Windows', 'L7', 'IE2'),
    # ('FB221', 'Contabilitate manageriala', 'L13', 'FB2'),
    ('FB222', 'Contabilitate bancară', 'L9', 'FB2', 'Cont banc'),
    # ('FB223', 'Finanțe publice', 'L14', 'FB2'),
    ('FB224', 'Econometrie', 'L17', 'FB2', 'Econom'),
    # ('FB225', 'Finanțe personale', 'L13', 'FB2'),
    ('FB226', 'Finanţe corporative', 'L6', 'FB2', 'Fin corp'),
    # ('FB227', 'Gestiunea financiară a instituțiilor publice', 'L15', 'FB2'),
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
