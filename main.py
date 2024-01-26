from flask import Flask, render_template, flash, redirect, request, url_for
from sqlalchemy import UniqueConstraint
import sqlalchemy.dialects.sqlite as sqlite
from collections import Counter
import pandas as pd
import tabula
import re
from sqlalchemy import or_
import sqlalchemy
from sqlalchemy import delete, select, String, Integer, Column, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.orm import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MuthuPalaniyappanOL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

engine = sqlalchemy.create_engine('sqlite:///database.db')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


DeclarativeBase = declarative_base()

class Student(DeclarativeBase):
    __tablename__ = 'student'

    roll_number = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    joined_year = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Student(roll_number={self.roll_number}, name={self.name})"

    def __str__(self):
        return f"Student(roll_number={self.roll_number}, name={self.name})"


class Course(DeclarativeBase):
    __tablename__ = 'course'

    course_id = Column(String(10), primary_key=True)

    def __repr__(self) -> str:
        return f"Course(course_id={self.course_id})"

class StudentCourse(DeclarativeBase):
    __tablename__ = 'student_course'

    id = Column(Integer, primary_key=True)
    
    course_id = Column(String(10), ForeignKey('course.course_id'), nullable=False)
    roll_number = Column(Integer, ForeignKey('student.roll_number'), nullable=False)
    grade = Column(String(1), nullable=False)
    graded_year = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    updated_grade = Column(String(1), nullable=True)
    updated_graded_year = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint('course_id', 'roll_number', name='_course_roll_number_uc'),)

    def __repr__(self) -> str:
        return f"StudentCourse(roll_number={self.roll_number}, course_id={self.course_id}, graded_year={self.graded_year}, grade={self.grade})"

@app.route('/', methods=['POST', 'GET'])
def home():
    years = session.query(Student.joined_year).distinct().all()
    subjects = session.query(Course.course_id).distinct().all()
    
    selected_year = request.form.get('year')
    selected_year = '' if selected_year == None or selected_year == '' else int(selected_year)
    search_flag = request.form.get('search_flag')

    if selected_year != '':
        
        # Get names
        names = session.query(Student).where(Student.joined_year == int(selected_year)).all()
        names_map = {}
        for n in names:
            names_map[n.roll_number] = n.name

        # Get Data
        data = session.query(StudentCourse).join(Student, StudentCourse.roll_number == Student.roll_number).filter(Student.joined_year == int(selected_year)).all()
        m = {}
        for d in data:
            if d.roll_number not in m:
                m[d.roll_number] = []
            
            m[d.roll_number].append(d)
        
        for v in m:
            m[v] = sorted(m[v], key=lambda d:d.graded_year)

        if search_flag != '' and search_flag != '0.5':
            flag = int(search_flag)
            for v in m:
                m[v] = [sc for sc in m[v] if sc.status == flag]
            m = {v : m[v] for v in m if len(m[v]) > 0}

        if search_flag == '0.5':
            for v in m:
                m[v] = [sc for sc in m[v] if sc.status == 0 or sc.status == 1]
            m = {v : m[v] for v in m if len(m[v]) > 0}
        
        return render_template('home.html', title='Home', years=years, subjects=subjects, selected_year=selected_year, m=list(enumerate(sorted(list(m.items()), key=lambda x: x[0]), start=1)), names_map=names_map, search_flag=search_flag)

    
    return render_template('home.html', title='Home', years=years, subjects=subjects, selected_year=selected_year)

@app.get('/database')
def database():
    return render_template('database.html', title='Database')

grade_convertor = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'C': 5,
    'RA': 0,
    'U': 0,
    'SA': 0,
    '-': 0
}

