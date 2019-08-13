window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

var color = Chart.helpers.color;
var config = {
	type: 'line',
		data: {
			datasets: [{
                label: 'Flag',
                backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
                borderColor: window.chartColors.blue,
                fill: false,
                data: [/*{
                    x: "2019-12-30 12:24:56",
					y: 100
				}*/] // end data
            
			}] // end datasets
			
			},
			options: {
				responsive: true,
				title: {
					display: false,
					text: 'Chart.js Time Point Data'
				},
				scales: {
					xAxes: [{
						type: 'time',
						display: true,
						scaleLabel: {
							display: false,
							labelString: 'Date'
						},
						ticks: {
							major: {
								fontStyle: 'bold',
								fontColor: '#FF0000'
							}
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: false,
							labelString: 'value'
						}
					}]
				},
				legend: false
			}
		};

		window.onload = function() {

			var ctx = document.getElementById('canvas').getContext('2d');
			window.myLine = new Chart(ctx, config);
			
			loadChart();

			//var reScale = document.getElementById('canvas');
			//reScale.style = "width: 100%; height: 250px; margin-top: 10px;";
		};