from flask import Flask
from flask_pymongo import PyMongo

import hashlib, json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/p3t4_ctf"
mongo = PyMongo(app)


class P3t4ControllerTeams:

    def __init__(self):
        pass
    

    def CreateTeam(self, tokenUser, teamName):

        try:
            
            if len(teamName) > 30:
                return False

            teamHash = hashlib.sha256(teamName).hexdigest()
            
            """ Create Team """ 
            resultTeamID = mongo.db.teams.insert(
                {
                    "_id": teamHash,
                    "title": teamName,
                    "members": [],
                    "creator": "",
                    "score": 0,
                    "activate": False,
                    "twitter": ""
                }
                
            )
            
            """ Update user creator team """ 
            user = mongo.db.users.find_one_and_update(
                {'token': tokenUser},
                    {'$set': {'team': {
                        "teamName": teamName,
                        "teamID": resultTeamID
                    }}}
            )

            updateTeam = mongo.db.teams.find_one_and_update(
                {'_id': resultTeamID},
                    {'$set': {
                        'creator': user['name']}
                    }
            )

            updateTeam2 = mongo.db.teams.find_one_and_update(
                {'_id': resultTeamID},
                    {'$push': {
                        'members': user['name']}
                    }
            )

            #result = mongo.db.teams.insert(
            #    {
            #        "_id": teamHash,
            #        "title": teamName,
            #        "members": [creator],
            #        "creator": creator,
            #        "score": 0,
            #        "activate": False,
            #        "twitter": ""
            #    }
            #    
            #)

            return True
        except:
            return False
    

    def FindTeamID(self, teamID):
        
        try:
            result = mongo.db.teams.find_one_or_404({'_id': teamID})
            return result
        except:
            return False
    
    def FindTeamMembers(self, members):

        try:
            
            tmpData = []

            for user in members:
                result = mongo.db.users.find_one_or_404({'name': user})
                
                packet = {
                    "name": result['name'],
                    "score": result['puntos'],
                    "twitter": result['twitter']
                }
                tmpData.append(packet)
            
            return tmpData
        except:
            return False

    def FindTeamsTopLimit100(self):
    
        try:
            result = mongo.db.teams.find().sort('score', -1).limit(100)
            return result
        except:
            return False