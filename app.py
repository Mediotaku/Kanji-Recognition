#render_templates to manage HTML files
from flask import Flask, render_template, request, redirect
import pymysql
import yaml

#Configure db
db = yaml.load(open('db.yaml'))
mysql = pymysql.connect(host=db['mysql_host'],
                       user=db['mysql_user'],
                       password=db['mysql_password'],
                       db=db['mysql_db'],
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#__name__ is the current module, identified with two underscores
app = Flask(__name__) 

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        #Enter data into the db
        cur = mysql.cursor()
        cur.execute("INSERT INTO users(name,email) VALUES(%s, %s)",(name, email))
        mysql.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)

if __name__== '__main__': 
    #debug=True to update server changes without restarting
    app.run(debug=True) 