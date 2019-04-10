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


app.jinja_env.add_extension('jinja2.ext.loopcontrols')

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

@app.route('/faq')
def service_faq():
    return render_template('faq.html')
    
@app.route('/login', methods=['GET', 'POST'])
def service_login():

    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        
        name = request.form['username']
        password = request.form['password']

        token = hashlib.sha512(name + password).hexdigest()
        
        # expirate token
        ts = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        
        if p3t4ControllerUsers.LoginUser(name, password):
            resp = make_response(redirect('/challenges'))
            resp.set_cookie('token', token, path='/', expires=ts)
            return resp 
        else:
            return redirect("/login")

@app.route('/register', methods=['GET', 'POST'])
def service_register():

    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        
        name = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirm-password']
        email = request.form['email']
        code = request.form['code']

        print password
        print confirmPassword

        if password != confirmPassword:
            salida = "Los passwords tienen que ser iguales.".encode('utf-8')
            flash(salida, "error")
            return redirect('/register')
        

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

@app.route('/logout')
def service_logout():

    if request.method == 'GET':
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)
        return resp

@app.route('/challenges')
def service_chanllenges():

    if request.method == 'GET':
        
        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataUser == False:
                return resp
            
            dataChallenges = p3t4ControllerChallenges.GetAllChallenges()
            if dataChallenges == False:
                return resp

            return render_template('challenges.html', dataChallenges=dataChallenges, dataUser=dataUser)
        else:
            return resp

@app.route('/challenge/<challengeID>', methods=['GET', 'POST'])
def service_challenge(challengeID):

    if request.method == 'GET':
        
        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataUser == False:
                return resp
            
            dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
            if dataChallenge == False:
                return resp

            dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
            if dataAllUsers == False:
                return resp

            return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
        else:
            return resp
    
    if request.method == 'POST':
        
        token = request.cookies.get('token')
        
        flag = request.form['flag']
        
        if p3t4ControllerUsers.CheckToken(token):
            
            username = p3t4ControllerUsers.FindUserByToken(token)

            if p3t4ControllerChallenges.CheckFlag(username, challengeID, flag):
                
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
                #flash("Flag correcta, buen trabajo", "success")
                return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
            
                #resp = make_response(render_template('challenges.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge))
                #return resp
            else:
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
                #flash("Flag incorrecta, siguen intentandolo", "danger")
                return render_template('challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
                
        else:
            return redirect('/')

@app.route('/users')
def service_usuarios():

    if request.method == 'GET':

        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp
            
            dataAll = p3t4ControllerUsers.FindAllUsersSort()
            if dataAll == False:
                return resp

            return render_template('users.html', data=dataAll, dataName=dataName)
        else:
            return resp

@app.route('/profile/<name>')
def service_dashboard(name):
  
    if request.method == 'GET':
        
        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)
        
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.CheckTokenByName(name, token):
                
                # local user
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataUser == False:
                    return resp

                return render_template('profile.html', dataUser=dataUser)
            else:
                
                # view user
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataUser == False:
                    return resp

                viewUser = p3t4ControllerUsers.FindUserByNameReturnData(name)
                if viewUser == False:
                    return resp

                return render_template('userView.html', dataUser=dataUser, viewUser=viewUser)
        
        else:
            return resp

@app.route('/admin')
def service_admin():

    if request.method == 'GET':
        
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)

        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataName == False:
                    return resp

                dataAll = p3t4ControllerUsers.FindAllUsersSort()
                if dataAll == False:
                    return resp
                
                return render_template('admin.html', data=dataAll, dataName=dataName)
            else:
                return resp
        else:
            return resp

