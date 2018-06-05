var plan_map;

function show_route(pub_id) {
    plan_map = new google.maps.Map(document.getElementById('map'), {});
    return $.ajax({
        method: "GET",
        url: "/api/route/"+pub_id,
        success: load_route_details
    });
}

function line_bounds(line){
  var bounds = new google.maps.LatLngBounds();
  line.getPath().forEach(function(item, index) {
      bounds.extend(new google.maps.LatLng(item.lat(), item.lng()));
  });
  return bounds;
}

function load_route_details(data) {
  bounds = new google.maps.LatLngBounds();
  data.lines.forEach(function (line_coords) {
    line = create_new_line(line_coords);
    line.setMap(plan_map);
    bbox = line_bounds(line);
    bounds.extend(bbox.getNorthEast());
    bounds.extend(bbox.getSouthWest());
  });
  console.log(bounds);
  plan_map.fitBounds(bounds);
}
