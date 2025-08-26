from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from config import flask_secret_key
from system_usage import get_usage_data
from take_screenshot import capture_image
from sql_connection import SQLconnector 
from totp_key import TOTPManager


app = Flask(__name__)
app.secret_key = flask_secret_key

#Will be deleted soon
names = ['John','George','Valera','Nicola']

@app.route("/")
@app.route("/home")
def home():
    if session.get('logged_in') == True:
        return render_template('status.html')
    else:
        return redirect(url_for('login'))
    
#test page that will be deleted soon 
@app.route('/test')
def test():
    return render_template('testfile.html', names=names,)

#template that send one-time code to complete login and get to the manage page
@app.route('/code',methods=['GET','POST'])
def code():
    if request.method == 'POST':
        
        code = ''.join(request.form.getlist('digit'))

        #Get secret TOTP key for an user and send it to TOTP manager to verify one-time code and give access to the main template
        if TOTPManager.verify_totp(SQLconnector.get_secret_key(session['username']), code):
            session['logged_in'] = True
            return redirect(url_for('home'))
        
        else:
            error = 'Invalid code'
            return render_template('code.html', error=error,auth_failed=True)
        
    #check if login page was passed properly and user wrote right password or else return him back
    else:
        if session.get('password_verified') == True:
            return render_template('code.html')
        else:
            return redirect(url_for('login'))
            
    
#Check password and login and move to home page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':

        # variables that contain username and password received from user
        submitted_username = request.form.get('username')
        submitted_password = request.form.get('password')

        # use class method that check that username and password are correct and send to the home page  
        if SQLconnector.check_login(username=submitted_username, password=submitted_password):
            session['username'] = submitted_username
            session['password_verified'] = True
            
            return redirect(url_for('code'))
        else:
            
            error = 'Incorrect password or login'
            return render_template('login.html', error=error,auth_failed=True) 
        
    else:
        return render_template('login.html')

# private page for management users such as add,delete and change data in user account
@app.route('/private/admin/user-management',methods=['GET','POST'])
def user_management():
    if request.method == 'POST':
        submitted_data = request.form.to_dict()
        print(submitted_data)
        if submitted_data:
            SQLconnector.create_new_user(password=submitted_data.get('password'), username= submitted_data.get('username'))
            return redirect('user-management')
    
    else:
        return render_template('user_management.html', users=SQLconnector.get_all_users())

#function to delete user from the database through the user management page
@app.route('/delete-user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    print(user_id)
    SQLconnector.delete_user(user_id)

    return redirect(url_for('user_management'))

#function to logout from user account and clear all session data
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))       

#Sending data to fetch 
@app.route('/data')
def data():
    return jsonify(get_usage_data())

#function that makes screenshot and send it to the web application
@app.route('/screenshot')
def screenshot():
    return jsonify(capture_image())


if __name__ == '__main__':
    app.run(debug=True)
    
