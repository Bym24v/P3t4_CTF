from flask import Flask
from flask_pymongo import PyMongo

import hashlib, json

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
                return False
        
            if len(password) > 50:
                print "[+] Password require length"
                return False

            result = mongo.db.users.find_one_or_404({"name": name})
            parsePassword = hashlib.sha512(password).hexdigest()
            
            if parsePassword == result['password']:
                print "[+] User Password Match!"
                return True
            else:
                print "[+] Password no Match!"
                return False
        except:
            print "[+] Password no Match!"
            return False
        
    def RegisterUser(self, name, password, email, code):
        
        token = hashlib.sha512(name + password).hexdigest()
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
                            "twitter": "",
                            "team_create": {},
                            "team_member": {}
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
            result = mongo.db.users.delete_one({'_id': userID})
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
                            "twitter": result['twitter'],
                            "activate": result['activate'],
                            "fecha": item['fecha'],
                            "hora": item['hora'],
                            "team_create": result['team_create'],
                            "team_member": result['team_member']
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