var plan_map;

function show_route(pub_id) {
    plan_map = new google.maps.Map(document.getElementById('map'), {});
    return $.ajax({
        method: "GET",
        url: "/api/route/"+pub_id,
        success: load_route_details
    });
}

function load_route_details(data) {
  sw = new google.maps.LatLng(data.bbox.s, data.bbox.w);
  ne = new google.maps.LatLng(data.bbox.n, data.bbox.e);
  plan_map.fitBounds(new google.maps.LatLngBounds(sw, ne));
  data.lines.forEach(function (line_coords) {
    line = create_new_line(line_coords);
    line.setMap(plan_map);
  });
}
