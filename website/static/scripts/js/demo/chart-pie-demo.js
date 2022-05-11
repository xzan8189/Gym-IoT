// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


function myPieChart(gym) {
    // Pie Chart Example
    console.log('calories_lost_today: ' + gym['calories_lost_today']);
    console.log('calories_to_reach_today: ' + gym['calories_to_reach_today']);
    var calorie_mancanti_da_consumare = parseFloat(gym['calories_to_reach_today']) - parseFloat(gym['calories_lost_today'])
    console.log('Calorie mancanti: ' + calorie_mancanti_da_consumare);
    var ctx = document.getElementById("myPieChart");

    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ["Calories left", "Calories already left today"],
        datasets: [{
          data: [gym['calories_to_reach_today']-gym['calories_lost_today'], gym['calories_lost_today']],
          backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
          hoverBackgroundColor: ['#2e59d9', '#17a673'],
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
        },
        legend: {
          display: true
        },
        cutoutPercentage: 80,
      },
    });
}