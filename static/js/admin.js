var matches = document.querySelectorAll("td > a");

var modName = document.getElementById('mod-name')
var modScore = document.getElementById('mod-score')
var modActivate = document.getElementById('mod-activate')
var modAdmin = document.getElementById('mod-admin')

var deleteUserName = document.getElementById('deleteUserName');


for (let i = 0; i < matches.length; i++) {
    
    matches[i].addEventListener('click', function(e){

        e.preventDefault();


        if (matches[i].id.search('btn-edit') == 0)
        {   
            var parseName = e.target.href.split('/')

            var ajaxEdit = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxEdit.open("GET", "/admin/edit/" + parseName[5]); 
            ajaxEdit.send(null)

            ajaxEdit.onreadystatechange = function () {

                if (ajaxEdit.readyState == 4) {

                    if (ajaxEdit.status == 200) {

                        var data = ajaxEdit.responseText;
                        
                        var parseJson = JSON.parse(data)

                        modName.value = parseJson.name
                        modScore.value = parseJson.puntos
                        modActivate.value = parseJson.activate
                        modAdmin.value = parseJson.admin

                        // show modal
                        $('#editModal').modal('show')
                    }
                }
            };

        }else{
            
            var parseName = e.target.href.split('/')

            var ajaxDelete = new XMLHttpRequest();
            /*ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.addEventListener("load", completeHandler, false);
            ajax.addEventListener("error", errorHandler, false);
            ajax.addEventListener("abort", abortHandler, false);*/
            ajaxDelete.open("GET", "/admin/delete/" + parseName[5]); 
            ajaxDelete.send(null)

            ajaxDelete.onreadystatechange = function () {

                if (ajaxDelete.readyState == 4) {
                    
                    // ok
                    if (ajaxDelete.status == 200) {
                        
                        // data
                        var data = ajaxDelete.responseText;
                        
                        // json
                        var parseJson = JSON.parse(data)
                        //console.log(parseJson);
                        
                        // user name
                        deleteUserName.textContent = parseJson.name

                        // show modal
                        $('#deleteModal').modal('show')
                    }
                }
            };
        }
    })
}

// end for

var modBtnEdit = document.getElementById('mod-btn-edit')
var modBtnDelete = document.getElementById('mod-btn-delete')


modBtnEdit.addEventListener('click', function(){
    
})

modBtnDelete.addEventListener('click', function(){
    
    var ajaxDelete = new XMLHttpRequest();
    /*ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);*/
    ajaxDelete.open("POST", "/admin/delete/" + deleteUserName.textContent); 
    ajaxDelete.send(null)

    ajaxDelete.onreadystatechange = function () {

        if (ajaxDelete.readyState == 4) {
            
            // ok
            if (ajaxDelete.status == 200) {
                
                // data
                var data = ajaxDelete.responseText;
                
                if (data == "done"){
                    console.log(data == "done");
                    $('#deleteModal').modal('hide')
                    window.location.reload();
                }else{
                    console.log("Error Delete user");
                }

                
                
                
            }
        }
    };

})

