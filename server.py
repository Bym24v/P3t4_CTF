from flask import Flask, render_template, request, redirect, flash, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import hashlib, datetime, os, time

# Upload Folder
UPLOAD_FOLDER = os.getcwd() + '\\public-challenges'
#ALLOWED_EXTENSIONS = set(['.zip'])

# App
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_paco"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Modules Users
from modules.P3t4Users.ControllerUsersDB import P3t4ControllerUsers
p3t4ControllerUsers = P3t4ControllerUsers()

# Modules Challenges
from modules.P3t4Challenges.ControllerChallengesDb import P3t4ControllerChallenges
p3t4ControllerChallenges = P3t4ControllerChallenges()

# Modules Teams
from modules.P3t4Teams.ControllerTeamsDB import P3t4ControllerTeams
p3t4ControllerTeams = P3t4ControllerTeams()

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
        
        try:
            name = request.form['username']
            password = request.form['password']
        except:
            return redirect("/login")
        
        if len(name) > 20:
            return redirect("/login")

        if len(password) > 50:
            return redirect("/login")

        hashPass = hashlib.sha512(password).hexdigest()
        
        # expirate token
        ts = datetime.datetime.utcnow() + datetime.timedelta(days=1)

        user = p3t4ControllerUsers.LoginUser(name, password)

        if user == "done":

            newToken = p3t4ControllerUsers.GenerateNewToken(name, hashPass)
            if newToken == False:
                return redirect("/login")

            resp = make_response(redirect('/challenges'))
            resp.set_cookie('token', newToken, path='/', expires=ts)
            return resp
        elif user == "user":
            flash("El usuario no existe", "user")
            return redirect("/login")
        elif user == "pass":
            flash("El password no coincide", "pass")
            return redirect("/login")
        elif user == "error":
            flash("Error", "error")
            return redirect("/login")

@app.route('/register', methods=['GET', 'POST'])
def service_register():

    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        
        try:
            name = request.form['username']
            password = request.form['password']
            confirmPassword = request.form['confirm-password']
            email = request.form['email']
            code = request.form['code']
        except:
            return redirect('/register')
        
        # revisar
        if password != confirmPassword:
            salida = "Los passwords tienen que ser iguales.".encode('utf-8')
            flash(salida, "error")
            return redirect('/register')
        
        #parseName
        parseName = name.lower()

        # register user
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

        # token
        token = request.cookies.get('token')

        # check token
        if p3t4ControllerUsers.CheckToken(token):

            # data user
            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataUser == False:
                return resp
            
            # data challenge
            dataChallenges = p3t4ControllerChallenges.GetAllChallenges()
            if dataChallenges == False:
                return resp

            return render_template('challenges/challenges.html', dataChallenges=dataChallenges, dataUser=dataUser)
        else:
            return resp

