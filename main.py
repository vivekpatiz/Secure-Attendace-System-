# main.py
import os
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
import cv2
import shutil
import PIL.Image
from PIL import Image
import datetime
import imagehash
import mysql.connector
import urllib.request
import urllib.parse

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  use_pure=True,
  database="staff_attendance "

)
app = Flask(__name__)


@app.route('/')
def index():
    shutil.copy('f1.jpg', 'faces/f1.jpg')
    shutil.copy('f2.jpg', 'faces/f2.jpg')
    shutil.copy('f3.jpg', 'faces/f3.jpg')
    shutil.copy('f4.jpg', 'faces/f4.jpg')
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    cutoff = 20
    for rows in data:
        m1="static/photo/"+str(rows[0])+".jpg"
        print(rows[0])
        i=1
        while i <= 2:
            m2="faces/f"+str(i)+".jpg"
            hash0 = imagehash.average_hash(Image.open(m1)) 
            hash1 = imagehash.average_hash(Image.open(m2)) 
            cc=hash0 - hash1
            print("s="+m2+" "+str(cc))
            i += 1
                    
        
        
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    shutil.copy('f1.jpg', 'faces/f1.jpg')
    shutil.copy('f2.jpg', 'faces/f2.jpg')
    shutil.copy('f3.jpg', 'faces/f3.jpg')
    shutil.copy('f4.jpg', 'faces/f4.jpg')
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            #session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        regno=request.form['regno']
        m1=regno+".jpg"
        shutil.copy('faces/f1.jpg', 'static/photo/'+m1)
        #mm2 = PIL.Image.open('static/photo/'+m1)
        #rz = mm2.resize((100,100), PIL.Image.ANTIALIAS)
        #rz.save('static/photo/'+m1)
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    if request.method=='GET':
        act = request.args.get('act')
        did = request.args.get('did')
        if act=="del":
            fn=did+".jpg"
            #os.remove("static/photo/"+fn)
            cursor1 = mydb.cursor()
            cursor1.execute('delete FROM student WHERE regno = %s', (did, ))
            mydb.commit()   
            return redirect(url_for('home',data=data))
    return render_template('home.html',data=data)

@app.route('/student', methods=['GET', 'POST'])
def student():
    #import student
    msg=""
    if request.method=='POST':
        name=request.form['name']
        regno=request.form['regno']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['branch']
        cursor = mydb.cursor()
        sql = "INSERT INTO student(regno,name,mobile,email,branch) VALUES (%s, %s, %s, %s, %s)"
        val = (regno,name,mobile,email,address)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('home'))
        else:
            msg='Already Exist'
    return render_template('student.html',msg=msg)

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    #regno=""
    #if request.method=='GET':
     #   regno=request.form['regno']
    regno = request.args.get('regno')
    print(regno)
    
                
    return render_template('capture.html',regno=regno)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('login.html')

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    
    act="0"
    st="1"
    cnt=0
    nn=0
    pr=0
    period=0
    cutoff=10
    lat="10.988440"
    long="78.733510"
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    cursor1 = mydb.cursor()
    cursor1.execute('select * from admin')
    data = cursor1.fetchone()
    mobile=data[3]
    if request.method=='GET':
        act = request.args.get('act')
        if act is None:
            act="0"
            
        period=int(act)
        if period>=2:
            act="0"
            st="2"
            
        if period<2:
            nn=period+1
        
            act=str(nn)
            #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
            print(rdate)
            cursor11 = mydb.cursor()
            cursor11.execute('SELECT * FROM student')
            srow = cursor11.fetchall()
            for sr in srow:
                
                regno=sr[0]
                #print(regno)
                img=str(sr[0])+".jpg"

                hash0 = imagehash.average_hash(Image.open("static/photo/"+img)) 
                hash1 = imagehash.average_hash(Image.open("faces/f1.jpg"))
                cc1=hash0 - hash1

                hash20 = imagehash.average_hash(Image.open("static/photo/"+img)) 
                hash21 = imagehash.average_hash(Image.open("faces/f2.jpg"))
                cc2=hash20 - hash21

                hash30 = imagehash.average_hash(Image.open("static/photo/"+img)) 
                hash31 = imagehash.average_hash(Image.open("faces/f3.jpg"))
                cc3=hash30 - hash31

                hash40 = imagehash.average_hash(Image.open("static/photo/"+img)) 
                hash41 = imagehash.average_hash(Image.open("faces/f4.jpg"))
                cc4=hash40 - hash41

                if cc1<=cutoff or cc2<=cutoff or cc3<=cutoff or cc4<=cutoff:
                    print(str(cc1)+" "+str(cc2))
                    
                    
                    #try:
                    cursor1 = mydb.cursor()        
                    cursor1.execute('SELECT * FROM attendance WHERE rdate=%s && regno = %s', (rdate, regno))
                    arow = cursor1.fetchall()
                    cnt=len(arow)
                    print("dd="+str(cnt))
                    
                    
                    if cnt>0:
                        
                        if arow[0][3] is None:
                            pr=10

                        pr=int(arow[0][3])
                        if pr<2:
                            print("dd="+str(pr))
                            cursor2 = mydb.cursor()
                            cursor2.execute('update attendance set attendance=attendance+1 WHERE regno = %s && rdate=%s', (regno, rdate))
                            mydb.commit()
                            
                        if pr==0:
                            cursor2 = mydb.cursor()
                            cursor2.execute('update attendance set attendance=attendance+1 WHERE regno = %s && rdate=%s', (regno, rdate))
                            mydb.commit()
                        elif pr==1:
                            cursor2 = mydb.cursor()
                            cursor2.execute('update attendance set attendance=attendance+1 WHERE regno = %s && rdate=%s', (regno, rdate))
                            mydb.commit()
                          

                            
                            
                            
                    else:
                        #print("jjjj")
                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT max(id)+1 FROM attendance")
                        maxid = mycursor.fetchone()[0]
                        if maxid is None:
                            maxid=1
                        cursor = mydb.cursor()
                        sql = "INSERT INTO attendance(id,regno,rdate, latitude,longitude,attendance) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (maxid,regno,rdate,'1',lat,long)
                        cursor.execute(sql, val)
                        mydb.commit()
                        print(val)
                        message="Today Attendance Location ,Latitude:"+lat+", Longitude:"+long
                        params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'NoTSMS', 'message':message, 'number':mobile})
                        url = "http://pay4sms.in/sendsms/?%s" % params
                        with urllib.request.urlopen(url) as f:
                            print(f.read().decode('utf-8'))  
                    #except:
                    #    print("Exception")
            
            
            
            #return redirect(url_for('monitor',act=act))
    return render_template('monitor.html', act=act, st=st)
