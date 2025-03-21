import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="988987",
            database="flask_db"
        )
        return connection

    except Error as e:
        print(f"Error:{e}")
        return None

@app.route('/')
def collegeAdmin():
    return render_template('collegeAdmin.html')

@app.route('/subject', methods=['POST', 'GET'])
def subject():
    if request.method == 'POST':
        sub_id = request.form.get('sub_id')
        sub_name = request.form.get('sub_name')
        credit = request.form.get('credit')

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute('''INSERT INTO subjects_information(subject_id,subject_name,credits) VALUES (%s,%s,%s)''',
                               (sub_id, sub_name, credit))

                connection.commit()

                return render_template('subject.html', message="Registration successfull")
            except Error as e:

                return render_template('subject.html', message=f"Error:{e}")
            finally:
                cursor.close()
                connection.close()
        else:
            return render_template('subject.html', message="Successfully subject added.")

    return render_template('subject.html')


@app.route('/students_report', methods=['POST', 'GET'])
def students_report():

    if request.method == 'POST':
        firstname = request.form.get('firstname')
        secondname = request.form.get('secondname')
        dob = request.form.get('dateofbirth')
        gender = request.form.get('gender')
        course = request.form.get('course')
        phone_num = request.form.get('number')
        email = request.form.get('email')
        enrollment = request.form.get('enrollment')
        address=request.form.get('address')
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(''' INSERT INTO students_report(firstname,secondname,dob,gender,course,phone_num,email,enrollment,address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (
                    firstname, secondname, dob, gender, course, phone_num, email, enrollment,address))

                connection.commit()
                return render_template('students_report.html', message="Data inserted succesfully")

            except Error as e:

                return render_template('students_report.html', message=f"Error:{e}")
            finally:
                cursor.close()
                connection.close()
        else:
            return render_template('students_report.html', message="Data Added")

    return render_template('students_report.html')


@app.route('/update_marks', methods=['POST','GET'])
def updatemarks():

    if request.method == 'POST':
        name = request.form.get('name')
        enrollment = request.form.get('enrollment')
        dob = request.form.get('dateOfBirth')
        subject1 = request.form.get('subject1')
        subject2 = request.form.get('subject2')
        subject3 = request.form.get('subject3')
        subject4 = request.form.get('subject4')
        grade1=request.form.get('marks1')
        grade2=request.form.get('marks2')
        grade3=request.form.get('marks3')
        grade4=request.form.get('marks4')
        connection = create_connection()

        if connection:
            cursor = connection.cursor()

            try:
                cursor.execute('''INSERT INTO students_data(enrollment,name,dob,subject1,grade1,subject2,grade2,subject3,grade3,subject4,grade4) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (
                    enrollment, name, dob, subject1,grade1, subject2,grade2, subject3,grade3, subject4,grade4))

                connection.commit()

                return render_template('marks.html', message="Data inserted successfully")

            except Error as e:
                return render_template('marks.html', message=f"Error:{e}")
            finally:
                cursor.close()
                connection.close()

        else:
            return render_template('marks.html', message="Marks updated")

    return render_template('marks.html')


@app.route('/reportcard', methods=['POST', 'GET'])
def reportcard():
    if request.method == 'POST':
        enrollment = request.form['enrollment']
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    '''SELECT enrollment,name,dob,subject1,grade1,subject2,grade2,subject3,grade3,subject4,grade4 FROM students_data WHERE  enrollment=%s''', (enrollment,))

                student_data = cursor.fetchone()

                if student_data:
                    return render_template('about1.html', student=student_data)
                else:
                    return render_template('about1.html', message="No student found with this enrollment.")

            except Error as e:
                return render_template('about1.html', message=f"error:{e}")
            finally:
                cursor.close()
                connection.close()
        else:
            return render_template('about1.html', message="Error:Unable to connect")

    return render_template('about1.html')


if __name__ == '__main__':
    app.run(debug=True)
