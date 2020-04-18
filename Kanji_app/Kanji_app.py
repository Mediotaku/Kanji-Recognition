#render_templates to manage HTML files and session to store a value between request
from flask import Flask, render_template, request, redirect, session
import pymysql
import yaml
import cv2
import os
import numpy as np
from PIL import Image
import base64
import json
# generate random integer values
from random import seed
from random import randint
#Set an int as seed
seed(7)

#Configure db
db = yaml.load(open('db.yaml'))
mysql = pymysql.connect(host=db['mysql_host'],
                       user=db['mysql_user'],
                       password=db['mysql_password'],
                       db=db['mysql_db'],
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Load character JSON with all the classes to ask for
with open('CharacterJSON.json', encoding="utf8") as f:
    classes = json.load(f)
#Create an entry in table classes if doesn't exist yet
cur = mysql.cursor()

for name in classes["character"]:
    cur.execute("SELECT number FROM classes WHERE name=%s",name)
    result = cur.rowcount
    if result==0:
        cur.execute("INSERT INTO classes(name,number) VALUES(%s, %s)",(name, 0))
        mysql.commit()

cur.close()

#__name__ is the current module, identified with two underscores
app = Flask(__name__) 
app.secret_key = 'You Will Never Guess'
@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'GET':      
        #Now we look for the classes with lowest number to ask for it
        #If we find multiple with the same number, choose random one
        cur = mysql.cursor()
        cur.execute("SELECT * FROM classes WHERE number = ( SELECT MIN(number) FROM classes )")
        resultnumber = cur.rowcount
        result = cur.fetchall()
        print(result)
        if resultnumber != 1:      
            value = randint(0, resultnumber-1)
            session['character'] = result[value]["name"]
        else:
            session['character'] = result[0]["name"]
        mysql.commit()
        cur.close()

        flag="notsent"
        return render_template('index.html', character=session['character'], postedwindow=flag)


    #print(session['character'])
    if request.method == 'POST':
        #Fetch form data
        data_url = request.values['imgcanvas']
        #We have to parse something like this:
        #"data:image/png;base64,iVBORw0KGgoAAAANSUhE..."
        content = data_url.split(';')[1]
        image_encoded = content.split(',')[1]
        body = base64.decodebytes(image_encoded.encode('utf-8'))
        #Save temp image for comparing

        #Using Python 3.x syntax to save into file
        #wb means writing in binary mode, like images or .exe
        #wt or w would write in text mode, like for plain text or text-based formats like CSV
        with open("./static/temp.png", "wb") as fh: 
            fh.write(body)
            fh.close()

        #Fill png transparent with white to support small kana
        image = cv2.imread('./static/temp.png', cv2.IMREAD_UNCHANGED)
        trans_mask = image[:,:,3] == 0
        image[trans_mask] = [255, 255, 255, 255]
        temp = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        #Erase lightgrey grid lines
        mask = cv2.inRange(temp, np.array([211,211,211]), np.array([211,211,211]))
        temp[mask!=0] = (255,255,255)
        temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2BGR)

        #Check if canvas is not empty with OpenCV
        equal = 1
        default = cv2.imread("./static/default.png")
        if temp.shape == default.shape:
            difference = cv2.subtract(default, temp)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                equal = 0

        flag="noimage"
        if equal == 1:
            #Now we should process the image to MNIST format using OpenCV
            dim = (28, 28) 
            #INTER_AREA is the recommended interpolation method for shrinking 
            temp = cv2.resize(temp, dim, interpolation = cv2.INTER_AREA) 

            #Create filename and store in database along form data
            cur = mysql.cursor()
            character = session['character']
            cur.execute("SELECT number FROM classes WHERE name=%s",character)
            result = cur.fetchone()
            result = result["number"]
            filename = "./test_filesystem/" + session['character'] +"_"+ str(result) + ".png"
            #print(filename)

            #Save image in filesystem
            #We have to use this method to avoid that OpenCV imwrite only allow
            #ascii characters in filename, splitext returns a pair (root, ext),
            #this way we obtain the file extension for imencode
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, temp, None)
            with open(filename, "wb") as f:
                n.tofile(f)


            #Save into database, first we increment the counter in classes and then we insert in dataset
            cur.execute("UPDATE classes SET number=number+1 WHERE name=%s",character)
            country = request.values['country']
            language = request.values['language']
            inputype = request.values['input']

            cur.execute("INSERT INTO dataset(name,imageurl,country,language,type) VALUES(%s, %s,%s, %s, %s)",(character, filename, country, language, inputype))

            mysql.commit()
            cur.close()

            #Now we look for the classes with lowest number to ask for it
            #If we find multiple with the same number, choose random one
            cur = mysql.cursor()
            cur.execute("SELECT * FROM classes WHERE number = ( SELECT MIN(number) FROM classes )")
            resultnumber = cur.rowcount
            result = cur.fetchall()
            #print(resultnumber, result)
            if resultnumber != 1:      
                value = randint(0, resultnumber-1)
                session['character'] = result[value]["name"]
            else:
                session['character'] = result[0]["name"]
            mysql.commit()
            cur.close()
            #On post success, flag is sent
            flag="sent"
        
        return render_template('index.html', character=session['character'], postedwindow=flag)
    
    return render_template('index.html', character=session['character'])
'''
@app.route('/users')
def users():
    cur = mysql.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)
'''
if __name__== '__main__': 
    #debug=True to update server changes without restarting
    app.run(debug=False) 