@app.route('/challenge/<challengeID>', methods=['GET', 'POST'])
def service_challenge(challengeID):

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            # data user
            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataUser == False:
                return resp
            
            # data challenge id
            dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
            if dataChallenge == False:
                return resp

            # all users complete challenge
            dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
            if dataAllUsers == False:
                return resp

            return render_template('/challenges/challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
        else:
            return resp
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        try:
            flag = request.form['flag']
        except:
            return resp
        
        if p3t4ControllerUsers.CheckToken(token):
            
            username = p3t4ControllerUsers.FindUserByToken(token)

            if p3t4ControllerChallenges.CheckFlag(username, challengeID, flag):
                
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
                return render_template('/challenges/challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge)
            else:
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                dataChallenge = p3t4ControllerChallenges.GetChallengeByID(challengeID)
                dataAllUsers = p3t4ControllerUsers.FindAllUsersCompleteChallenge(dataChallenge)
                return render_template('/challenges/challenge.html', dataUser=dataUser, dataAllUsers=dataAllUsers, dataChallenge=dataChallenge) 
        else:
            return resp

@app.route('/users')
def service_usuarios():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token 
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            #dataName
            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp
            
            # all user top 100
            dataAll = p3t4ControllerUsers.FindUsersTopLimit100()
            if dataAll == False:
                return resp

            return render_template('/users/users.html', data=dataAll, dataName=dataName)
        else:
            return resp

@app.route('/profile/<name>', methods=['GET', 'POST'])
def service_dashboard(name):
    
    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        # token 
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.CheckTokenByName(name, token):
                
                # local user
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataUser == False:
                    return resp

                return render_template('/profile/profile.html', dataUser=dataUser)
            else:
                
                # dataUser
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataUser == False:
                    return resp

                # view user
                viewUser = p3t4ControllerUsers.FindUserByNameReturnData(name)
                if viewUser == False:
                    return resp

                return render_template('/profile/userView.html', dataUser=dataUser, viewUser=viewUser)
        else:
            return resp

    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        # revisar
        #try:
        #    oldPassword = request.form['old-password']
        #    newPassword = request.form['new-password']
        #    confirmPassword = request.form['confirm-password']
        #
        #    if len(oldPassword) > 50 or len(newPassword) > 50 or len(confirmPassword) > 50:
        #        return "error length"
        #    
        #    if newPassword != confirmPassword:
        #        return "error confim"
        #except:
        #    return resp
    
        # check user
        if p3t4ControllerUsers.CheckToken(token):
    
            if p3t4ControllerUsers.CheckTokenByName(name, token):
                
                # local user
                dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataUser == False:
                    return resp
                
                changePass = p3t4ControllerUsers.UserChangePassword(token, oldPassword, newPassword)
                #if changePass == False:
                #    return resp

                return render_template('/profile/profile.html', dataUser=dataUser)
            else:
                return resp
        else:
            return resp

@app.route('/profile/change/password', methods=['GET'])
def service_preChangePassword():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token 
        token = request.cookies.get('token')

        tokenPassword = request.cookies.get('token-password')

        if p3t4ControllerUsers.CheckToken(token):

            #dataName
            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp
            
            if tokenPassword:

                return redirect('/profile/change/password/' + tokenPassword)
            else:
                
                # expirate token
                ts = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)

                tokenPass = hashlib.sha512(str(ts)).hexdigest()

                if p3t4ControllerUsers.SaveTokenPassword(token, tokenPass):
                    resp3 = make_response(redirect('/profile/change/password/' + tokenPass))
                    resp3.set_cookie('token-password', tokenPass, path='/profile/change/password', expires=ts)
                    return resp3
                else:
                    return resp
            
        else:
            return resp

@app.route('/profile/change/password/<tokenPass>', methods=['GET', 'POST'])
def service_changePassword(tokenPass):

     # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token 
        token = request.cookies.get('token')
        
        tokenPassword = request.cookies.get('token-password')

        if p3t4ControllerUsers.CheckToken(token):

            #dataName
            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp

            if(tokenPass == tokenPassword):
                return render_template('/profile/changePassword.html', dataUser=dataName)
            else:
                return redirect('/profile/' + dataName['name'])
        else:
            return resp
    
    if request.method == 'POST':

        # token 
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            
            try:
                actualPassword = request.form['actualPassword']
                newPassword = request.form['newPassword']
                confirmNewPassword = request.form['confirmNewPassword']
            except:
                return resp
            
            print actualPassword
            print newPassword
            print confirmNewPassword

            #dataName
            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp
            
            return render_template('/profile/changePassword.html', dataUser=dataName)
        else:
            return resp

@app.route('/profile/activity/<name>')
def service_profileActivity(name):

    

    if request.method == "GET":

        # error response
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', path='/', expires=0)

        # token
        token = request.cookies.get('token')

        # check user
        if p3t4ControllerUsers.CheckToken(token):
    
            data = p3t4ControllerUsers.GetChartActivity(name)
            if data == False:
                return "Error"

            return jsonify(data)
        else:
            return resp

""" Admin """
@app.route('/admin')
def service_admin():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                # dataName
                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataName == False:
                    return resp

                # all users
                dataAll = p3t4ControllerUsers.FindAllUsersSort()
                if dataAll == False:
                    return resp
                
                return render_template('/admin/admin.html', data=dataAll, dataName=dataName)
            else:
                return resp
        else:
            return resp

@app.route('/admin/edit/<userID>', methods=['GET', 'POST'])
def service_editUser(userID):
    
    if request.method == 'GET':
        
        # token
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

        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            try:
                editUserName = request.form['mod-name']
                editUserScore = request.form['mod-score']
                editUserActivate = request.form['mod-activate']
                editUserAdmin = request.form['mod-admin']
            except:
                return "error"
            
            # check activate
            if editUserActivate == "false" or editUserActivate == "False":
                editUserActivate = False
            elif editUserActivate == "true" or editUserActivate == "True":
                editUserActivate = True
            else:
                return "error"

            # check admin
            if editUserAdmin == "false" or editUserAdmin == "False":
                editUserAdmin = False
            elif editUserAdmin == "true" or editUserAdmin == "True":
                editUserAdmin = True
            else:
                return "error"

            if p3t4ControllerUsers.CheckToken(token):
                
                # user Result
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

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                # dataUser 
                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataName == False:
                    return resp
                
                # dataAll
                dataAll = p3t4ControllerChallenges.GetAllChallenges()
                if dataAll == False:
                    return resp

                return render_template('/admin/adminChallenge.html', data=dataAll, dataName=dataName)
            else:
                return resp
        else:
            return resp

@app.route('/admin/challenges/edit/<challengeID>',  methods=['GET', 'POST'])
def service_adminChallengesEdit(challengeID):

    if request.method == 'GET':

        # token 
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
        
        # token
        token = request.cookies.get('token')
    
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            try:
                editChallengeID = request.form['mod-challengeID']
                editUserScore = request.form['mod-score']
                editUserValidate = request.form['mod-validate']
                editUserCreator = request.form['mod-creator']
            except:
                return "error"
            
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
        
        # token
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
        
        # token
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

@app.route('/teams', methods=['GET'])
def service_teams():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            # dataName
            dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataName == False:
                return resp
            
            # all teams
            teamsAll = p3t4ControllerTeams.FindTeamsTopLimit100()
            if teamsAll == False:
                return resp

            return render_template('/teams/teams.html', teams=teamsAll, dataName=dataName)
        else:
            return resp

""" admin teams """ 
@app.route('/admin/teams')
def service_adminTeams():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        #token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                # dataName
                dataName = p3t4ControllerUsers.CheckTokenReturnData(token)
                if dataName == False:
                    return resp
                
                # dataAll
                dataAll = p3t4ControllerTeams.FindAllTeams()
                if dataAll == False:
                    return resp

                return render_template('/admin/adminTeams.html', data=dataAll, dataName=dataName)
            else:
                return resp
        else:
            print "Admin Require"
            return resp

@app.route('/admin/teams/edit/<teamID>', methods=['GET', 'POST'])
def service_adminTeamEdit(teamID):
    
    if request.method == 'GET':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            if p3t4ControllerUsers.CheckToken(token):

                team = p3t4ControllerTeams.FindTeamID(teamID)
                if team == False:
                    return "error"

                newPacket = {
                    "id": team['_id'],
                    "score": team['score'],
                    "activate": team['activate'],
                    "creator": team['creator']
                }

                return jsonify(newPacket)
            else:
                return "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
    
        if p3t4ControllerUsers.CheckTokenAdmin(token):
            
            # revisar
            try:
                editTeamID = request.form['mod-teamID']
                editTeamScore = request.form['mod-score']
                editTeamValidate = request.form['mod-validate']
                editTeamCreator = request.form['mod-creator']
            except:
                return "error"
            
            # check activate
            if editTeamValidate == "false" or editTeamValidate == "False":
                print "Active false"
                editTeamValidate = False
            elif editTeamValidate == "true" or editTeamValidate == "True":
                print "Active true"
                editTeamValidate = True
            else:
                print "Error type"
                return "error"
    
            if p3t4ControllerUsers.CheckToken(token):
                
                # challenge edit result
                challengeResult = p3t4ControllerTeams.AdminTeamEdit(editTeamID, editTeamScore, editTeamValidate, editTeamCreator)
                if challengeResult == False:
                    return "error"

                return challengeResult
            else:
                return "error"
        else:
            return "Admin Require"

@app.route('/admin/teams/delete/<teamID>', methods=['GET', 'POST'])
def service_adminTeamDelete(teamID):
    
    if request.method == 'GET':
        
        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                team = p3t4ControllerTeams.FindTeamID(teamID)
                if team == False:
                    return "error"

                packet = {
                    "title": team['title'],
                    "id": team['_id']
                }

                return jsonify(packet)
            else:
                "error"
        else:
            return "Admin Require"
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckTokenAdmin(token):

            if p3t4ControllerUsers.CheckToken(token):
                
                result = p3t4ControllerTeams.AdminDeleteTeam(teamID)
                if result == False:
                    return "error"

                return result
            else:
                return "error"
        else:
            return "Admin Require"

""" team """ 
@app.route('/team/<teamID>', methods=['GET'])
def service_team(teamID):
    
    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            # dataUser
            dataUser = p3t4ControllerUsers.CheckTokenReturnData(token)
            if dataUser == False:
                return resp

            # team
            team = p3t4ControllerTeams.FindTeamID(teamID)
            if team == False:
                return resp

            # members in Team
            membersTeam = p3t4ControllerTeams.FindTeamMembers(team['members'])
            if membersTeam == False:
                return resp

            return render_template('/teams/team.html', team=team, teamMembers=membersTeam, dataUser=dataUser)
        else:
            return resp

@app.route('/create/team/<name>', methods=['POST'])
def service_createTeam(name):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerTeams.CreateTeam(token, name):
                return "done"
            else:
                return "error"
        else:
            return "Error token"

""" owner delete team """
@app.route('/delete/team', methods=['POST'])
def service_deleteTeam():
    pass

""" Leave member in team """
@app.route('/user/leave/team/<teamID>', methods=['POST'])
def service_userLeaveTeam(teamID):
    
    if request.method == 'POST':
        
        #token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.UserLeaveTeam(token, teamID):
                return "done"
            else:
                return "error"
        else:
            return "Error token"


"""  owner add user team """
@app.route('/owner/team/add/user', methods=['POST'])
def service_ownerRemoveTeam():
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        try:
            teamID = request.form['mod-teamID']
            username = request.form['mod-username']
        except:
            return "error"

        if len(username) > 30:
            return "error"
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerTeams.AddMemberTeam(token, teamID, username):
                return "done"
            else:
                return "error"
        else:
            return "Error token"


"""  owner team delete users"""
@app.route('/owner/team/remove/user/<userID>', methods=['POST'])
def service_ownerTeamRemoveUser(userID):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
                
            result = p3t4ControllerTeams.DeleteUserInTeam(token, userID)
            if result == False:
                return "error"

            return result
        else:
            return "error"


""" followers users """ 
@app.route('/follow/<name>', methods=['POST'])
def service_follow(name):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.FindUserAddFollower(token, name):
                return "done"
            else:
                return "error"
        else:
            return "Error token"

@app.route('/unfollow/<name>', methods=['POST'])
def service_unfollow(name):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.FindUserUnFollower(token, name):
                return "done"
            else:
                return "error"
        else:
            return "Error token"


""" followers teams """
@app.route('/team/follow/<teamID>', methods=['POST'])
def service_followTeam(teamID):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.FindTeamAddFollower(token, teamID):
                return "done"
            else:
                return "error"
        else:
            return "Error token"

@app.route('/team/unfollow/<teamID>', methods=['POST'])
def service_unfollowTeam(teamID):
    
    if request.method == 'POST':
        
        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):

            if p3t4ControllerUsers.FindTeamUnFollower(token, teamID):
                return "done"
            else:
                return "error"
        else:
            return "Error token"


