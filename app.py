from flask import Flask, render_template, url_for, redirect, flash

#bootstrap - provides bootstrap/base.html which is invisible
from flask_bootstrap import Bootstrap

#using flaskforms i have separated all the classes to forms.py inside classes
from classes import forms

#request object - handling request
from flask import request

#importing configurations
from config import Config

from pymongo import MongoClient

#dunder name is given cuz , it says this is the main file and all the other files are accessed from the files like directories (templates dir)
app = Flask(__name__)


#from_object adds the key:value's to app.config
app.config.from_object(Config)



client = MongoClient('localhost',27017,username='jbadmin',password='jbadminpass')
db = client.jb
users = db.users


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shady:thisisthepass@localhost/sample'

bootstrap = Bootstrap(app)



@app.route('/login',methods=['GET','POST'])
def login():
	form = forms.login()
	if(request.method == 'POST'):
		if(form.validate_on_submit()):
			record = list(users.find({'uname':request.form['uname']}))
			if(record and users.find({'uname':record[0]['uname'],'pwrd':record[0]['pwrd']})):
				return redirect(url_for('home',user=record[0]['name']))
			else:
				print('Nooo')
	return render_template('login.html',form=form)


@app.route('/home/<user>')
def home(user):
	print('yes')
	return render_template('home.html',name=user)


@app.route('/register',methods=['GET','POST'])
def register():
	form = forms.register()
	if(request.method == 'POST'):
		if(form.validate_on_submit()):
			uname = request.form['uname']
			pwrd = request.form['pwrd']
			email = request.form['email']
			name = request.form['name']
			if(not list(users.find({'uname':uname}))):
				users.insert_one({'uname':uname,'pwrd':pwrd,'email':email,'name':name})
			flash('You are successfully registered! You can login now')
			return redirect(url_for('login'))
	return render_template('register.html',form=form)

# #routes (or) views
# @app.route('/login')
# def hello():
# 	return render_template('base.html')


#@app.route('/sampleroute')  I can pass any number of routes like this
@app.route('/test')
def test():
	return render_template('test.html')



@app.route('/sample',methods=['GET','POST'])
def sample():
	return render_template('index.html')




if(__name__ == '__main__'):
	app.run(host='localhost',port = 3000,debug = True)





