from flask import Flask,jsonify,request
import pymysql
import os
from flask_cors import CORS  # <--- ថែមជួរនេះ


app = Flask(__name__)
CORS(app)  # <--- ថែមជួរនេះ (វានឹងអនុញ្ញាតឱ្យគ្រប់វេបសាយទាញទិន្នន័យបាន)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def db_connection():
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'), # GitHub នឹងលែងចាប់ Error ទៀតហើយ
        db=os.environ.get('DB_NAME'),
        port=int(os.environ.get('DB_PORT', 23122)),
        ssl={'ssl': {}}, # ចាំបាច់សម្រាប់ Aiven
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route("/getuser")
def get_user():
    conection = db_connection()
    cursor = conection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return jsonify(users)

@app.route('/adduser',methods=['POST'])
def adduser ():
    conection = db_connection()
    cursor = conection.cursor()

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']
    image = request.files.get('image')

    filename=""
    if image:
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

    sql = ("INSERT INTO users (name,age,gender,salary,image) values(%s,%s,%s,%s,%s)")
    cursor.execute(sql,(name,age,gender,salary,filename))
    conection.commit()
    return jsonify("insert into database success !")


@app.route('/updateuser/<int:id>',methods=['POST','PUT'])
def update_user(id):
    conection = db_connection()
    cursor = conection.cursor()

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']
    image = request.files.get('image')


    filename=""
    if image:
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        sql = "UPDATE users SET name=%s ,age=%s,gender=%s,salary=%s,image=%s WHERE id = %s"
        cursor.execute(sql,(name,age,gender,salary,filename,id))

    else:
        sql = "UPDATE users SET name=%s ,age=%s,gender=%s,salary=%s WHERE id = %s"
        cursor.execute(sql,(name,age,gender,salary,id))

    conection.commit()

    return jsonify("update user successfully !")    

@app.route('/deleteuser/<int:id>',methods=['DELETE','POST'])
def delete_user(id):
    conection = db_connection()
    cursor = conection.cursor()


    sql = ("DELETE FROM users WHERE id=%s")
    cursor.execute(sql,(id))

    conection.commit()
    return jsonify("delete successfully !")





    





    

if __name__=="__main__":
    print("server is running 🤣")
    app.run(debug=True)


