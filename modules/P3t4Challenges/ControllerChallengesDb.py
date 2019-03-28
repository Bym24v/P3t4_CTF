from flask import Flask
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)

class P3t4ControllerChallenges:

    def GetAllChallenges(self):
        
        try:
            result = mongo.db.challenges.find().sort("puntos", -1)
            return result
        except:
            return "error"
    
    def SaveChallenge(self, creador, titulo, puntos, flag, nameZip, resumen):
        
        try:

            parsePuntos = int(puntos, 10) * 10

            result = mongo.db.challenges.insert({

                "_id": hashlib.sha256(titulo).hexdigest(),
                "creador": creador,
                "titulo": titulo,
                "puntos": parsePuntos,
                "flag": flag,
                "zip": nameZip,
                "descripcion": resumen,
                "validado": False
            })

            return True
        except:
            return False
