from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector as sql
import hashlib

# Create your views here.

sp_username,sp_email,sp_pass,sp_cnfrmpass = "","","",""
si_username,si_pass = "",""

def home(request):
    return render(request,"loginpage_app/signup.html")

def signup(request):
    pass
    global sp_username,sp_email,sp_pass,sp_cnfrmpass,si_username,si_pass
    if request.method == "POST":
        m = sql.connect(host="localhost",user="root",password="Twilight@28",database="fake_job_users",auth_plugin='mysql_native_password')
        cursor = m.cursor()
        d = request.POST
        for key,value in d.items():
            if key=="sp_username":
                sp_username = value
            if key=="sp_email":
                sp_email = value
            if key=="sp_pass":
                sp_pass = value
            if key=="sp_cnfrmpass":
                sp_cnfrmpass = value
            if key=="si_username":
                si_username = value
            if key=="si_pass":
                si_pass = value

        if sp_username:
            encpass = hashlib.sha256(sp_cnfrmpass.encode()) 
            c = "insert into users values('{}','{}','{}')".format(sp_username,sp_email,encpass.hexdigest())#sp_cnfrmpass)
            cursor.execute(c)
            m.commit()
            return render(request,"loginpage_app/signup.html")
        else:
            encpass_check = hashlib.sha256(si_pass.encode()) 
            c = "select * from users where email='{}' and password = '{}'".format(si_username,encpass_check.hexdigest())#si_pass)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            if t==():
                return render(request,"loginpage_app/fail.html")
            else:
                return render(request,"fake_job_app/index.html")
    return render(request,"loginpage_app/signup.html")