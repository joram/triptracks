  poly = new google.maps.Polyline({
    strokeColor: '#000000',
    strokeOpacity: 1.0,
    strokeWeight: 3
  });
  poly.setMap(map);

// Handles click events on a map, and adds a new point to the Polyline.
function addLatLng(event) {
  var path = poly.getPath();
  path.push(event.latLng);
}

function remove_marker(index) {
  $('#map').gmap('get','markers')[index].setMap(null);
  ajax_update_map();
}