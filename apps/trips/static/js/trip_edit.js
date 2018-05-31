
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

$( document ).ready(function() {
    init_datepicker();
});
