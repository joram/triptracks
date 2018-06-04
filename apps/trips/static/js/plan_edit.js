
function init_datepicker(){
  $('input#trip_datepicker').daterangepicker({}, update_datetime);
}

function update_datetime(start, end, label){
  plan_pub_id = $("div#plan-pub-id").text();
  data = {
    start: start.format('YYYY/MM/DD'),
    end: end.format('YYYY/MM/DD')
  };
  $.ajax({
    type: "POST",
    url: "/trip/plan/edit/"+plan_pub_id,
    data: data,
    dataType: 'json'
  });
}

function init_remove(){
  $("#remove").on("click", remove_plan);
}

function remove_plan(){
  plan_pub_id = $("div#plan-pub-id").text();
  window.location.href = "/trip/plan/remove/"+plan_pub_id;
}



function init_forecast(){
  var plan_pub_id = $("div#plan-pub-id").text();
  $.ajax({
    type: "GET",
    url: "/trip/plan/"+plan_pub_id+"/forecast",
    dataType: 'json',
    success: createChart
  })
}

function createChart(rawData) {
  humidityData = [];
  cloudinessData = [];
  minTemperatureData = [];
  maxTemperatureData = [];
  precipitationData = [];
  precipitationLabels = [];
  keys = Object.keys(rawData).sort();
  for(var i=0; i<keys.length; i ++){
    key = keys[i];
    val = rawData[key];
    dt = new Date(key);
    if("minTemperature" in val){
      minTemperatureData.push({'t': dt, 'y': val.minTemperature});
    }
    if("maxTemperature" in val) {
      maxTemperatureData.push({'t': dt, 'y': val.maxTemperature});
    }
    if("precipitation" in val) {
      precipitationData.push(val.precipitation);
      precipitationLabels.push(dt);
    }
  };

  options = {
    scales: {
      xAxes: [{
        time: {
          unit: 'day'
        },
        type: 'time',
        distribution: 'linear'
      }]
    }
  };

  options2 = {};
  new Chart($("#precipitationChart"), {
    options: options,
    type: 'bar',
    data: {
      labels: precipitationLabels,
      datasets: [{
        label: "Precipitation mm",
        data: precipitationData,
        backgroundColor: 'rgba(132,99,255,1)'
      }]
    }
  });

  new Chart($("#temperatureChart"), {
    options: options,
    type: 'line',
    data:  {
      datasets: [{
        label: "Min C°",
        data: minTemperatureData,
        borderColor: 'rgba(132,99,255,1)',
        backgroundColor: 'rgba(0,0,0,0)'
      }, {
        label: "Max C°",
        data: maxTemperatureData,
        borderColor: 'rgba(255,99,132,1)',
        backgroundColor: 'rgba(0,0,0,0)'
      }]
    }
  });

}

$( document ).ready(function() {
  init_datepicker();
  init_remove();
  init_forecast();
});
