
var btnEquipo = document.getElementById('create-team');
var btnFollower = document.getElementById('btn-follower');
var btnUnFollower = document.getElementById('btn-unfollower');

    
// Un Follow
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

// Follow
if(btnFollower != null){

    btnFollower.addEventListener('click', function(){

        var ajaxDelete = new XMLHttpRequest();
        /*ajax.upload.addEventListener("progress", progressHandler, false);
        ajax.addEventListener("load", completeHandler, false);
        ajax.addEventListener("error", errorHandler, false);
        ajax.addEventListener("abort", abortHandler, false);*/

        if(btnFollower.getAttribute('name') != ""){

        
            ajaxDelete.open("POST", "/follow/" + btnFollower.getAttribute('name')); 
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


// Create Team
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



var tmpObject;

// profile
if(btnFollower == null && btnUnFollower == null){
    console.log("Profile");
    
}else{
    // user view
    if(btnFollower == null){
        tmpObject = btnUnFollower;
        loadChart();
    }else {
        tmpObject = btnFollower;
        loadChart();
    }
}


// load 
function loadChart(){

    var ajaxChart = new XMLHttpRequest();
    ajaxChart.open("GET", "/profile/activity/" + tmpObject.getAttribute("name")); 
    ajaxChart.send(null)

    ajaxChart.onreadystatechange = function () {

        if (ajaxChart.readyState == 4) {
            
            // ok
            if (ajaxChart.status == 200) {
                
                // data
                var data = ajaxChart.responseText;
                var parseJson = JSON.parse(data)
                var total = 0;
                
                if(parseJson.length > 0){

                    parseJson.forEach(element => {
                    
                        var x = element.fecha + "/" + element.hora;
                        var y = element.puntos;
                        
                        // Date
                        config.data.labels.push(x);

                        // update data chart
                        config.data.datasets[0].data.push({x, y});
                        window.myLine.update();
                    });
                }
               
            }
        }
    };
}