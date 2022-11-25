from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import subprocess
import jwt

app = Flask(__name__)

def has_valid_jwt(jwt_cookie):
    try:
        jwt.decode(jwt_cookie,verify=False)
        return True
    except:
        return False

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('ping.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if (request.form['password'] == os.environ['dew_password'] \
            and request.form['username'] == os.environ['dew_user']) \
            or has_valid_jwt(request.cookies.get('jwt')):
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/ping', methods=['POST'])
def do_ping():
    if not session.get('logged_in'):
        return render_template('login.html')
    pingcmd = "ping -c 1 %s" % request.form['pingdestination']

    output = ""
    try:
        output = subprocess.check_output(pingcmd, shell=True)
        output = output.decode('utf-8')
    except:
        print("Exception")
    return render_template('pingoutput.html', pingresult=output)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    print("Log: Starting\nUsername: " + os.environ['dew_user'] + "\nPassword:" + os.environ['dew_password'])
    app.run(debug=True, host='0.0.0.0', port=4000)