""" Public challenge """ 
@app.route('/public/challenge', methods=['GET', 'POST'])
def service_subchallenge():

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            
            # data
            data = p3t4ControllerUsers.CheckTokenReturnData(token)
            if data == False:
                return resp
            
            return render_template('/challenges/publicChallenge.html', data=data)
        else:
            return resp

    if request.method == "POST":

        if 'file' not in request.files:
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')
        
        try:
            file = request.files['file']
        except:
            return resp

        if file.content_type != "application/x-zip-compressed":
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')

        if file.filename == '':
            flash('Archivo no valido.', "danger")
            return redirect('/public/challenge')
        
        try:
            titulo = request.form['titulo']
            categoria = request.form['categoria']
            plataforma = request.form['plataforma']
            puntos = request.form['puntos']
            flag = request.form['flag']
            descripcion = request.form['descripcion']
        except:
            return resp
        

        if titulo == '' or len(titulo) > 25:
            flash("Titulo no valido.", "danger")
            return redirect('/public/challenge')
        
        if categoria == '' or len(categoria) > 10:
            flash("Puntos no validos.", "danger")
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
        
        # token
        token = request.cookies.get('token')

        if p3t4ControllerUsers.CheckToken(token):
            
            # filename
            filename = secure_filename(file.filename)
            
            # datetime
            hora = time.strftime("%H-%M-%S")
            fecha = time.strftime("%d-%m-%y")
            
            try:
                newName = fecha + "-" + hora + "_" + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], newName))
            except:
                return resp
            
            user = p3t4ControllerUsers.CheckTokenReturnData(token)
            if user == False:
                return resp

            if p3t4ControllerChallenges.SaveChallenge(user['name'], titulo, fecha, categoria, plataforma, puntos, flag, newName, descripcion):
                flash("Publicado con exito, a la espera de que un administrador lo valide.", "success")
                return redirect('/public/challenge')
            else:
                flash("No se a podido publicar, ponte en contacto con un administrador.", "danger")
                return redirect('/public/challenge')
        else:
            return resp

""" Send file cahllenge """ 
@app.route('/send/<name>', methods=['GET'])
def service_send_file(name):

    # error response
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', path='/', expires=0)

    if request.method == 'GET':

        # token
        token = request.cookies.get('token')
        
        if p3t4ControllerUsers.CheckToken(token):
            path = app.config['UPLOAD_FOLDER'] + "\\" + name
            
            # check file
            if os.path.isfile(path):
                return send_file(path, mimetype="application/x-zip-compressed")
            else:
                print "File not found"
                return redirect('/challenges')
        else:
            print "Token Required"
            return resp



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)