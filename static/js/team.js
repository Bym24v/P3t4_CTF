var btnFollowerTeam = document.getElementById('btn-follower-team')
var btnUnFollowerTeam = document.getElementById('btn-unfollow-team')

var modUserLeaveTeam = document.getElementById('mod-userLeaveTeam') // modal 
var btnUserLeaveTeam = document.getElementById('btn-userLeave')     // form 


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

