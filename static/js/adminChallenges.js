var matches = document.querySelectorAll("td > a");

var modChallengeID = document.getElementById('mod-challengeID')
var modScore = document.getElementById('mod-score')
var modValidate = document.getElementById('mod-validate')
var modCreator = document.getElementById('mod-creator')

var deleteChallengeID = "";
var deleteChallengeTitle = document.getElementById('deleteChallengeName');


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
            ajaxEdit.open("GET", "/admin/challenges/edit/" + parseName[5]); 
            ajaxEdit.send(null)

            ajaxEdit.onreadystatechange = function () {

                if (ajaxEdit.readyState == 4) {

                    if (ajaxEdit.status == 200) {

                        var data = ajaxEdit.responseText;
                        var parseJson = "";

                        if (data.search('{') != -1){
                            parseJson = JSON.parse(data)
                            
                            modChallengeID.value = parseJson.id
                            modScore.value = parseJson.puntos
                            modValidate.value = parseJson.validado
                            modCreator.value = parseJson.creador

                            // show modal
                            $('#editModal').modal('show')
                        }else{
                            //console.log(data);
                            window.location.href = "/"
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
            ajaxDelete.open("GET", "/admin/challenges/delete/" + parseName[5]); 
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
                            deleteChallengeID = parseJson.id;

                            // Modal name
                            deleteChallengeTitle.textContent = parseJson.titulo
                            
                            // show modal
                            $('#deleteModal').modal('show')
                        }else{

                            //console.log(data);
                            window.location.href = "/"
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
    ajaxDelete.open("POST", "/admin/challenges/edit/" + modChallengeID.value); 

    var formdata = new FormData();
    formdata.append("mod-challengeID", modChallengeID.value);
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
                    $('#deleteModal').modal('hide')
                    window.location.reload();
                }else{
                    console.log("Error Edit user");
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
    ajaxDelete.open("POST", "/admin/challenges/delete/" + deleteChallengeID);
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
                    console.log("Error Delete user");
                }
            }
        }
    };

})

