
var toggle = document.getElementById('toggle-logo')
var sidebar = document.getElementById('sidebar')
var toggleBtn = false;

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