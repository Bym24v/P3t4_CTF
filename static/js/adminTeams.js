var matches = document.querySelectorAll("td > a");

var modTeamID = document.getElementById('mod-teamID')
var modScore = document.getElementById('mod-score')
var modValidate = document.getElementById('mod-validate')
var modCreator = document.getElementById('mod-creator')

var deleteTeamID = "";
var deleteTeamTitle = document.getElementById('deleteChallengeName');


for (let i = 0; i < matches.length; i++) {
    
    matches[i].addEventListener('click', function(e){

        e.preventDefault();

        // edit
        if (matches[i].id.search('btn-edit') == 0)
        {   
            var parseName = e.target.href.split('/')

            var ajaxEdit = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxEdit.open("GET", "/admin/teams/edit/" + parseName[5]); 
            ajaxEdit.send(null)

            ajaxEdit.onreadystatechange = function () {

                if (ajaxEdit.readyState == 4) {

                    if (ajaxEdit.status == 200) {

                        var data = ajaxEdit.responseText;
                        var parseJson = "";

                        if (data.search('{') != -1){
                            parseJson = JSON.parse(data)
                            //console.log(parseJson);
                            
                            modTeamID.value = parseJson.id
                            modScore.value = parseJson.score
                            modValidate.value = parseJson.activate
                            modCreator.value = parseJson.creator

                            // show modal
                            $('#editModal').modal('show')
                        }else{
                            //console.log(data);
                            window.location.href = "/admin/teams"
                        }

                    }
                }
            };

        }else{ // Delete
            
            var parseName = e.target.href.split('/')

            var ajaxDelete = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxDelete.open("GET", "/admin/teams/delete/" + parseName[5]); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data server 
                        var data = ajaxDelete.responseText;
                        parseJson = ""
                        
                        if (data.search('{') != -1){
                            parseJson = JSON.parse(data)
                            //console.log(parseJson);
                            
                            // challenge id
                            deleteTeamID = parseJson.id;

                            // Modal name
                            deleteTeamTitle.textContent = parseJson.title
                            
                            // show modal
                            $('#deleteModal').modal('show')
                        }else{
                            //console.log(data);
                            window.location.href = "/admin/teams"
                        }

                    }
                }
            };
        }
    })
}

// end for

var modBtnEdit = document.getElementById('mod-btn-edit')
var modBtnDelete = document.getElementById('mod-btn-delete')

// Edit
modBtnEdit.addEventListener('click', function(){
    
    var ajaxDelete = new XMLHttpRequest();
    /*ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);*/
    ajaxDelete.open("POST", "/admin/teams/edit/" + modTeamID.value); 

    var formdata = new FormData();
    formdata.append("mod-teamID", modTeamID.value);
    formdata.append("mod-score", modScore.value);
    formdata.append("mod-validate", modValidate.value);
    formdata.append("mod-creator", modCreator.value);

    ajaxDelete.send(formdata)

    ajaxDelete.onreadystatechange = function () {

        if (ajaxDelete.readyState == 4) {
            
            // ok
            if (ajaxDelete.status == 200) {
                
                // data
                var data = ajaxDelete.responseText;
                
                if (data == "done"){
                    //console.log(data);
                    $('#editModal').modal('hide')
                    window.location.reload();
                }else{
                    $('#editModal').modal('hide')
                    console.log("Error Edit team");
                }
            }
        }
    };
    
})

// Delete
modBtnDelete.addEventListener('click', function(){
    
    var ajaxDelete = new XMLHttpRequest();
    /*ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);*/
    ajaxDelete.open("POST", "/admin/teams/delete/" + deleteTeamID);
    ajaxDelete.send(null);

    ajaxDelete.onreadystatechange = function () {

        if (ajaxDelete.readyState == 4) {
            
            // ok
            if (ajaxDelete.status == 200) {
                
                // data
                var data = ajaxDelete.responseText;
                
                if (data == "done"){
                    //console.log(data);
                    $('#deleteModal').modal('hide')
                    window.location.reload();
                }else{
                    $('#deleteModal').modal('hide')
                    console.log("Error delete team");
                }
            }
        }
    };

})

