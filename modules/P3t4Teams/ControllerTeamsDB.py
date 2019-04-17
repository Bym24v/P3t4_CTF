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
                    "followers": [],
                    "creator": "",
                    "score": 0,
                    "activate": False
                }
                
            )
            
            """ Update user creator team """ 
            user = mongo.db.users.find_one_and_update(
                {'token': tokenUser},
                    {'$set': {'team_create': {
                        "name": teamName,
                        "id": resultTeamID
                    }}}
            )

            """ Update user member team """ 
            user = mongo.db.users.find_one_and_update(
                {'token': tokenUser},
                    {'$set': {'team_member': {
                        "name": teamName,
                        "id": resultTeamID
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
                        'members': user['name'],
                        'followers': user['name']}
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
    
    def FindAllTeams(self):
        
        try:
            result = mongo.db.teams.find()
            return result
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
                    "flags": result['completado_challenges']
                }
                tmpData.append(packet)
            
            return tmpData
        except:
            return False

    def FindTeamMembersTotalScore(self, members):

        try:
            
            tmpData = 0

            for user in members:
                result = mongo.db.users.find_one_or_404({'name': user})
                tmpData += result['puntos']
            
            package = {
                "score": tmpData
            }

            return package
        except:
            return False

    """ admin edit team """ 
    def AdminTeamEdit(self, teamID, new_score, new_activate, new_creator):

        if len(new_score) <= 6 and len(new_creator) <= 30:
        
            try:
                mongo.db.teams.find_one_and_update(
                    {'_id': teamID},
                    {'$set': {
                        'score': int(new_score, 10),
                        'activate': new_activate,
                        'creator': new_creator}
                    }
                )
                return "done"
            except:
                return False

    def AdminDeleteTeam(self, teamID):

        try:

            team = mongo.db.teams.find_one_or_404({'_id': teamID})

            mongo.db.users.find_one_and_update(
                {'name': team['creator']},
                {'$set': {'team_create': {}}}
            )

            mongo.db.users.find_one_and_update(
                {'name': team['creator']},
                {'$set': {'team_member': {}}}
            )

            result = mongo.db.teams.delete_one({'_id': teamID})
            return "done"
        except:
            return "error"
    
    def AddMemberTeam(self):
        pass

    def DeleteUserInTeam(self):
        pass

    def FindTeamsTopLimit100(self):
    
        try:
            result = mongo.db.teams.find().sort('score', -1).limit(100)
            return result
        except:
            return False