// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Budget Data Pie Chart
var getData = $.get('/data/spending-profit-balance')
var ctx3 = document.getElementById("myPieChart");
getData.done(function(data){
    var profit = data.Profit
    var spending = data.Spending
    var balance = data.Balance
    var myPieChart = new Chart(ctx3, {
      type: 'doughnut',
      data: {
        labels: ["Balance", "Profit", "Spending"],
        datasets: [{
          data: [balance, profit, spending],
          backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
          hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
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

})
