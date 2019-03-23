from flask import Flask, render_template, request, redirect, flash, make_response
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_paco"

import hashlib, datetime

# Modules P3t4
from modules.P3t4Users.ControllerUsersDB import P3t4ControllerUsers
p3t4ControllerUsers = P3t4ControllerUsers()

@app.route('/')
def home():
    return render_template("home.tpl")
    
@app.route('/login')
def service_login():
    return render_template("login.tpl")

@app.route('/login', methods=['POST'])
def service_login_post():

    # expirate token
    ts = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    
    if request.method == 'POST':
        
        name = request.form['username']
        password = request.form['password']
        
        token = hashlib.sha512(name + password).hexdigest()

        if p3t4ControllerUsers.LoginUser(name, password):
            resp = make_response(redirect('/challenges'))
            resp.set_cookie('token', token, path='/', expires=ts)
            return resp 
        else:
            return redirect("/login")

@app.route('/register')
def service_register():
    return render_template("register.tpl")

@app.route('/register', methods=['POST'])
def service_register_post():

    if request.method == 'POST':
        
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        code = request.form['code']

        result = p3t4ControllerUsers.RegisterUser(name, password, email, code)

        if result == "error":
            flash("Error al registar el usuario.", "error")
            return redirect('/register')
        elif result == "require":
            flash("Valores no validos", "require")
            return redirect('/register')
        elif result == "code":
            flash("Codigo no valido", "code")
            return redirect('/register')
        
        return redirect('/login')

    return render_template("register.tpl")

@app.route('/challenges')
def service_chanllenges():

    if request.method == 'GET':
        #resp = make_response(redirect('/challenges'))
        #resp.set_cookie('token', instUsr.token, path='/', expires=ts)
        token = request.cookies.get('token')
        
        
        if p3t4ControllerUsers.CheckToken(token):
            return render_template('challenges.tpl')
        else:
            return redirect('/login')
    
    


@app.route('/users')
def service_usuarios():
    return render_template("users.tpl")

@app.route('/profile/<name>')
def service_dashboard(name):
    return render_template("profile.tpl")

@app.route('/challenge/<name>')
def service_challenge(name):
    return render_template("challenge.tpl")


@app.route('/upload/challenge')
def service_subchallenge():
    return render_template("subChallenge.tpl")

#@error(404)
#def error404(error):
#    return template("view/errors/404.tpl")
#
#@error(500)
#def error404(error):
#    return 'Nothing here, sorry 500'
#
#@error(505)
#def error404(error):
#    return 'Nothing here, sorry 505'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)