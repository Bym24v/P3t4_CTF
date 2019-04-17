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
                    "id": result['_id'],
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

    """ admin teams """ 
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

            # owner team
            mongo.db.users.find_one_and_update(
                {'name': team['creator']},
                {'$set': {'team_create': {}}}
            )

            mongo.db.users.find_one_and_update(
                {'name': team['creator']},
                {'$set': {'team_member': {}}}
            )

            for user in team['members']:
                
                mongo.db.users.find_one_and_update(
                    {'name': user},
                    {'$set': {'team_member': {}}}
                )


            result = mongo.db.teams.delete_one({'_id': teamID})
            return "done"
        except:
            return False
    
    """ owner team """
    def AddMemberTeam(self, token, teamID, username):
        
        try:

            ownerTeam = mongo.db.users.find_one_or_404({'token': token})
            team = mongo.db.teams.find_one_or_404({'_id': teamID})
            user = mongo.db.users.find_one_or_404({'name': username})
            
            # user is activate ? 
            if user['activate']:

                # user in not team and not owner team
                if len(user['team_create']) == 0 and len(user['team_member']) == 0:

                    # check owner team and token 
                    if team['creator'] == ownerTeam['name']:
                    
                        # user in not team 
                        if not username in team['members'] and len(team['members']) <= 9:

                            mongo.db.teams.find_one_and_update(
                                {'_id': teamID},
                                {'$push': {'members': username}}
                            )

                            mongo.db.users.find_one_and_update(
                                {'_id': user['_id']},
                                    {'$set': {'team_member': {
                                        "name": team['title'],
                                        "id": team['_id']
                                    }}}
                            )
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except:
            return False

    def DeleteTeam(self, token):

        try:

            user = mongo.db.users.find_one_or_404({'token': token})
            #team = mongo.db.users.find_one_or_404({'': token})

            print user['team_create']['name']


            # owner team
            #mongo.db.users.find_one_and_update(
            #    {'name': team['creator']},
            #    {'$set': {'team_create': {}}}
            #)
            #
            #mongo.db.users.find_one_and_update(
            #    {'name': team['creator']},
            #    {'$set': {'team_member': {}}}
            #)
            #
            #for user in team['members']:
            #    
            #    mongo.db.users.find_one_and_update(
            #        {'name': user},
            #        {'$set': {'team_member': {}}}
            #    )


            #result = mongo.db.teams.delete_one({'_id': teamID})
            return True
        except:
            return False

    def DeleteUserInTeam(self, token, userID):
        
        try:
            
            # owner team 
            ownerTeam = mongo.db.users.find_one_or_404({"token": token})
            
            # team
            team = mongo.db.teams.find_one_or_404({"_id": ownerTeam['team_create']['id']})
            
            # user delete
            userDelete = mongo.db.users.find_one_or_404({'_id': userID})

            if userDelete['name'] in team['members']:
                
                mongo.db.teams.find_one_and_update(
                    {"_id": ownerTeam['team_create']['id']},
                    {'$pull': {'members': userDelete['name']}}
                )
                
                mongo.db.users.find_one_and_update(
                    {'_id': userID},
                    {'$set': {'team_member': {}}}
                )

            return "done"
        except:
            return False

    def FindTeamsTopLimit100(self):
    
        try:
            result = mongo.db.teams.find().sort('score', -1).limit(100)
            return result
        except:
            return False