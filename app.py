from flask import Flask,render_template,url_for,request,redirect,session,g,flash
from flask_mysqldb import MySQL
from operator import itemgetter
import MySQLdb.cursors
import yaml
import os
from datetime import datetime
import random
import bcrypt

app=Flask(__name__)

app.secret_key =os.urandom(24)
#configuring the mysql db

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'Iruntheworld1'
app.config['MYSQL_DB']= 'utagdb'

mysql=MySQL(app)
#--------------------------------------------------------
#--------------HOME PAGE---------------------------------
#--------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/signin',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def logIn():
    msg=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        staffId=request.form['staffId']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM lecturer WHERE email = %s AND staffId=%s', (email,staffId))
        account = cur.fetchone()
        
        cur.close()
        if account:
            hashedPassword=account['hashedPassword']
            if bcrypt.checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8')):
                session['type']='lecturer'
                session['loggedIn'] = True
                session['id'] = account['idLecturer']
                session['email'] = account['email']
                session['surname']=account['surname']
                session['verifiedMail']=account['verifiedMail']
                nameOfUser=session['surname']
                return redirect('/dashboard')
            else:'Password is Incorrect'
        else:
            msg='incorrect email or StaffId'
    return render_template('lecturer/login.html',msg=msg)


@app.route('/register', methods=['GET','POST'])
def signup():
    # Output message if something goes wrong...
    msg=''
    if request.method=='POST':
        surname=request.form['surname']
        othername=request.form['otherName']
        email=request.form['email']
        password=request.form['password']
        hashedPassword=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        phoneNumber=request.form['contact']
        staffId=request.form['lecturerId']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM lecturer WHERE email = %s|| phoneNumber=%s', (email,phoneNumber))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists!'
            cur.close()
            return render_template('lecturer/register.html',msg=msg)
        else:
            cur.execute("INSERT INTO lecturer (surname,othername,email,hashedPassword,phoneNumber,staffId) VALUES(%s,%s,%s,%s,%s,%s)",(surname,othername,email,hashedPassword,phoneNumber,staffId))
            mysql.connection.commit()
            cur.execute('SELECT * FROM lecturer WHERE email = %s', [email])
            account = cur.fetchone()
            cur.close()
            if account:
                session['type']='lecturer'
                session['loggedIn'] = True
                session['id'] = account['idLecturer']
                session['email'] = account['email']
                session['surname']=account['surname']
                session['verifiedMail']=account['verifiedMail']
                nameOfUser=session['surname']
            return redirect('/dashboard')
    return render_template('lecturer/register.html',msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedIn', None)
   session.pop('id', None)
   session.pop('email', None)
   session.pop('type', None)
   session.pop('surname', None)
   session.pop('verifiedMail', None)
   # Redirect to login page
   return redirect(request.referrer)

#--------------------------------------------------------
#-----------------Lecturer's DASHBOARD-------------------
#--------------------------------------------------------
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
  #  return render_template('lecturer/dashboard.html')
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        return render_template('lecturer/dashboard.html',nameOfUser=nameOfUser),200
    return redirect('/login')

@app.route('/apply')
def apply():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * from applicationWindow LIMIT 1')
        applicationWindow=cur.fetchone()
        if applicationWindow:
            endDate=applicationWindow['endTime']
            startDate=applicationWindow['startTime']
            return render_template('lecturer/applyBedspace.html',nameOfUser=nameOfUser,startDate=startDate,endDate=endDate)
        #-----------------------------------------------
        #-----------IF APPLICATION WINDOW HAS NOT BEEN OPEN-------
        return 'APPLICATION WINDOW HAS NOT BEEN OPEN'
    return redirect('/login')


@app.route('/applyforBedspace')
def applyforBedspace():
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        alreadyBooked=cur.execute("SELECT idLecturer from bookingList WHERE idLecturer=%s",[g.id])
        if alreadyBooked:
            return "YOU HAVE ALREADY BOOKED FOR A BED SPACE THIS YEAR"
        nameOfuser=g.surname        
        cur.execute('SELECT * from applicationWindow LIMIT 1')
        applicationWindow=cur.fetchone()
        if applicationWindow:
            endDate=applicationWindow['endTime']
            startDate=applicationWindow['startTime']
            currentTime = datetime.now()
            #currentTime=str(currentTime)
            #currentTime=datetime.strptime(currentTime, '%Y-%m-%dT%H:%M')
            if currentTime<endDate:
                cur.execute("INSERT INTO bookingList(idLecturer) VALUES (%s)",[g.id])
                mysql.connection.commit()
                return render_template('lecturer/wardInfoSuccess.html')
            return "APPLICATION HAS ENDED"
                
        return 'APPLICATION WINDOW HAS NOT BEEN OPEN'
    return redirect('/login')
    
    
    
    
@app.route('/accept/wardInfo',methods=['GET','POST'])
def acceptWardInfo():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        msg=''
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT applicationId FROM selectedApplicants where idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        hasBeenSelected=cur.fetchone()
        if not hasBeenSelected:
            msg1="SORRY"
            msg= 'You do not have access to the page requested'
            return render_template('lecturer/acceptDecline.html',nameOfUser=nameOfUser,msg=msg,msg1=msg1)
        if request.method=='POST':
            lastName=request.form['lastName']
            otherName=request.form['otherName']
            reference=request.form['reference']
            gender=request.form['gender']
           
            cur.execute('SELECT referenceNumber FROM wardinfo WHERE referenceNumber = %s|| idLecturer=%s LIMIT 1', (reference,[g.id]))
            account = cur.fetchone()
            if account:
                cur.close()
                msg="This student has already been registered for a Bedspace"
                return render_template('lecturer/wardinfo.html',msg=msg)
            else:
                if 1==1:
                    applicationId=hasBeenSelected['applicationId']
                    cur.execute("INSERT INTO wardinfo (surname,otherName,referenceNumber,gender,idLecturer,applicationId) VALUES(%s,%s,%s,%s,%s,%s)",(lastName,otherName,reference,gender,[g.id],applicationId))
                    cur.execute("UPDATE selectedApplicants SET accepted='YES' WHERE idLecturer=%s",[g.id])
                    mysql.connection.commit()
                    msg1="SUCCESS"
                    msg= 'You have successfully Accepted the Bed Space'
                    nameOfUser=g.surname

                    return render_template('lecturer/acceptdecline.html',nameOfUser=nameOfUser,msg=msg,msg1=msg1)
                #except MySQLdb.IntegrityError:
                else:
                    msg='Please type info again'
                    app.logger.info('insert into booking list did not work')
                    return render_template('lecturer/wardInfo.html',msg=msg)            

        return render_template('lecturer/wardInfo.html',msg=msg)
    return redirect('/login')

@app.route('/swap')
def swap():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        return render_template('lecturer/sellorbuy.html',nameOfUser=nameOfUser)
    return redirect('/login')

@app.route('/acceptbedspace')
def acceptbedspace():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #to know if you have been alocated a bed and youve not sold it too
        cur.execute("SELECT idLecturer FROM selectedApplicants where idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        hasBeenSelected=cur.fetchone()
        cur.close()
        if hasBeenSelected:          
            return render_template('lecturer/accept.html',nameOfUser=nameOfUser)
        else:
            msg1="SORRY"
            msg="You do not have a bedSpace to accept or decline"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect('/login')

@app.route('/accept')
def accept():
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT idLecturer FROM selectedApplicants where idLecturer=%s AND sold='NO' AND accepted IS NULL LIMIT 1;",[g.id])
        hasBeenSelected=cur.fetchone()
        if hasBeenSelected:
            return redirect('/accept/wardInfo')
        else:
            msg1="SORRY"
            msg="You do not have a bedSpace to accept or decline"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect ('/login')

@app.route('/decline')
def decline():
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT idLecturer FROM selectedApplicants where idLecturer=%s AND sold='NO' AND accepted IS NULL LIMIT 1;",[g.id])
        hasBeenSelected=cur.fetchone()
        if hasBeenSelected:
            cur.execute("DELETE FROM selectedApplicants WHERE idLecturer=%s;",[g.id])
            cur.execute("UPDATE lecturer SET priority=priority-1 WHERE idLecturer=%s;",[g.id])
            mysql.connection.commit()
            cur.close()
            msg1="SUCCESS"
            msg= 'You have successfully Rejected the Bed Space'
            nameOfUser=g.surname

            return render_template('lecturer/acceptDecline.html',nameOfUser=nameOfUser,msg=msg,msg1=msg1)
        else:
            msg1="SORRY"
            msg="You do not have a bedSpace to accept or decline"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect ('/login')

@app.route('/sellbed')
def sellBed():
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT idLecturer FROM selectedApplicants where idLecturer=%s AND sold='NO';",[g.id])
        hasBeenSelected=cur.fetchone()
        if hasBeenSelected:
            nameOfUser=g.surname
            return render_template('lecturer/sellBed.html',nameOfUser=nameOfUser)
        else:
            msg1="SORRY"
            msg="You do not have a bedSpace to Sell"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect ('/login')

@app.route('/postBed')
def postBed():
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT applicationId FROM selectedApplicants where idLecturer=%s AND sold='NO';",[g.id])
        hasBeenSelected=cur.fetchone()
        if hasBeenSelected:
            nameOfUser=g.surname
            applicationId=hasBeenSelected['applicationId']
            cur.execute("SELECT idLecturer FROM sellingBed where idLecturer=%s",[g.id])
            bedAlreadyPosted=cur.fetchone()
            if bedAlreadyPosted:
                cur.close()
                msg1="ERROR"
                msg="You have already put this bedspace up for trade"
                return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
            cur.execute("INSERT INTO sellingbed(applicationID,idLecturer) VALUES(%s,%s);",(applicationId,[g.id]))
            mysql.connection.commit()
            cur.close()
            return render_template('lecturer/adpostsuccess.html',nameOfUser=nameOfUser)
        else:
            cur.close()
            msg1="SORRY"
            msg="You do not have a bedSpace to Sell"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect('/login')

@app.route('/reviewBed')
def reviewBed():
    if g.loggedIn and g.type=='lecturer':
        #check if hes posted a bed for sale
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT applicationId,id FROM sellingBed where idLecturer=%s AND sold='NO'; LIMIT 1",[g.id])
        bedPosted=cur.fetchOne()
        if bedPosted:
            applicationId=bedPosted['applicationId']
            sellingBedId=bedPosted['id']
            #-----------------------------------------------------------
            #-------------------------------------------------------
            
        else:
            cur.close()
            msg1="ERROR"
            msg="You have not posted a bed For sale"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
    return redirect('/login')

@app.route('/buybed')
def buyBed():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT *FROM selectedApplicants WHERE idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        alreadyHasBedSpace=cur.fetchone()
        if alreadyHasBedSpace:
            cur.close()
            msg1="ERROR"
            msg="You are NOT eligible to use this feature. You already have a bedSpace"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        cur.execute("SELECT s.idLecturer,s.id, s.applicationId,l.phoneNumber, l.surname, l.othername FROM sellingBed as s LEFT JOIN lecturer as l ON l.idLecturer=s.idLecturer;")
        sellers=cur.fetchall()
        return render_template('lecturer/buyBed.html',nameOfUser=nameOfUser,sellers=sellers)
    return redirect ('/login')

@app.route('/request/<int:id>/<int:idLecturer>/<int:applicationId>')
def requestBed(id,idLecturer,applicationId):
    if g.loggedIn and g.type=='lecturer':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT *FROM selectedApplicants WHERE idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        alreadyHasBedSpace=cur.fetchone()
        if alreadyHasBedSpace:
            cur.close()
            msg1="ERROR"
            msg="You are NOT eligible to use this feature. You already have a bedSpace"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        cur.execute("SELECT * from bid where sellingbed_selectedApplicants_idLecturer=%s AND lecturer_idLecturer=%s",(idLecturer,[g.id]))
        hasPlacedBidAlready=cur.fetchone()
        if hasPlacedBidAlready:
            cur.close()
            msg1="ERROR"
            msg="You have already made this request"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        cur.execute("SELECT * FROM sellingBed WHERE id=%s AND idLecturer=%s AND applicationId=%s",(id,idLecturer,applicationId))
        bedExists=cur.fetchone()
        if bedExists:
            cur.execute("INSERT INTO bid(lecturer_idLecturer,sellingBed_id,sellingbed_selectedApplicants_idLecturer,sellingbed_selectedApplicants_applicationId) VALUES (%s,%s,%s,%s); ",([g.id],id,idLecturer,applicationId))
            mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return redirect ('/login')


@app.route('/sentrequests')
def sentrequests():
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT *FROM selectedApplicants WHERE idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        alreadyHasBedSpace=cur.fetchone()
        if alreadyHasBedSpace:
            cur.close()
            msg1="ERROR"
            msg="You are NOT eligible to use this feature. You already have a bedSpace"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        cur.execute("SELECT l.surname,l.othername,l.phoneNumber,b.id,b.sellingbed_id FROM bid AS b LEFT JOIN lecturer AS l ON l.idLecturer=b.sellingbed_selectedApplicants_idLecturer WHERE b.lecturer_idLecturer=%s;",[g.id])
        myBids=cur.fetchall()
        cur.close()
        return render_template('lecturer/sentrequests.html',nameOfUser=nameOfUser,myBids=myBids)
    return redirect('/login')

@app.route('/sentrequests/cancel/<int:sellingbed_id>')
def cancelSentRequest(sellingbed_id):
    if g.loggedIn and g.type=='lecturer':
        nameOfUser=g.surname
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT *FROM selectedApplicants WHERE idLecturer=%s AND sold='NO' LIMIT 1;",[g.id])
        alreadyHasBedSpace=cur.fetchone()
        if alreadyHasBedSpace:
            cur.close()
            msg1="ERROR"
            msg="You are NOT eligible to use this feature. You already have a bedSpace"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        cur.execute("SELECT id FROM bid where sellingbed_id=%s AND lecturer_idLecturer=%s;",(sellingbed_id,[g.id]))
        hasRequestedForBed=cur.fetchone()
        if not hasRequestedForBed:
            cur.close()
            msg1="ERROR"
            msg="You have not requested for this Bed Space"
            return render_template('lecturer/acceptdecline.html',msg=msg,msg1=msg1)
        bidId=hasRequestedForBed['id']
        cur.execute("DELETE FROM bid WHERE id=%s;",[bidId])
        mysql.connection.commit()
        cur.close()
        return redirect('/sentrequests')
    return redirect('/login')
#--------------------------------------------------------
#-----------------admin DASHBOARD------------------------
#--------------------------------------------------------
@app.route('/admin')
@app.route('/admin/dashboard')
def adminHome():
    if g.loggedIn and g.type=='admin':
        return render_template('admin/index.html')
    return redirect('/admin/login')

@app.route('/admin/login',methods=['GET','POST'])
def adminlogIn():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM admin WHERE username = %s', [username])
        account = cur.fetchone()
        cur.close()
        if account:
            hashedPassword=account['hashedPassword']
            if bcrypt.checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8')):
                session['type']='admin'
                session['loggedIn'] = True
                session['id'] = account['adminId']
                session['email'] = None
                session['surname']=None
                session['verifiedMail']=None
                return redirect('/admin/dashboard')
            else:'Password is Incorrect'
        else:
            msg='incorrect email'
    return render_template('admin/login.html',msg=msg)

@app.route('/admin/setApplicationWindow',methods=['GET','POST'])
def adminSetApplicationWindow():
    if g.loggedIn and g.type=='admin':
        msg=''
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * from applicationWindow LIMIT 1")
        existingWindow=cur.fetchone()
        if existingWindow:
            return render_template('admin/applicationWindowAlreadyOpened.html')
        if request.method=='POST':
            
            startDate=datetime.strptime(request.form['startDate'], '%Y-%m-%dT%H:%M')
            endDate=datetime.strptime(request.form['endDate'], '%Y-%m-%dT%H:%M')
            slot=request.form['slot']
            if endDate>startDate:               
                try:
                    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("INSERT into applicationWindow (startTime,endTime,slots) VALUES (%s,%s,%s)",(startDate,endDate,slot))
                    mysql.connection.commit()
                        
                except MySQLdb.IntegrityError:
                    msg='Please type info again'
                    app.logger.info('insert into application window did not work')
                    return render_template('admin/applicationWindow.html'),500
                finally:
                    return render_template('admin/applicationWindowSuccess.html'),200
                    
            else:
                app.logger.info('admin %s trying to enter same date or wrong date input',[g.id])
                msg='End date can not be equal to or later than the start Date'
            #--------------------------------------
            #------------------------------------------
        return render_template('admin/applicationWindow.html',msg=msg)
    return redirect('/admin/login')


@app.route('/admin/shuffle')
def shuffle():
    if g.loggedIn and g.type=='admin':
        #---Check if the window is closed
        if 1==1:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * from applicationWindow LIMIT 1')
            applicationWindow=cur.fetchone()
            if applicationWindow:
                endDate=applicationWindow['endTime']
                slots=applicationWindow['slots']
                currentTime = datetime.now()
                #currentTime=datetime.strptime(currentTime, '%Y-%m-%dT%H:%M')
                if currentTime>endDate:
                    #-check if already shuffled
                    cur.execute('SELECT applicationId from selectedApplicants LIMIT 1;')
                    numberOfSelectedApplicants=cur.fetchone()
                    if not numberOfSelectedApplicants:
                        cur.execute('SELECT bookingList.bookingId, bookingList.idLecturer,lecturer.priority as priority FROM bookingList LEFT JOIN lecturer ON bookingList.idLecturer=lecturer.idLecturer ORDER BY lecturer.priority ASC')
                        bookingList=cur.fetchall()
                        print(bookingList,flush=True)
                        totalShuffledList=[]
                        shuffledList=[]
                        newList=[]
                        maxPriority=max(bookingList,key=itemgetter('priority'))
                        print (maxPriority, flush=True)
                        for x in [0,1,maxPriority]:                           
                            for item in bookingList:
                                print(x,flush=True)
                                print(item,flush=True)
                                if item['priority']==x:
                                    newList.append(item['idLecturer'])
                            random.shuffle(newList)
                            totalShuffledList.extend(newList)
                            print(totalShuffledList,flush=True)
                            newList.clear()
                        print(totalShuffledList, flush=True)
                        selectedApplicants=totalShuffledList[:slots]
                        for item in selectedApplicants:
                            cur.execute("INSERT INTO selectedApplicants(idLecturer) VALUES (%s)",[item])
                            cur.execute("UPDATE lecturer SET priority=priority+1 WHERE idLecturer=%s",[item])
                            mysql.connection.commit()
                        return "SUCCESS"
                    else:
                        return "YOU HAVE ALREADY SHUFFLED "#------------------------------------------------__-
                    #-------------------------------------------------
                else:
                    cur.close()
                    msg='Application Window has not yet ended'
                    return render_template('admin/selectedApplicants.html',msg=msg) #-=-=-=-=--=-=-=-=-=--=-=
            else:   
                msg='You have not opened an application window' 
                return render_template('admin/selectedApplicants.html')
        #-check if already shuffled
        #- check that booking list is not empty
        #- check number of booked people
        #- check number of slots
        else:
            return redirect(request.referrer)
        
    return redirect('/admin/login')

@app.route('/admin/editApplicationWindow',methods=['GET','POST'])
def editApplicationWindow():
    if g.loggedIn and g.type=='admin':
        if request.method=='POST':
            if request.method=='POST':
                cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            startDate=datetime.strptime(request.form['startDate'], '%Y-%m-%dT%H:%M')
            endDate=datetime.strptime(request.form['endDate'], '%Y-%m-%dT%H:%M')
            slot=request.form['slot']
            if endDate>startDate:
                cur.execute("SELECT * from applicationWindow LIMIT 1")
                existingWindow=cur.fetchone()
                if not existingWindow:
                    msg="PLEASE OPEN AN APPLICATION WINDOW FIRST"
                    return render_template('admin/editwindowdate.html')
                else:
                    try:
                        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cur.execute("UPDATE applicationWindow SET startTime=%s,endTime=%s,slots=%s LIMIT 1",(startDate,endDate,slot))
                        mysql.connection.commit()
                        return render_template('admin/applicationWindowSuccess.html'),200
                    except MySQLdb.IntegrityError:
                        msg='Please type info again'
                        app.logger.info('insert into application window did not work')
                        return render_template('admin/editwindowdate.html'),500
                    
            else:
                app.logger.info('admin %s trying to enter same date or wrong date input',[g.id])
                msg='End date can not be equal to or later than the start Date'
            #--------------------------------------
        return render_template('admin/editwindowdate.html')
    return redirect('/admin/login')

@app.route('/selectedApplicants')
def selectedApplicants():
    if g.loggedIn and g.type=='admin':
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #joining selected applicants, ward info and lecturers
        #ifnull is to ensure that we dont get NULL 
        cur.execute("SELECT IFNULL(s.accepted,'N/A') AS accepted, l.surname,l.othername,l.staffId, IFNULL(w.referenceNumber,'N/A') AS referenceNumber, IFNULL(w.gender,'N/A') AS gender, IFNULL(w.surname,'N/A')  AS wardSurname, IFNULL(w.othername,'N/A') AS wardOtherName FROM selectedapplicants AS s LEFT JOIN lecturer AS l ON l.idlecturer=s.idLecturer LEFT JOIN wardInfo AS w ON w.idLecturer=s.idLecturer;")
        selectedApplicants=cur.fetchall()
        return render_template('admin/selectedApplicants.html',selectedApplicants=selectedApplicants)
    return redirect('/admin/login')


#-------------TO REGISTER AN ADMIN-----------
@app.route('/admin/register')
def adminRegister():
    password='administrator'
    username='admin'
    hashedPassword=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('select * from admin LIMIT 1')
    adminExists=cur.fetchone()
    if not adminExists:
        cur.execute('INSERT INTO admin (username,hashedPassword) VALUES (%s,%s)',(username,hashedPassword))
        mysql.connection.commit()
        return redirect('/admin')
    return 'admin already exists'

#------------------------------------------------------------
#--------------BEFORE Requests--------------------------------
@app.before_request
def before_request():
    g.type=None
    g.loggedIn= None
    g.id=None
    g.email=None
    g.surname=None
    g.verifiedMail=None
    if 'loggedIn' in session:
        g.type=session['type']
        g.loggedIn= True
        g.id=session['id']
        g.email=session['email']
        g.surname=session['surname']
        g.verifiedMail=session['verifiedMail']
#-----------------THANK YOU--------------------------------

if __name__=='__main__':
    app.run(debug=True)