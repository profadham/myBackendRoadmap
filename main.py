from flask import Flask, jsonify, request
import logging
import os
import psycopg2
from psycopg2 import sql
app = Flask(__name__)

logging.basicConfig(filename='scraper.log', level=logging.DEBUG,
format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

db_params = {
    'dbname': 'Student Management',
    'user': 'postgres',
    'password': '123Xx456Yy789Zz',
    'host': 'localhost',  
    'port': '5432'        
}

def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn

'''@app.route('/', methods=['GET'])
def test():
    return jsonify({'mes':'hello'})'''

cur_id = 0;
students = []
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT id, name, birthdate, male_flag, gpa FROM students WHERE id = %s"
    cursor.execute(select_query, (id,))
    student = cursor.fetchone()  # Fetch the first result
    if student:
        logging.info("GET a student")
        student_data = {
            "id": student[0],
            "name": student[1],
            "birthdate": student[2],
            "male_flag": student[3],
            "gpa": student[4]
        }
        return jsonify(student_data)
    return jsonify({'message':'id not found'})


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    birthdate = data.get('birthdate')
    male_flag = data.get('male_flag')
    gpa = data.get('gpa')
    if not name or not birthdate or not male_flag or gpa is None:
        return jsonify({"error": "Missing required fields"}), 400
    logging.info("POST of student with id=",id)
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO students (name, birthdate, male_flag, gpa)
    VALUES (%s, %s, %s, %s)"""
    cursor.execute(insert_query, (name, birthdate, male_flag, gpa))
    conn.commit()
    logging.info("POST a student")
    return jsonify({"message": "Student added sucessfully"})

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT id, name, birthdate, male_flag, gpa FROM students WHERE id = %s"
    delete_query = "DELETE FROM students WHERE id = %s"
    cursor.execute(select_query, (id,))
    student = cursor.fetchone()
    if student:
        logging.info("DELETE a student")
        cursor2 = conn.cursor()
        cursor2.execute(delete_query, (id,))
        conn.commit()
        student_data = {
            "id": student[0],
            "name": student[1],
            "birthdate": student[2],
            "male_flag": student[3],
            "gpa": student[4]
        }
        return jsonify(student_data)
    return jsonify({'message':'id not found'})

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    name = data.get('name')
    birthdate = data.get('birthdate')
    male_flag = data.get('male_flag')
    gpa = data.get('gpa')

    conn = get_db_connection()
    cursor = conn.cursor()

    update_query = """
        UPDATE students
        SET name = %s, birthdate = %s, male_flag = %s, gpa = %s
        WHERE id = %s
    """
    cursor.execute(update_query, (name, birthdate, male_flag, gpa, id))
    if cursor.rowcount > 0:
        logging.info("PUT a student")
        conn.commit()  
        return jsonify({"message": "Student updated successfully."})
    return jsonify({'message':'id not found'})

@app.route('/empty', methods=['DELETE'])
def empty_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM students"
    cursor.execute(query)
    conn.commit()
    logging.info("DELETE all students")
    return jsonify({"message":"your database has been emptied"})

app.run(port=8000)