def process_pdf(file):
    def process_df(df):
        for i in range(0, len(df) - 1):
            df[i].columns = df[i].iloc[0]
            df[i] = df[i][1:]
        df = pd.concat([df[i] for i in range(0, len(df) - 1)])
        df = df.drop(columns=['GPA', 'S.No.'])
        return df.groupby(['Register No.']).agg(lambda x: x.dropna().iloc[0] if x.notna().any() else None).reset_index()
    
    def find_year(df):
        year_counter = Counter([int(r[:4]) for r in df['Register No.'].to_list()])
        return max(year_counter, key=year_counter.get)
    
    df = tabula.read_pdf(file, pages='all',lattice=True)
    semester = int(re.search(r'Semester\s*:\s*(\d+)', df[0].columns[0]).group(1))
    current_year = int(re.search(r'[A-Za-z]*\s*\-\s*([0-9]{4})', df[0].columns[0]).group(1))
    df = process_df(df)
    year = find_year(df)

    for i in range(len(df)):
        insert_statement = sqlite.insert(Student).values(roll_number=int(df.iloc[i][0]), name=df.iloc[i][1], joined_year=int(df.iloc[i][0][:4]))
        insert_statement = insert_statement.on_conflict_do_nothing(index_elements=["roll_number"])
        conn.execute(insert_statement)
    
    for c in df.columns[2:]:
        insert_statement = sqlite.insert(Course).values(course_id=c)
        insert_statement = insert_statement.on_conflict_do_nothing(index_elements=["course_id"])
        conn.execute(insert_statement)
    
    for course_i, c in enumerate(df.columns[2:]):
        for student_i in range(len(df)):
            if df.iloc[student_i][course_i + 2] is not None:
                students_in_db = [StudentCourse(**row._asdict()) for row in conn.execute(select(StudentCourse).where((StudentCourse.roll_number == df.iloc[student_i][0]) & (StudentCourse.course_id == c))).fetchall()]

                # New Student Detail
                if len(students_in_db) == 0:
                        conn.execute(sqlite.insert(StudentCourse).values(course_id=c, roll_number=int(df.iloc[student_i][0]), grade=df.iloc[student_i][course_i + 2], graded_year=current_year, status=(0 if df.iloc[student_i][course_i + 2] in ['O', 'A+', 'A', 'B+', 'B'] else 2)))
                else:
                    if students_in_db[0].graded_year < current_year:
                        print('Update ' + str(students_in_db[0].roll_number) + ' ' + students_in_db[0].course_id)
                        conn.execute(update(StudentCourse).values(updated_grade=df.iloc[student_i][course_i + 2], updated_graded_year=current_year, status=1).where((StudentCourse.roll_number==int(df.iloc[student_i][0])) & (StudentCourse.course_id==c)))

                    if students_in_db[0].graded_year > current_year:
                        print('Reverse Update ' + str(students_in_db[0].roll_number) + ' ' + students_in_db[0].course_id)
                        conn.execute(update(StudentCourse).values(grade=df.iloc[student_i][course_i + 2], graded_year=current_year, updated_grade=students_in_db[0].grade, updated_graded_year=students_in_db[0].graded_year, status=1).where((StudentCourse.roll_number==int(df.iloc[student_i][0])) & (StudentCourse.course_id==c)))
                
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #                                          OLD PLAN                                       #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # if len(students_in_db) == 0:

                #     # Reappearing Student
                #     if int(df.iloc[student_i][0][:4]) < year:
                #         insert_statement = sqlite.insert(StudentCourse).values(course_id=c, roll_number=int(df.iloc[student_i][0]), grade='', graded_year=0, updated_grade=df.iloc[student_i][course_i + 2], updated_graded_year=current_year)
                #         conn.execute(insert_statement)
                    
                #     # Straight Result
                #     else:
                #         insert_statement = sqlite.insert(StudentCourse).values(course_id=c, roll_number=int(df.iloc[student_i][0]), grade=df.iloc[student_i][course_i + 2], graded_year=current_year)
                #         conn.execute(insert_statement)

                # else:
                    
                #     if students_in_db[0].graded_year == 0 and students_in_db[0].updated_graded_year == year:
                #         conn.execute(update(StudentCourse).values(grade=df.iloc[student_i][course_i + 2], graded_year=year).where((StudentCourse.roll_number==int(df.iloc[student_i][0])) & (StudentCourse.course_id==c)))
                #     else:
                #         conn.execute(update(StudentCourse).values(updated_grade=df.iloc[student_i][course_i + 2], updated_graded_year=year).where((StudentCourse.roll_number==int(df.iloc[student_i][0])) & (StudentCourse.course_id==c)))
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    conn.commit()

@app.route('/profile')
def profile():
    roll_number = int(request.args.get('roll_number'))
    student = session.query(Student).filter_by(roll_number=roll_number).first()
    if student is None:
        return render_template('error.html', error='No Such Student')
    student_courses_data = session.query(StudentCourse).filter(StudentCourse.roll_number == roll_number).all()
    data = sorted([{'year': student.graded_year, 'course': student.course_id, 'status': student.status, 'grade': student.grade} for student in student_courses_data], key=lambda b:b['year'])
    failed_data = sorted(list(filter(lambda s:s.status == 2 or s.status == 1, student_courses_data)), key=lambda b:b.graded_year)
    return render_template('profile.html', name=student.name, roll_number=student.roll_number, title=student.name, data=data, failed_data=failed_data)

@app.route('/execute')
def execute():
    return render_template('execute.html', title='Execute')

@app.post('/upload')
def upload_file():

    files = request.files.getlist('file')

    if len(files) == 0:
        flash('No File was uploaded', 'upload')
        return redirect(url_for('database'))

    for f in files:
        process_pdf(f)
    
    return redirect(url_for('database'))

if __name__ == '__main__':
    Student().metadata.create_all(bind=engine)
    Course().metadata.create_all(bind=engine)
    StudentCourse().metadata.create_all(bind=engine)

    app.run(debug=True)