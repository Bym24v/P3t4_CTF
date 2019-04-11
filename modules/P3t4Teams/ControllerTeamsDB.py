from flask import Flask
from flask_pymongo import PyMongo

import hashlib, json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)


class P3t4ControllerTeams:

    def __init__(self):
        pass
    

    def CreateTeam(self, creator, teamName):

        try:
            
            if len(creator) > 30 or len(teamName) > 30:
                return False


            teamHash = hashlib.sha256(teamName).hexdigest()

            result = mongo.db.teams.insert(
                {
                    "_id": teamHash,
                    "title": teamName,
                    "members": [creator],
                    "creator": creator,
                    "score": 0,
                    "activate": False,
                    "twitter": ""
                }
                
            )

            return True
        except:
            return False
    

    def FindTeamID(self, teamID):
        pass
    

    def FindTeamsTopLimit100(self):
    
        try:
            result = mongo.db.teams.find().sort('score', -1).limit(100)
            return result
        except:
            return False