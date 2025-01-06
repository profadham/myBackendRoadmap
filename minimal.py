from flask import Flask, jsonify, request
app = Flask(__name__)

students = [{'id':'001', 'name':'Adham'},{'id':'002', 'name':'Yasser'}]

@app.route('/', methods=['GET'])
def test():
    return jsonify({'mes':'hello'})

@app.route('/student/<string:id>', methods=['GET']) #for read
def get_student(id):
    for student in students:
        if (student['id']==id):
            return jsonify(student['name'])
    return jsonify({'message':'id not found'})


@app.route('/student', methods=['POST'])  #for create
def add_student():
    req_data = request.get_json()
    new_stud = {
        'id':req_data['id'],
        'name':req_data['name']
    }
    students.append(new_stud)
    return jsonify(new_stud)

@app.route('/student/<string:id>', methods=['DELETE'])  #for delete
def delete_student(id):
    i = 0
    deleted = False;
    for student in students:
        if (student['id']==id):
            students.pop(i)
            return jsonify({'message':'deleted successfully'})
        i+=1
    return jsonify({'message':'id not found'})

'''@app.route('/student/<string:id>', methods=['PATCH'])  #for update (updates name of a certain id)
def update_student(id):
    req_data = request.get_json()
    updated = False;
    for student in students:
        if (student['id']==id):
            studen.update(req_data)
            return jsonify({'message':'updated successfully'})
    return jsonify({'message':'id not found'})'''

@app.route('/student/<int:idx>', methods=['PUT']) #for update (updates student in a certain index in the table)
def update_student(idx):
    if idx < len(students):
        req_data = request.get_json()
        students[idx] = req_data
        return jsonify({'message':'updated successfully'})    
    return jsonify({'message':'id not found'})

app.run(port=8000)
