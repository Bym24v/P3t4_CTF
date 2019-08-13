var dias = document.getElementById('dias')
var horas = document.getElementById('horas')
var minutos = document.getElementById('minutos')
var segundos = document.getElementById('segundos')

var countDownDate = new Date("Aug 15, 2019 00:00:00").getTime();

var conutDownFunction = setInterval(function(){

	var now = new Date().getTime();

	var distance = countDownDate - now;
	//console.log(distance)

	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	// check valid value
	if (days < 0){
		days = 0;
	}

	if (hours < 0){
		hours = 0;
	}

	if (minutes < 0){
		minutes = 0;
	}

	if (seconds < 0){
		seconds = 0;
	}
	
	dias.innerHTML = days + "d";
	horas.innerHTML = hours + "h";
	minutos.innerHTML = minutes + "m";
	segundos.innerHTML = seconds + "s";
})