@app.route('/map', methods=['GET', 'POST'])
def map():
    msg=""
    if 'username' in session:
        uname = session['username']
    if request.method=='GET':
        lat=request.args.get('lat')
        lon=request.args.get('lon')
    return render_template('map.html',msg=msg, lat=lat, lon=lon)

@app.route('/update', methods=['GET', 'POST'])
def update():
    msg=""
    cursor1 = mydb.cursor()
    cursor1.execute('select * from admin')
    data = cursor1.fetchone()
        
    if request.method=='POST':
        mob=request.form['mobile']
        cursor1 = mydb.cursor()
        cursor1.execute('update admin set mobile=%s', (mob, ))
        mydb.commit()
        msg="update success"
        return redirect(url_for('update',msg=msg))
    return render_template('add_mobile.html',msg=msg, data=data)

@app.route('/report', methods=['GET', 'POST'])
def report():
    pp=""
    data = []
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    if request.method=='POST':
        rdate=request.form['rdate']
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT * FROM attendance WHERE rdate=%s', (rdate, ))
        data = cursor1.fetchall()
        print(data)
        #return redirect(url_for('report',data=data, rdate=rdate))
    if request.method=='GET':
        act = request.args.get('act')
        did = request.args.get('did')
        if act=="del":
            
            cursor1 = mydb.cursor()
            cursor1.execute('delete FROM attendance WHERE id = %s', (did, ))
            mydb.commit()   
            #return redirect(url_for('report',rdate=rdate))
        pp = request.args.get('pp')

    return render_template('report.html',data=data, rdate=rdate)



@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    
    if request.method=='POST':
        staff=request.form['id']
        report=request.form['compl']
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        cursor1 = mydb.cursor()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM report")
        maxid = mycursor.fetchone()[0]
        sql=" insert into report(id,sid,report,rdate) values(%s,%s,%s,%s)"
        val=(maxid,staff,report,rdate)
        cursor1.execute(sql,val)
        mydb.commit()
        msg="success"
        return redirect(url_for('login',msg=msg))
    return render_template('complaint.html')



@app.route('/complaint_view', methods=['GET', 'POST'])
def complaint_view():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM report")
    data = mycursor.fetchall()
    return render_template('complaint_view.html',data=data)

def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
        

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
