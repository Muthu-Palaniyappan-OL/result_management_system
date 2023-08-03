CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_number TEXT NOT NULL,
    student_name TEXT NOT NULL
);

CREATE TABLE gpa (
    student_id INTEGER NOT NULL,
    student_semester INTEGER NOT NULL,
    gpa REAL NOT NULL,
    UNIQUE(student_id, student_semester)
);

CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    subject_semester INTEGER NOT NULL
);

CREATE TABLE student_subject (
    student_id INTEGER NOT NULL,
    subject_id TEXT NOT NULL,
    grade TEXT NOT NULL,
    UNIQUE(student_id, subject_id)
);