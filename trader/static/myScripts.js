var bitData;
var ethData =  [750, 765, 780, 785, 805, 850, 900];
var liteData =  [760, 768, 785, 775, 790, 825, 860];
///////////////////////////////////////////bit coin Chart////////////////////////////////////////
function bitChart(){
var bitData = temp;

var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
        type: 'line',
    
    // The data for our dataset
    data: {
        labels: ["0","5","10","15","20","25","30"],
        datasets: [{
            label: "Bit Coin",
            borderColor: 'red',
            data: [bitData[29],bitData[24],bitData[19],bitData[14],bitData[9],bitData[4],bitData[0]]
        }],
    },

    // Configuration options go here
    options: {
    	scales: { 
            yAxes: [{ ticks: { suggestedMin:800, suggestedMax: 1100, stepsize : 50 } }]
        }
    }
});

}

///////////////////////////////////////////Ethereum Chart////////////////////////////////////////
function ethChart(){
var ctx = document.getElementById('myChart1').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["0","5","10","15","20","25","30"],
        datasets: [{
        	x: 7, y:50,
            label: "Ethereum Coin",
            borderColor: 'green',
            data: ethData
        }]
    },

    // Configuration options go here
    options: {
    	scales: { yAxes: [{ ticks: {suggestedMin:800, suggestedMax: 1100, stepsize : 50 } }]
        }
    }
});

}
///////////////////////////////////////////Lite Coin Chart////////////////////////////////////////

function liteChart(){
var ctx = document.getElementById('myChart2').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["0","5","10","15","20","25","30"],
        datasets: [{
            label: "Lite Coin",
            borderColor: 'blue',
            data: liteData
        }]
    },

    // Configuration options go here
    options: {
    	scales: { yAxes: [{ ticks: {suggestedMin:800, suggestedMax: 1100, stepsize : 50 } }]
        }
    }
});

}

function combine(){
    bitData = temp;
	var ctx = document.getElementById('combo').getContext('2d');
	var chart = new Chart (ctx, {
 // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["0","5","10","15","20","25","30"],
        datasets: [{label: "Lite Coin",borderColor: 'blue',data: liteData},
        		   {label: "Bit Coin", borderColor: 'red', data: [bitData[29],bitData[24],bitData[19],bitData[14],bitData[9],bitData[4],bitData[0]]},
        		   {label: "Ethereum Coin", borderColor:'green', data:ethData}]
    },

    // Configuration options go here
    options: {
    	scales: { yAxes: [{ ticks: { suggestedMin:800, suggestedMax: 1100, stepsize : 50 } }]
        }
    }


});
}

function getData(){
var url = "https://7d609bf1.ngrok.io/get-market-data?coin=Bitcoin";
var data;
var xhr = new XMLHttpRequest();
xhr.open("GET", url, true);
xhr.onreadystatechange = function() {
if (xhr.readyState === 4) {
    if (xhr.status === 200) {
        data = xhr.responseText;
        var obj = JSON.parse(data);

        temp = [obj["result"][0], obj["result"][1], obj["result"][2], obj["result"][3],obj["result"][4], obj["result"][5], obj["result"][6], obj["result"][7],obj["result"][8],
         obj["result"][9], obj["result"][10], obj["result"][11],obj["result"][12], obj["result"][13], obj["result"][14], obj["result"][15],obj["result"][16], obj["result"][17], obj["result"][18], 
        obj["result"][19],obj["result"][20], obj["result"][21], obj["result"][22], obj["result"][23],obj["result"][24],obj["result"][25], obj["result"][26], obj["result"][27],obj["result"][28], obj["result"][29]];
        
        temp = temp.map(Number);
        console.log(temp);
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(null);
}


var temp = getData();


 