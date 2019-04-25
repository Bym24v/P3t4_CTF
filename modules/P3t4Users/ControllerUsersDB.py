from flask import Flask
from flask_pymongo import PyMongo

import hashlib, json, time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)


class P3t4ControllerUsers:

    def __init__(self):
        pass
    
    def LoginUser(self, name, password):
        
        try:

            if len(name) > 30:
                print "[+] Name require length"
                return "error"
        
            if len(password) > 50:
                print "[+] Password require length"
                return "error"

            user = mongo.db.users.find_one_or_404({"name": name})
            hashPass = hashlib.sha512(password).hexdigest()
            
            if user['password'] == hashPass:
                print "[+] User Password Match!"
                return "done"
            else:
                print "[+] Password no Match!"
                return "pass"
        except:
            print "[+] User no Match!"
            return "user"
        
    def RegisterUser(self, name, password, email, code):
        
        # datetime
        hora = time.strftime("%H-%M-%S")
        fecha = time.strftime("%d-%m-%y")

        token = hashlib.sha512(name + str(fecha) + str(hora)).hexdigest()
        parseID = hashlib.sha256(name).hexdigest()
        parsePassword = hashlib.sha512(password).hexdigest()


        if code == "28" and len(code) <= 10:

            if len(name) <= 30 and len(email) <= 50 and len(password) <= 50:
            
                try:
                    
                    result = mongo.db.users.insert(
                        {
                            "_id": parseID,
                            "avatar": "", 
                            "name": name,
                            "password": parsePassword,
                            "email": email,
                            "token": token,
                            "activate": False,
                            "admin": False,
                            "puntos": 0,
                            "completado_challenges": [],
                            "followers": [],
                            "team_create": {},
                            "team_member": {},
                            "register_date": fecha
                        }
                    )

                    print "[+] Register User Done!"
                    return "done"
                except:
                    print "[+] Error Register User"
                    return "error"
            else:
                print "[+] Error Register minimun require"
                return "require"
        else:
            print "[+] Error Register code require"
            return "code"
    
    def GenerateNewToken(self, name, hashPass):

        try:

            # datetime
            hora = time.strftime("%H-%M-%S")
            fecha = time.strftime("%d-%m-%y")

            # user
            user = mongo.db.users.find_one_or_404({'name': name})

            # new token
            newToken = hashlib.sha512(name + str(fecha) + str(hora)).hexdigest()

            if user['password'] == hashPass:
                
                mongo.db.users.find_one_and_update(
                    {'_id': user['_id']},
                    {'$set': {'token': newToken}}
                )

            return newToken
        except:
            return False


    """ change password """
    def UserChangePassword(self, token, old_pass, new_pass):

        try:
            user = mongo.db.users.find_one_or_404({'token': token})

            oldHashPass = hashlib.sha512(old_pass).hexdigest()
            newHashPass = hashlib.sha512(newHashPass).hexdigest()
            newToken = hashlib.sha512(name + newHashPass).hexdigest()

            if user['password'] == oldHashPass:
                
                mongo.db.users.find_one_and_update(
                    {'_id': user['_id']},
                    {'$set': {'password': newHashPass}}
                )

            return True
        except:
            return False

    """ User """
    def CheckToken(self, token):

        try:
            result = mongo.db.users.find_one_or_404({"token": token})
            print "[+] Token Found!"
            return True
        except:
            return False
    
    def CheckTokenAdmin(self, token):

        try:
            result = mongo.db.users.find_one_or_404({"token": token})
            
            if result['admin'] == True:
                print "[+] Check admin Found!"
                return True
            else:
                print "[+] Error Check admin"
                return False
        except:
            print "[+] Error Check admin"
            return False

    def CheckTokenReturnData(self, token):
    
        try:
            result = mongo.db.users.find_one_or_404({"token": token})
            return result
        except:
            return False

    def CheckTokenByName(self, name, token):
    
        try:
            result = mongo.db.users.find_one_or_404({"name": name})
            
            if result['token'] == token:
                print "[+] Token ByName Found!"
                return True
            else:
                print "[+] Token ByName no Found"
                return False
        except:
            print "[+] Token ByName no Found"
            return False

    def FindUserByNameReturnData(self, name):
        
        try:
            result = mongo.db.users.find_one_or_404({'name': name})
            return result
        except:
            return False
    
    def FindUserNameReturnID(self, name):

        try:
            result = mongo.db.users.find_one_or_404({'name': name})
            return result['_id']
        except:
            return False
        
    """ End User """

    """ Delete User Api """

    def FindUserIdReturnDelete(self, userID):

        try:
            result = mongo.db.users.find_one_or_404({'_id': userID})
            return result['name']
        except:
            return False

    def FindUserIdDeleteUser(self, userID):
    
        try:

            user = mongo.db.users.find_one_or_404({'_id': userID})

            for challenge in user['completado_challenges']:
                
                #challengeID = mongo.db.challenges.find_one_or_404({'_id': challenge})

                mongo.db.challenges.find_one_and_update(
                    {"_id": challenge},
                    {'$pull': {'completado_users': {'name': user['name']}}}
                )

            mongo.db.users.delete_one({'_id': userID})
            
            return "done"
        except:
            return False
    
    """ End Delete User """

    """ Edit User Api """ 

    def FindUserIdReturnEdit(self, userID):
    
        try:
            result = mongo.db.users.find_one_or_404({'_id': userID})
            return result
        except:
            return False

    def FindUserIdEditUser(self, userID, new_puntos, new_activate, new_admin):
        

        if len(new_puntos) <= 6:

            try:
                mongo.db.users.find_one_and_update(
                    {'_id': userID},
                    {'$set': {
                        'puntos': int(new_puntos, 10),
                        'activate': new_activate,
                        'admin': new_admin}
                    }
                )
                
                return "done"
            except:
                return False

    """ End Edit User """

    """ Challenge """ 
    def FindUsersTopLimit100(self):

        try:
            result = mongo.db.users.find().sort('puntos', -1).limit(100)
            return result
        except:
            return False
    
    def FindAllUsersCompleteChallenge(self, dataUers):

        salida = []

        for key, value in dataUers.iteritems():
            
            if key == 'completado_users':
            
                for item in value:
                    
                    try:
                        result = mongo.db.users.find_one_or_404({'name': item['name']})
                        
                        newUser = {
                            "name": result['name'],
                            "puntos": result['puntos'],
                            "activate": result['activate'],
                            "fecha": item['fecha'],
                            "hora": item['hora'],
                            "team_create": result['team_create'],
                            "team_member": result['team_member'],
                            "completado_challenges": result['completado_challenges']
                        }
                        
                        salida.append(newUser)
                    except:
                        return False
        return salida

    def FindUserByToken(self, token):

        try:
            result = mongo.db.users.find_one_or_404({'token': token})
            return result['name']
        except:
            return False

    """ End Challenge """

    """ Admin """
    def FindAllUsersSort(self):
    
        try:
            result = mongo.db.users.find().sort('puntos', -1)
            return result
        except:
            return False

    """ end Admin """

    """ Home Top Users """ 
    def FindTopTresUsers(self):

        try:
            result = mongo.db.users.find().sort('puntos', -1).limit(3)
            return result
        except:
            return False

    
    """ followers user """
    def FindUserAddFollower(self, token, user_follow):
        
        try:

            if len(user_follow) > 30:
                return False

            userFollower = mongo.db.users.find_one_or_404({"token": token})
        
            user = mongo.db.users.find_one_or_404({'name': user_follow})
            
            if not userFollower['name'] in user['followers']:

                mongo.db.users.find_one_and_update(
                    {"name": user_follow},
                    {'$push': {'followers': userFollower['name']}}
                )
            return True
        except:
            return False

    def FindUserUnFollower(self, token, user_unfollow):
        
        try:

            if len(user_unfollow) > 30:
                return False

            userFollower = mongo.db.users.find_one_or_404({"token": token})

            user = mongo.db.users.find_one_or_404({'name': user_unfollow})
            
            if userFollower['name'] in user['followers']:

                mongo.db.users.find_one_and_update(
                    {"name": user_unfollow},
                    {'$pull': {'followers': userFollower['name']}}
                )
            return True
        except:
            return False
    
    """ follower team """ 
    def FindTeamAddFollower(self, token, team_follow):
        
        try:

            userFollower = mongo.db.users.find_one_or_404({"token": token})
        
            team = mongo.db.teams.find_one_or_404({'_id': team_follow})
            
            if not userFollower['name'] in team['followers']:

                mongo.db.teams.find_one_and_update(
                    {"_id": team_follow},
                    {'$push': {'followers': userFollower['name']}}
                )
            return True
        except:
            return False

    def FindTeamUnFollower(self, token, team_unfollow):
        
        try:

            userFollower = mongo.db.users.find_one_or_404({"token": token})

            team = mongo.db.teams.find_one_or_404({'_id': team_unfollow})
            
            if userFollower['name'] in team['followers']:

                mongo.db.teams.find_one_and_update(
                    {"_id": team_unfollow},
                    {'$pull': {'followers': userFollower['name']}}
                )
            return True
        except:
            return False

    """ user leave team  """ 
    def UserLeaveTeam(self, token, teamID):

        try:

            userLeave = mongo.db.users.find_one_or_404({"token": token})

            team = mongo.db.teams.find_one_or_404({'_id': teamID})
            
            if userLeave['name'] in team['members']:

                mongo.db.teams.find_one_and_update(
                    {"_id": teamID},
                    {'$pull': {'members': userLeave['name']}}
                )

                mongo.db.users.find_one_and_update(
                    {'token': token},
                    {'$set': {'team_member': {}}}
                )

                #mongo.db.teams.find_one_and_update(
                #    {"_id": teamID},
                #    {'$pull': {'followers': userLeave['name']}}
                #)

            return True
        except:
            return False

   