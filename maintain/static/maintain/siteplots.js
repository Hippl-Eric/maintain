/* Grab the plotting canvas and user Chart.js to plot mileage data */
if (document.getElementById('mileage-plot')) {

    // Determine default or all-cars
    const plotType = document.getElementById('mileage-plot').dataset.plot;
    const carType = document.getElementById('mileage-plot').dataset.car;

    // Grab csrftoken from cookie
    const csrftoken = Cookies.get('csrftoken');

    // Create request to get mileage data to plot
    const request = new Request(
        "/plotlogs",
        {
            method: "PUT",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin",
            body: JSON.stringify({
                type: plotType,
                car: carType,
            })
        }
    );
    
    // Fetch plot data
    fetch(request)
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alert(data.error);
        }
        else {

            // Parse returned string data to JSON
            const jsonData = JSON.parse(data);

            // Establish list of colors for plot data
            const colorList = ['rgba(255, 77, 77)', 'rgba(77, 130, 255)', 'rgba(77, 255, 97)', 'rgba(252, 255, 77)']
            const l = colorList.length

            // Create list of dataset objects for plotting
            const plotData = []
            jsonData.forEach((obj, i) => {
                data_obj = {
                    label: obj["label"],
                    data: obj["data"],
                    fill: false,
                    backgroundColor: colorList[i - l * Math.trunc(i/l)], // Loop through colors in colorList
                    borderColor: colorList[i - l * Math.trunc(i/l)],
                }
                plotData.push(data_obj)
            })
            
            // Create the plot via chart.js
            const ctx = document.getElementById('mileage-plot').getContext('2d');
            const lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: plotData
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {
                                unit: 'month'
                            },
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                }
            });
        }
    })
}