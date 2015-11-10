$( document ).ready(function() {
    $('#map').gmap().bind('init', init_map);
});

function init_map(event, map) {
  map_options = {
    center: {lat: 48.4, lng: -123},
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    draggable: true,
  };
  map.set(map_options);
}


function ajax_update_map(){
	data = {
    'action': 'update_map',
    'markers': []};
  $.each($('#map').gmap('get','markers'), function(i, marker){
    if(marker.map != null){
      data['markers'].push({
        'lat': marker.position.lat(),
        'lng': marker.position.lng()});
    }
  });
  $.post(window.location.href, JSON.stringify(data));
}