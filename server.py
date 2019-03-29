from flask import Flask, render_template, request, redirect, flash, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import hashlib, datetime, os, time

# root upload folder
UPLOAD_FOLDER = os.getcwd() + '\\public-challenges'
ALLOWED_EXTENSIONS = set(['.zip'])

# app
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_paco"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Modules P3t4
from modules.P3t4Users.ControllerUsersDB import P3t4ControllerUsers
p3t4ControllerUsers = P3t4ControllerUsers()

# Modules P3t4
from modules.P3t4Challenges.ControllerChallengesDb import P3t4ControllerChallenges
p3t4ControllerChallenges = P3t4ControllerChallenges()

@app.route('/')
def home():

    data = p3t4ControllerUsers.FindTopTresUsers()

    return render_template("home.html", data=data)
    
@app.route('/login')
def service_login():
    return render_template("login.html")

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
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def service_register_post():

    if request.method == 'POST':
        
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        code = request.form['code']

        parseName = name.lower()

        result = p3t4ControllerUsers.RegisterUser(parseName, password, email, code)

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

    return render_template("register.html")

@app.route('/logout')
def service_logout():

    if request.method == 'GET':
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)
        return resp

@app.route('/challenges')
def service_chanllenges():

    if request.method == 'GET':
        #resp = make_response(redirect('/challenges'))
        #resp.set_cookie('token', instUsr.token, path='/', expires=ts)
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            dataChallenges = p3t4ControllerChallenges.GetAllChallenges()
            return render_template('challenges.html', dataChallenges=dataChallenges, dataUser=dataUser)
        else:
            return redirect('/')

@app.route('/challenge/<challengeID>', methods=['GET', 'POST'])
def service_challenge(challengeID):

    token = request.cookies.get('token')

    if request.method == 'GET':
        #resp = make_response(redirect('/challenges'))
        #resp.set_cookie('token', instUsr.token, path='/', expires=ts)

        if p3t4ControllerUsers.CheckToken(token):

            # return data user name
            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            dataAllUsers = p3t4ControllerUsers.FindAllUsersSort()
            dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
            return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
        else:
            return redirect('/')
    
    if request.method == 'POST':
       
        flag = request.form['flag']

        if p3t4ControllerUsers.CheckToken(token):
            
            username = p3t4ControllerUsers.FindUserByToken(token)

            if p3t4ControllerChallenges.CheckFlag(username, challengeID, flag):
                
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersSort()
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                #flash("Flag correcta, buen trabajo", "success")
                return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
            
                #resp = make_response(render_template('challenges.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge))
                #return resp
            else:
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersSort()
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                #flash("Flag incorrecta, siguen intentandolo", "danger")
                return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
                
        else:
            return redirect('/')

@app.route('/users')
def service_usuarios():

    if request.method == 'GET':
        #resp = make_response(redirect('/challenges'))
        #resp.set_cookie('token', instUsr.token, path='/', expires=ts)
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            data = p3t4ControllerUsers.FindAllUsersSort()

            return render_template('users.html', data=data, dataName=dataName)
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', '', path='/', expires=0)
            return resp

@app.route('/profile/<name>')
def service_dashboard(name):
  
    if request.method == 'GET':
    
        if p3t4ControllerUsers.FindUserName(name):

            #resp = make_response(redirect('/challenges'))
            #resp.set_cookie('token', instUsr.token, path='/', expires=ts)
            token = request.cookies.get('token')

            if p3t4ControllerUsers.CheckTokenByName(name, token):
                data = p3t4ControllerUsers.CheckTokenReturnData(token)
                return render_template('profile.html', data=data)
            else:
                resp = make_response(redirect('/login'))
                resp.set_cookie('token', '', path='/', expires=0)
                return resp

        else:
            resp2 = make_response(redirect('/'))
            resp2.set_cookie('token', '', path='/', expires=0)
            return resp2

@app.route('/admin')
def service_admin():

    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                data = p3t4ControllerUsers.FindAllUsersSort()
                return render_template('admin.html', data=data, dataName=dataName)
            else:
                resp = make_response(redirect('/'))
                resp.set_cookie('token', '', path='/', expires=0)
                return resp
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', '', path='/', expires=0)
            return resp

@app.route('/admin/edit/<name>')
def service_editUser(name):
    
    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.FindUserNameReturnData(name)
                #resp = make_response(redirect('/challenges'))
                #resp.set_cookie('token', instUsr.token, path='/', expires=ts)

                return jsonify(dataName)
            else:
                return "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':

        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.FindUserNameReturnData(name)
                #resp = make_response(redirect('/challenges'))
                #resp.set_cookie('token', instUsr.token, path='/', expires=ts)

                return jsonify(dataName)
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/admin/delete/<name>', methods=['GET', 'POST'])
def service_deleteUser(name):
    
    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                dataName = p3t4ControllerUsers.FindUserNameReturnData(name)
                #resp = make_response(redirect('/challenges'))
                #resp.set_cookie('token', instUsr.token, path='/', expires=ts)

                return jsonify(dataName)
            else:
                "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
    
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.FindUserNameReturnData(name)
                #resp = make_response(redirect('/challenges'))
                #resp.set_cookie('token', instUsr.token, path='/', expires=ts)
                result = p3t4ControllerUsers.FindUserByNameAndDelete(name)
                return result
            else:
                return "error"
        else:
            return "Admin Require"
    
@app.route('/public/challenge', methods=['GET', 'POST'])
def service_subchallenge():

    if request.method == 'GET':

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            data = p3t4ControllerUsers.CheckTokenReturnData(token)
            return render_template('publicChallenge.html', data=data)
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', '', path='/', expires=0)
            return resp

    if request.method == "POST":

        if 'file' not in request.files:
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')
        
        file = request.files['file']

        if file.content_type != "application/x-zip-compressed":
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')

        if file.filename == '':
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')
        
        titulo = request.form['titulo']
        puntos = request.form['puntos']
        flag = request.form['flag']
        descripcion = request.form['descripcion']

        if titulo == '' or len(titulo) > 30:
            flash("Titulo no valido.", "danger")
            return redirect('/public/challenge')
        
        if puntos == '' or len(puntos) > 2:
            flash("Puntos no validos.", "danger")
            return redirect('/public/challenge')
        
        if flag == '' or len(flag) > 50:
            flash("Flag no valida", "danger")
            return redirect('/public/challenge')
        
        if descripcion == '' or len(descripcion) > 60:
            flash("Descipcion no valida.", "danger")
            return redirect('/public/challenge')

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            pass
        else:
            return redirect('/')

        #if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # datetime
        hora = time.strftime("%H-%M-%S")
        fecha = time.strftime("%d-%m-%y")
        
        nameDate = fecha + "-" + hora + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nameDate))

        user = p3t4ControllerUsers.CheckTokenReturnData(token)

        if p3t4ControllerChallenges.SaveChallenge(user['name'], titulo, fecha, puntos, flag, nameDate, descripcion):
            flash("Publicado con exito, a la espera de que un administrador lo valide.", "success")
            return redirect('/public/challenge')
        else:
            flash("No se a podido publicar, ponte en contacto con un administrador.", "danger")
            return redirect('/public/challenge')
            
@app.route('/send/<name>')
def service_send_file(name):

    path = app.config['UPLOAD_FOLDER'] + "\\" + name
    return send_file(path, mimetype="application/x-zip-compressed")


#@error(404)
#def error404(error):
#    return template("view/errors/404.html")
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