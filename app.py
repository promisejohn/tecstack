# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
# Author: promisejohn
# Email: promise.john@gmail.com
#

from flask import 	Flask, render_template, request, redirect, url_for, flash, \
					send_from_directory, make_response, abort, session, escape
from werkzeug import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = '/Users/promise/dev/python/web/tecstack/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/index',methods=['GET'])
def index():
	app.logger.debug('get /index')
	app.logger.warning('get /index')
	app.logger.error('get /index')
	uname = request.cookies.get('uname')
	if 'username' in session:
		msg = 'logged in as %s.' % escape(session['username'])
	else:
		msg = 'You are not logged in.'
	resp = make_response(render_template('index.html',name=uname,msg=msg))
	if not uname:
		resp.set_cookie('uname','john')
	return resp

@app.route('/user/<username>')
def show_user_profile(username):
	return "User %s " % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return "Post %d " % post_id

@app.route('/about')
def about():
	return "About page"

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method == 'POST':
		# validate form, show error if nessary
		session['username'] = request.form['username']
		flash('You were successfully logged in')
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))

@app.route('/upload',methods=['POST','GET'])
def upload_file():
	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	if request.method == 'POST':
		f = request.files['myfile']
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			return redirect(url_for('index'))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name='myfile'>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/download/<filename>')
def download_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER',filename])

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'),404


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')