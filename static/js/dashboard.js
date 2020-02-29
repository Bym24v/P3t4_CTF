
var toggle = document.getElementById('toggle-logo')
var sidebar = document.getElementById('sidebar')
var toggleBtn = false;

// toggle sidebar
toggle.addEventListener('click', function(e){

    e.preventDefault();

    if(!toggleBtn){
        toggleBtn = true;
        sidebar.classList.add('mshow')
        sidebar.classList.remove('d-none')
        
    }else{
        toggleBtn = false
        sidebar.classList.remove('mshow')
        sidebar.classList.add('d-none')
    }
})

// show name file upload
var inputBtn = document.getElementById('validatedCustomFile')
var nameShow = document.getElementById('file-show')

// event input file upload


if (inputBtn != null && nameShow != null){

    inputBtn.addEventListener('change', function(e){
    
        var uploadFIle = e.target.files[0]
    
        nameShow.textContent = uploadFIle.name;
        
    })
}


var notifyBtn = document.getElementById('notify-btn');
var notifyMenu = document.getElementById('menu-notify');
var notifyActive = document.getElementById('notify-active');
var toggleMenu = false;

if(notifyBtn != null){

    notifyBtn.addEventListener('click', function(e){
        
        if(toggleMenu){
            notifyMenu.style = "visibility: hidden;";
            toggleMenu = false;
        }else{
            notifyMenu.style = "visibility: visible;";
            toggleMenu = true;

            notifyActive.style = "visibility: hidden;";
        }
        
    })
    

}