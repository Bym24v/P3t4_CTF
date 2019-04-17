var btnEquipo = document.getElementById('create-team');
var btnFollower = document.getElementById('btn-follower')
var btnUnFollower = document.getElementById('btn-unfollower')



if(btnUnFollower != null){

    btnUnFollower.addEventListener('click', function(){

        var ajaxDelete = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(btnUnFollower.getAttribute('name') != ""){

        
            ajaxDelete.open("POST", "/unfollow/" + btnUnFollower.getAttribute('name') ); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data
                        var data = ajaxDelete.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            console.log("Error Create Team");
                        }
                        
                    }
                }
            };

        }

    })
}

if(btnFollower != null){

    btnFollower.addEventListener('click', function(){

        var ajaxDelete = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(btnFollower.getAttribute('name') != ""){

        
            ajaxDelete.open("POST", "/follow/" + btnFollower.getAttribute('name') ); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data
                        var data = ajaxDelete.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            console.log("Error Create Team");
                        }
                        
                    }
                }
            };

        }

    })
}




if(btnEquipo != null){

    btnEquipo.addEventListener('click', function(){
        
        var titleTeam = document.getElementById('title-team');
        
        var ajaxDelete = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(titleTeam.value != ""){

        
            ajaxDelete.open("POST", "/create/team/" + titleTeam.value ); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data
                        var data = ajaxDelete.responseText;
                        
                        if(data === "done"){
                            window.location.reload();
                        }else{
                            //window.location.reload();
                            console.log("Error Create Team");
                            
                        }
                        
                    }
                }
            };

        }
        
    })

}