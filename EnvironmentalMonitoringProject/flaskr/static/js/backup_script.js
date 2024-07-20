 carbon_dioxide_id = document.getElementById('CarbonDioxideChart');
 ox_chart_id = document.getElementById('OxygenChart');
 nitric_dioxide_id = document.getElementById('NitricDioxideChart');
 hum_chart_id = document.getElementById('humidityChart');


// Function to fetch data from a URL
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

// Function to update the chart with new data
async function updateChart() {
    const Url = 'http://localhost:8021/api/data';
    const newData = await fetchData(Url);
    finalData = prepareData(newData)

    CarbonDioxideLineChart.data.labels = finalData.labels;
    CarbonDioxideLineChart.data.datasets[0].data = finalData.carbon_dioxide;

    HumLineChart.data.labels = finalData.labels;
    HumLineChart.data.datasets[0].data = finalData.hum_data;

    OxygenLineChart.data.labels = finalData.labels;
    OxygenLineChart.data.datasets[0].data = finalData.oxy_data;
    NitricDioxideLineChart.data.labels = finalData.labels;
    NitricDioxideLineChart.data.datasets[0].data = finalData.nitric_dioxide_data;


    CarbonDioxideLineChart.update();
    HumLineChart.update();
    OxygenLineChart.update();
    NitricDioxideLineChart.update();
}

// Function to prepare the data for the chart
function prepareData(data) {
    // Extract the last 100 entries
    const last100Entries = data.slice(-30);

    const timestamps = [];
    const carbon_dioxide_values = [];
    const hum_values = [];
    const oxygen_values = [];
    const nitric_dioxide_values = [];
    // Extract values into separate arrays
    last100Entries.forEach(entry => {
        timestamps.push(entry.timestamp);
        carbon_dioxide_values.push(entry.co2);
        hum_values.push(entry.humidity);
        oxygen_values.push(entry.o2);
        nitric_dioxide_values.push(entry.no2);
    });

    return {
        labels: timestamps,
        carbon_dioxide: carbon_dioxide_values,
        hum_data: hum_values,
        oxy_data: oxygen_values,
        nitric_dioxide_data: nitric_dioxide_values
    };
}

// Create the initial chart
const CarbonDioxideLineChart = new Chart(carbon_dioxide_id, {
    type: 'line',
    data: {
        //labels: ['2022-04-23T12:00:00', '2022-04-23T12:00:00', '2022-04-23T12:00:00', '2022-04-23T12:00:00', '2022-04-23T12:00:00', '2022-04-23T12:00:00'],
        datasets: [{
            label: 'Carbon Dioxide',
           // data: [12, 12, 12, 12, 12, 12],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


// Create the initial chart
const HumLineChart = new Chart(hum_chart_id, {
    type: 'line',
    data: {
        datasets: [{
            label: 'humidity',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


// Create the initial chart
const OxygenLineChart = new Chart(ox_chart_id, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Oxygen',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


// Create the initial chart
const NitricDioxideLineChart = new Chart(nitric_dioxide_id, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Nitric Dioxide',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Uncomment the following line to update the chart every 5 seconds
setInterval(updateChart, 3000);

