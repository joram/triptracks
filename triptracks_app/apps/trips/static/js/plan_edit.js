
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

function init_forecast(){
  var plan_pub_id = $("div#plan-pub-id").text();
  $.ajax({
    type: "GET",
    url: "/trip/plan/"+plan_pub_id+"/forecast",
    dataType: 'json',
    success: updateForecast
  })
}

function updateForecast(rawData) {
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
    console.log(key, dt);

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
  }


}

function init_invite(){
  modal = $("#invite_email_modal");
  button = $("#invite_email_button");
  input = $("#invite_email");
  button.on("click", function(){
    modal.modal("hide");
  });
}

$( document ).ready(function() {
  init_datepicker();
  // init_remove();
  init_forecast();
  init_invite();
});
