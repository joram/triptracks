$( document ).ready(function() {
  map_options = {
    center: {lat: 48.4, lng: -123},
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    draggable: true,
  };

  $('#map').gmap().bind('init', function(event, map) {
    $.each(map_data['markers'], function(index, marker){
      create_marker(new google.maps.LatLng(marker['lat'], marker['lng']));
    });
    $(map).click(add_marker);
  });

});

function create_marker(position){
  marker_options = {
    'position': position, 
    'draggable': true, 
    'bounds': false
  };
  $('#map').gmap('addMarker', marker_options, function(map, marker){
    google.maps.event.addListener(marker,'dragend', marker_drag_end);
  });
}
function add_marker(event) {
  create_marker(event.latLng);
  ajax_update_map();
}

function marker_drag_end(event) {
    ajax_update_map();
}

function ajax_update_map(){
	data = {
    'action': 'update_map',
    'markers': []};
  $.each($('#map').gmap('get','markers'), function(i, marker){
    data['markers'].push({
      'lat': marker.position.lat(),
      'lng': marker.position.lng()});
  });
  $.post(window.location.href, JSON.stringify(data));
}