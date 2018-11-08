function init_remove(){
  $("#remove").on("click", remove_plan);
}

function remove_plan(){
  plan_pub_id = $("div#plan-pub-id").text();
  window.location.href = "/trip/plan/remove/"+plan_pub_id;
}



