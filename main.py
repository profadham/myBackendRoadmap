from flask import Flask, jsonify, request
import logging
app = Flask(__name__)

logging.basicConfig(filename='scraper.log', level=logging.DEBUG,
format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Student:
    def __init__(self, id, name, gpa):
        self.id = id
        self.name = name
        self.gpa = gpa
    def get_name(self):
        return slf.name
    def get_id(self):
        return self.id
    def get_gpa(self):
        return self.get_gpa
    def set_gpa(self, new_gpa):
        self.gpa = new_gpa
    def to_dict(self):
        return {
            "student id: ": self.id,
            "student name: ":self.name,
            "student GPA: ":self.gpa
        }


'''@app.route('/', methods=['GET'])
def test():
    return jsonify({'mes':'hello'})'''

cur_id = 0;
students = []
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    my_student = list(filter(lambda student:student.id==id, students))
    if (my_student):
        logging.info("GET of student with id=",id)
        return jsonify(my_student[0].to_dict())
    logging.info("id: ",id, " was not found")
    return jsonify({'message':'id not found'})


@app.route('/student', methods=['POST'])
def add_student():
    global cur_id
    req_data = request.get_json()
    if req_data is None:
        return jsonify({'message':'invalid data'})
    cur_id+=1
    student_name = req_data.get('name', 'Unknown')
    student_gpa = req_data.get('gpa', 0)
    new_stud = Student(cur_id,student_name,student_gpa)
    students.append(new_stud)
    logging.info("POST of student with id=",cur_id)
    return jsonify(new_stud.to_dict())

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    my_student = list(filter(lambda student:student.id==id, students))
    if (my_student):
        students.remove(my_student[0])
        logging.info("DELETE of student with id=",id)
        return jsonify(my_student[0].to_dict())
    logging.info("id: ",id, " was not found")
    return jsonify({'message':'id not found'})

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    req_data = request.get_json()
    my_student = list(filter(lambda student:student.id==id, students))
    if (my_student):
        students.remove(my_student[0])
        my_student[0].set_gpa(req_data.get('gpa', 0.0))
        students.append(my_student[0])
        logging.info("PUT of student with id=",id)
        return jsonify(my_student[0].to_dict())
    logging.info("id: ",id, " was not found")
    return jsonify({'message':'id not found'})

app.run(port=8000)