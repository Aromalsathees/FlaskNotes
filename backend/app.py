from flask import Flask,request,jsonify, render_template,redirect,session
from models import db,User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# above are configutions 

@app.route('/signup')
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        user = User(username=username ,password=hashed_password,email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    
    return render_template('signup.html')

@app.route('/login')
def login():

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            session['user_id'] = user.id
            return redirect('home')

    return render_template('login.html')

# # home page url and views starts here
# @app.route('/')
# def home():
#     return jsonify({
#         'message':'flask restapi is working'
#     })

# # Get all students url and views starts here
# @app.route('/get_students',methods=['GET'])
# def get_students():

#     students = Student.query.all()

#     student_list = []
#     for student in students:
#         student_list.append(student.to_dict())

#     return jsonify(student_list)
  
# # Get a sinngle student url and views starts here
# @app.route('/single_student/<int:id>/', methods=['GET'])
# def get_single_student(id):

#     single_student = Student.query.get(id)
   
#     if not single_student:
#         return jsonify({
#             'message':'student not found'
#         }), 404
#     return jsonify({
#         'message':'here is the student',
#         'student':single_student.to_dict()}
#         )

# # post student url and views starts here
# @app.route('/add_students' , methods=['POST'])
# def add_students():

#     # recive json data
#     data = request.get_json()  
#     # create object
#     new_student = Student(
#         name=data['name'],
#         course=data['course']
#     )
#     db.session.add(new_student)
#     db.session.commit()

#     return jsonify({
#         'message':'student data added successfully',
#         'student':new_student.to_dict()
#     }),201

# # delete student url and views starts here
# @app.route('/delete_student/<int:id>/' , methods=['DELETE'])
# def remove_student(id):
#     student = Student.query.get(id)
#     if not student:
#         return jsonify({
#             'message':'The student Does Not Exist'
#         })
#     db.session.delete(student)
#     db.session.commit()
#     return jsonify({
#         'message':'The student is deleted from database'
#     }),200

# # update student url and views starts here
# @app.route('/update_student/<int:id>/',methods=['PUT'])
# def alter_data(id):
#     student = Student.query.get(id)
#     data = request.get_json()

#     student.name = data['name']
#     student.course = data['course']
#     db.session.commit()

#     return jsonify({
#         'message':'Data succesfully updated'
#     })


# below are configutions 
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)  

if __name__ == '__main__':
    app.run(debug=True)