$( document ).ready(function() {
  $('#map').gmap().bind('init', init_markers);
});

function init_markers(event, map) {
  $.each(map_data['markers'], function(index, marker){
    create_marker(new google.maps.LatLng(marker['lat'], marker['lng']));
  });
  $(map).click(add_marker);
}

function create_marker(position){
  marker_options = {
    'position': position, 
    'draggable': true, 
    'bounds': false
  };
  $('#map').gmap('addMarker', marker_options, function(map, marker){
    marker.info_window = new google.maps.InfoWindow({});
    marker.info_window.setContent("<div style='width:100px'><button onclick='remove_marker("+$('#map').gmap('get','markers').indexOf(marker)+");'>remove</button></div>");
    google.maps.event.addListener(marker,'dragend', drag_end_marker);
    google.maps.event.addListener(marker, "rightclick", function(event){
      close_all_info_windows();
      marker.info_window.open(map, marker);
    });
  });

}

function close_all_info_windows(){
  $.each($('#map').gmap('get','markers'), function(i, marker){
    marker.info_window.close();
  });
}

function add_marker(event) {
  create_marker(event.latLng);
  ajax_update_map();
}

function remove_marker(index) {
  $('#map').gmap('get','markers')[index].setMap(null);
  ajax_update_map();
}

function drag_end_marker(event) {
  ajax_update_map();
}
