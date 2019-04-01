from flask import Flask
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)

class P3t4ControllerChallenges:

    def GetAllChallenges(self):
        
        try:
            result = mongo.db.challenges.find()
            return result
        except:
            return False
    
    def SaveChallenge(self, creador, titulo, fecha, puntos, flag, nameZip, resumen):
  
        try:
            
            hashFlag = hashlib.sha256(flag).hexdigest()

            parse = int(puntos, 10) * 10
            progressType = ""

            if parse > 0 and parse <= 30:
                progressType = "success"    
            
            if parse > 30 and parse <= 60:
                progressType = "info"

            if parse > 60 and parse <= 80:
                progressType = "warning"
            
            if parse > 80 and parse <= 100:
                progressType = "danger"
                
            result = mongo.db.challenges.insert({

                "_id": hashlib.sha256(titulo).hexdigest(),
                "creador": creador,
                "titulo": titulo,
                "fecha": fecha,
                "puntos": parse,
                "challenge_type": progressType,
                "flag": hashFlag,
                "zip": nameZip,
                "descripcion": resumen,
                "validado": False,
                "completado_users": []
            })

            return True
        except:
            return False
    
    def GetChallengeByID(self, challengeID):

        try:
            result = mongo.db.challenges.find_one_or_404({'_id': challengeID})
            return result
        except:
            return False
    
    """ Challenge Edit""" 
    def FindByIDEditChallenge(self, challengeID, new_puntos, new_validado, new_creador):

        if len(new_puntos) <= 6 and len(new_creador) <= 30:
    
            try:
                mongo.db.challenges.find_one_and_update(
                    {'_id': challengeID},
                    {'$set': {
                        'puntos': int(new_puntos, 10),
                        'validado': new_validado,
                        'creador': new_creador}
                    }
                )
                return "done"
            except:
                return "error"

    """ End Challenge Edit """


    """ Challenge Delete  """

    def FindByIdDeleteChallenge(self, challengeID):

        try:
            result = mongo.db.challenges.delete_one({'_id': challengeID})
            print result
            return "done"
        except:
            return "error"

    """ End Delete Challenge"""
    def CheckFlag(self, username, challengeID, flag):

        try:
            result = mongo.db.challenges.find_one_or_404({'_id': challengeID})

            hashFlag = hashlib.sha256(flag).hexdigest()

            if result['flag'] == hashFlag:
                
                print "[+] Flag Found!"

                if not username in result['completado_users']:  

                    mongo.db.challenges.find_one_and_update(
                        {'_id': challengeID},
                        {'$push': {'completado_users': username}}
                    )

                    mongo.db.users.find_one_and_update(
                        {'name': username},
                        {'$inc': {'puntos': result['puntos']}}
                    )

                return True
            else:
                print "[+] Flag not Found!"
                return False
        except:
            print "[+] Flag not Found!"
            return False