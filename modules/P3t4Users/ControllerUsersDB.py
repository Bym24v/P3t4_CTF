from flask import Flask
from flask_pymongo import PyMongo

import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)


class P3t4ControllerUsers:

    def __init__(self):
        pass
    
    def LoginUser(self, name, password):
        
        try:
            result = mongo.db.users.find_one_or_404({"name": name})
            parsePassword = hashlib.sha512(password).hexdigest()
            
            if result == None:
                return False

            if parsePassword == result['password']:
                print "[+] User Found!"
                return True
        except:
            return False
        
        return False

    def RegisterUser(self, name, password, email, code):
        
        token = hashlib.sha512(name + password).hexdigest()
        parseID = hashlib.sha256(name).hexdigest()
        parsePassword = hashlib.sha512(password).hexdigest()

        if code == "28":

            if len(name) <= 30 and len(email) <= 50:
            
                try:
                    
                    result = mongo.db.users.insert(
                        {
                            "_id": parseID,
                            "name": name,
                            "password": parsePassword,
                            "email": email,
                            "token": token,
                            "avatar": "",
                            "activate": False,
                            "twitter": "Bym24v_cls",
                            "telegram": "Bym24v"
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
    
    def CheckToken(self, token):

        try:
            result = mongo.db.users.find_one_or_404({"token": token})
            print "[+] Token Found!"
            return True
        except:
            False

        
    def GetProfile(self):
        pass
    
    def FindUserName(self):
        pass