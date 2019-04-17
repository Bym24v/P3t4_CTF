var matchesUsersTeam = document.querySelectorAll("td > button");


var btnFollowerTeam = document.getElementById('btn-follower-team');
var btnUnFollowerTeam = document.getElementById('btn-unfollow-team');

// user leave team 
var modUserLeaveTeam = document.getElementById('mod-userLeaveTeam'); // modal 
var btnUserLeaveTeam = document.getElementById('btn-userLeave');     // form 

// owner add user 
var btnUserAddTeam = document.getElementById('btn-addUserTeam');    // btn add
var modUserAddTeamValue = document.getElementById('mod-userName'); // value modal
var btnUserAddTeamModal = document.getElementById('mod-addUserTeam'); // btn modal

// owner delete user 
var btnOwnerDeleteUserTeam = document.getElementById('btn-ownerDeleteUserTeam');
var modOwnerDeleteUserTeam = document.getElementById('mod-ownerDeleteUserTeam');
var tmpUserID = "";

modOwnerDeleteUserTeam.addEventListener('click', function(){

    var ajaxOwnerDeleteUser = new XMLHttpRequest();
    /*ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);*/

    if(tmpUserID != ""){

        ajaxOwnerDeleteUser.open("POST", "/owner/team/remove/user/" + tmpUserID); 
        ajaxOwnerDeleteUser.send(null)

        ajaxOwnerDeleteUser.onreadystatechange = function () {

            if (ajaxOwnerDeleteUser.readyState == 4) {
                
                // ok
                if (ajaxOwnerDeleteUser.status == 200) {
                    
                    // data
                    var data = ajaxOwnerDeleteUser.responseText;
                    
                    if(data === "done"){  
                        window.location.reload();
                    }else{
                        //$('#addUserModal').modal('hide');
                        console.log("Error delete user team");
                    }
                    
                }
            }
        };

    }
})


/* owner delete team */
for (let i = 0; i < matchesUsersTeam.length; i++) {
    
    matchesUsersTeam[i].addEventListener('click', function(e){
        
        if(matchesUsersTeam[i].getAttribute('name') != ""){

            tmpUserID = matchesUsersTeam[i].getAttribute('name')
            $('#ownerDeleteUserModal').modal('show');
        }
    })
}


/* add user team */
if(btnUserAddTeam != null){

    btnUserAddTeam.addEventListener('click', function(){
        $('#addUserModal').modal('show');
    })
}

if(btnUserAddTeamModal != null){

    btnUserAddTeamModal.addEventListener('click', function(){

        var ajaxAddUserTeam = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(modUserAddTeamValue.value != "" && btnUserAddTeamModal.getAttribute('name') != ""){

        
            ajaxAddUserTeam.open("POST", "/owner/team/add/user"); 

            var formdata = new FormData();
            formdata.append("mod-teamID", btnUserAddTeamModal.getAttribute('name'));
            formdata.append("mod-username", modUserAddTeamValue.value);

            ajaxAddUserTeam.send(formdata)

            ajaxAddUserTeam.onreadystatechange = function () {

                if (ajaxAddUserTeam.readyState == 4) {
                    
                    // ok
                    if (ajaxAddUserTeam.status == 200) {
                        
                        // data
                        var data = ajaxAddUserTeam.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            //$('#addUserModal').modal('hide');
                            console.log("Error add user team");
                        }
                        
                    }
                }
            };

        }

    })
}


/*leave user team */
if(btnUserLeaveTeam != null){

    btnUserLeaveTeam.addEventListener('click', function(){
        $('#userLeaveModal').modal('show');
    })
}

if(modUserLeaveTeam != null){

    modUserLeaveTeam.addEventListener('click', function(){
        
        var ajaxUserLeave = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(modUserLeaveTeam.getAttribute('name') != ""){

        
            ajaxUserLeave.open("POST", "/user/leave/team/" + modUserLeaveTeam.getAttribute('name') ); 
            ajaxUserLeave.send(null)

            ajaxUserLeave.onreadystatechange = function () {

                if (ajaxUserLeave.readyState == 4) {
                    
                    // ok
                    if (ajaxUserLeave.status == 200) {
                        
                        // data
                        var data = ajaxUserLeave.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            console.log("Error leave team");
                        }
                        
                    }
                }
            };

        }

    })
}


/* Follower */
if(btnUnFollowerTeam != null){

    btnUnFollowerTeam.addEventListener('click', function(){
        
        var ajaxUnFollow = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(btnUnFollowerTeam.getAttribute('name') != ""){

        
            ajaxUnFollow.open("POST", "/team/unfollow/" + btnUnFollowerTeam.getAttribute('name') ); 
            ajaxUnFollow.send(null)

            ajaxUnFollow.onreadystatechange = function () {

                if (ajaxUnFollow.readyState == 4) {
                    
                    // ok
                    if (ajaxUnFollow.status == 200) {
                        
                        // data
                        var data = ajaxUnFollow.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            console.log("Error unfollow team");
                        }
                        
                    }
                }
            };

        }

    })
}

if(btnFollowerTeam != null){

    btnFollowerTeam.addEventListener('click', function(){

        var ajaxFollow = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(btnFollowerTeam.getAttribute('name') != ""){

        
            ajaxFollow.open("POST", "/team/follow/" + btnFollowerTeam.getAttribute('name') ); 
            ajaxFollow.send(null)

            ajaxFollow.onreadystatechange = function () {

                if (ajaxFollow.readyState == 4) {
                    
                    // ok
                    if (ajaxFollow.status == 200) {
                        
                        // data
                        var data = ajaxFollow.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            console.log("Error follow team");
                        }
                        
                    }
                }
            };

        }

    })
}

