var matches = document.querySelectorAll("td > a");

var modName = document.getElementById('mod-name')
var modScore = document.getElementById('mod-score')
var modActivate = document.getElementById('mod-activate')
var modAdmin = document.getElementById('mod-admin')

var deleteUserName = document.getElementById('deleteUserName');

var tmpID = ""

for (let i = 0; i < matches.length; i++) {
    
    matches[i].addEventListener('click', function(e){

        e.preventDefault();

        // edit
        if (matches[i].id.search('btn-edit') == 0)
        {   
            var parseName = e.target.href.split('/')

            tmpID = parseName[5]

            var ajaxEdit = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxEdit.open("GET", "/admin/edit/" + tmpID); 
            ajaxEdit.send(null)

            ajaxEdit.onreadystatechange = function () {

                if (ajaxEdit.readyState == 4) {

                    if (ajaxEdit.status == 200) {

                        var data = ajaxEdit.responseText;
                        var parseJson = "";

                        if (data.search('{') != -1){
                            parseJson = JSON.parse(data)
                            
                            modName.value = parseJson.name
                            modScore.value = parseJson.puntos
                            modActivate.value = parseJson.activate
                            modAdmin.value = parseJson.admin

                            // show modal
                            $('#editModal').modal('show')
                        }else{
                            //console.log(data);
                            window.location.href = "/admin"
                        }

                    }
                }
            };

        }else{ // Delete
            
            var parseName = e.target.href.split('/')
            
            tmpID = parseName[5]

            var ajaxDelete = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxDelete.open("GET", "/admin/delete/" + tmpID); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data server 
                        var data = ajaxDelete.responseText;

                        if (data.search('Admin') == 0){
                            //console.log(data);
                            window.location.href = "/"
                        }else{
                            
                            // Modal name
                            deleteUserName.textContent = data

                            // show modal
                            $('#deleteModal').modal('show')
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
    ajaxDelete.open("POST", "/admin/edit/" + tmpID); 

    var formdata = new FormData();
    formdata.append("mod-name", modName);
    formdata.append("mod-score", modScore.value);
    formdata.append("mod-activate", modActivate.value);
    formdata.append("mod-admin", modAdmin.value);

    ajaxDelete.send(formdata)

    ajaxDelete.onreadystatechange = function () {

        if (ajaxDelete.readyState == 4) {
            
            // ok
            if (ajaxDelete.status == 200) {
                
                // data
                var data = ajaxDelete.responseText;
                
                if (data == "done"){
                    console.log(data);
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
    
    ajaxDelete.open("POST", "/admin/delete/" + tmpID); 
    ajaxDelete.send(null)

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

