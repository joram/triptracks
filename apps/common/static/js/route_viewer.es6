
function load_google_maps(api_key, route_id) {
    this.route_id = route_id;
    this.lines = [];

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function load_all_routes_google_maps(api_key){
    this.lines = [];

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map_all_routes`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function build_map_all_routes() {
    let map_element = document.getElementById("map");

    map = new google.maps.Map(map_element, {});
    map.setZoom(15);
    map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
    map_element.map = map;

    return $.ajax({
        method: "GET",
        url: `/api/routes/all`,
        success: load_map_all_routes_data
    });
}


function build_map() {
    let map_element = document.getElementById("map");

    map = new google.maps.Map(map_element, {});
    map.setZoom(15);
    map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
    map_element.map = map;

    return $.ajax({
        method: "GET",
        url: `/api/v1/route/${this.route_id}/`,
        success: load_map_data
    });
}

function load_map_all_routes_data(data) {
    first_route = data[0];
    console.log(first_route);
    center = {
        lat: parseFloat(first_route['center']['coordinates'][0]),
        lng: parseFloat(first_route['center']['coordinates'][1])
    }
    let map_element = document.getElementById("map");
    map_element.map.setCenter(center);

    $.each(data, (index, route) => {
      console.log("loading route");
        load_route(route);
    });
}

function load_map_data(data) {
  load_route(data)
}

function load_route(data) {
    center = {
        lat: parseFloat(data['center']['coordinates'][0]),
        lng: parseFloat(data['center']['coordinates'][1])
    }

    let map_element = document.getElementById("map");
    map_element.lines = [];
    map_element.map.setCenter(center);

//    if (data['markers'] !== null) {
//        $.each(data['markers']['coordinates'], this.add_marker);
//    }

    if (data['lines'] !== null) {
        $.each(data['lines']['coordinates'], (index, line) => {
            add_line(map_element.map, line);
        });
    }
}


function add_line(map, line_coords) {
    let line_coordinates = [];
    $.each(line_coords, (index, point) => line_coordinates.push({lat: point[0], lng: point[1]}));

    line = new google.maps.Polyline({
      path: line_coordinates,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    line.setMap(map);
    console.log("added a line");
}

function add_marker(coord) {
    let marker = new google.maps.Marker({
        'position': new google.maps.LatLng(coord[0], coord[1]),
        'draggable': false,
        'map': this.drawingManager.map });
    maparkers.add(marker);
    marker.list_index = markers.indexOf(marker);
    return marker;
}