@app.route('/admin/edit/<userID>', methods=['GET', 'POST'])
def service_editUser(userID):
    
    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerUsers.FindUserIdReturnEdit(userID)

                if dataName == False:
                    return "error"

                newPacket = {
                    "name": dataName['name'],
                    "puntos": dataName['puntos'],
                    "activate": dataName['activate'],
                    "admin": dataName['admin']
                }

                return jsonify(newPacket)
            else:
                return "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):

            editUserName = request.form['mod-name']
            editUserScore = request.form['mod-score']
            editUserActivate = request.form['mod-activate']
            editUserAdmin = request.form['mod-admin']
            
            # check activate
            if editUserActivate == "false" or editUserActivate == "False":
                print "Active false"
                editUserActivate = False
            elif editUserActivate == "true" or editUserActivate == "True":
                print "Active true"
                editUserActivate = True
            else:
                print "Error type"
                return "error"

            # check admin
            if editUserAdmin == "false" or editUserAdmin == "False":
                print "Admin false"
                editUserAdmin = False
            elif editUserAdmin == "true" or editUserAdmin == "True":
                print "Admin true"
                editUserAdmin = True
            else:
                print "Error type"
                return "error"

            if p3t4ControllerUsers.CheckToken(token):
                
                userResult = p3t4ControllerUsers.FindUserIdEditUser(userID, editUserScore, editUserActivate, editUserAdmin)
                if userResult == False:
                    return "error"

                return userResult
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/admin/delete/<userID>', methods=['GET', 'POST'])
def service_deleteUser(userID):
    
    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                dataName = p3t4ControllerUsers.FindUserIdReturnDelete(userID)
                if dataName == False:
                    return "error"

                return dataName
            else:
                "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
    
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                result = p3t4ControllerUsers.FindUserIdDeleteUser(userID)
                if result == False:
                    return "error"

                return result
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/admin/challenges')
def service_adminChallenges():

    if request.method == 'GET':
        
        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataName == False:
                    return resp
                
                dataAll = p3t4ControllerChallenges.GetAllChallenges()
                if dataAll == False:
                    return resp

                return render_template('adminChallenge.html', data=dataAll, dataName=dataName)
            else:
                return resp
        else:
            print "Admin Require"
            return resp

@app.route('/admin/challenges/edit/<challengeID>',  methods=['GET', 'POST'])
def service_adminChallengesEdit(challengeID):

    if request.method == 'GET':
            
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            if p3t4ControllerUsers.CheckToken(token):

                dataName = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                if dataName == False:
                    return "error"

                newPacket = {
                    "id": dataName['_id'],
                    "puntos": dataName['puntos'],
                    "validado": dataName['validado'],
                    "creador": dataName['creador']
                }

                return jsonify(newPacket)
            else:
                return "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
    
        token = request.cookies.get('token')
    
        if p3t4ControllerUsers.CheckTokenAdmin(token):
    
            editChallengeID = request.form['mod-challengeID']
            editUserScore = request.form['mod-score']
            editUserValidate = request.form['mod-validate']
            editUserCreator = request.form['mod-creator']
            
            # check activate
            if editUserValidate == "false" or editUserValidate == "False":
                print "Active false"
                editUserValidate = False
            elif editUserValidate == "true" or editUserValidate == "True":
                print "Active true"
                editUserValidate = True
            else:
                print "Error type"
                return "error"
    
            if p3t4ControllerUsers.CheckToken(token):
                
                challengeResult = p3t4ControllerChallenges.FindByIDEditChallenge(editChallengeID, editUserScore, editUserValidate, editUserCreator)
                if challengeResult == False:
                    return "error"

                return challengeResult
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/admin/challenges/delete/<challengeID>', methods=['GET', 'POST'])
def service_adminDelegeChallenge(challengeID):

    if request.method == 'GET':
        
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                challenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                if challenge == False:
                    return "error"

                packet = {
                    "titulo": challenge['titulo'],
                    "id": challenge['_id']
                }

                return jsonify(packet)
            else:
                "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
        
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                result = p3t4ControllerChallenges.FindByIdDeleteChallenge(challengeID)
                if result == False:
                    return "error"

                return result
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/public/challenge', methods=['GET', 'POST'])
def service_subchallenge():

    if request.method == 'GET':

        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)

        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            
            data = p3t4ControllerUsers.CheckTokenReturnData(token)
            if data == False:
                return resp
            
            return render_template('publicChallenge.html', data=data)
        else:
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
            
            #if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # datetime
            hora = time.strftime("%H-%M-%S")
            fecha = time.strftime("%d-%m-%y")
            
            nameDate = fecha + "-" + hora + "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], nameDate))

            user = p3t4ControllerUsers.CheckTokenReturnData(token)
            if user == False:
                return resp

            if p3t4ControllerChallenges.SaveChallenge(user['name'], titulo, fecha, puntos, flag, nameDate, descripcion):
                flash("Publicado con exito, a la espera de que un administrador lo valide.", "success")
                return redirect('/public/challenge')
            else:
                flash("No se a podido publicar, ponte en contacto con un administrador.", "danger")
                return redirect('/public/challenge')
        else:
            return resp
            
@app.route('/send/<name>', methods=['GET'])
def service_send_file(name):

    if request.method == 'GET':

        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):
            path = app.config['UPLOAD_FOLDER'] + "\\" + name
            return send_file(path, mimetype="application/x-zip-compressed")
        else:
            return "Token Required"

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