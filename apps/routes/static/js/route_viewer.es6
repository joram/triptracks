var lines_cache = {};

function load_google_maps(api_key, route_id) {
    this.route_id = route_id;
    this.lines = {};

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function load_all_routes_google_maps(api_key){
    this.lines = {};

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map_all_routes`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function build_map_all_routes() {

    navigator.geolocation.getCurrentPosition(function(position) {
        var center = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        let map_element = document.getElementById("map");
        map = new google.maps.Map(map_element, {
            zoom: 12,
            center: center,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
        });
        map_element.map = map;

        google.maps.event.addListener(map, 'bounds_changed', function() {
            bounds = map.getBounds().toUrlValue();
            return $.ajax({
                method: "GET",
                url: `/api/routes/all?bounds=${bounds}&zoom=${map.getZoom()}`,
                success: load_routes_data
            });
        });
        // map.addListener('zoom_changed', function() {
        //     console.log("zoom: "+map.getZoom());
        // });

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
        success: load_route_data
    });
}

function load_routes_data(data) {
    $.each(data, (index, route) => {
        unload_route(route);
        if(!use_cached_lines(route)){
            load_route(route);
        }
    });
}

function load_route_data(data) {
    load_route(data, true)
}

function unload_route(route) {
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    if (lines_cache[pub_id] != null){
        for(zoom in lines_cache[pub_id]) {
            if(lines_cache[pub_id][zoom] != null && zoom != zoom_level){
                lines_cache[pub_id][zoom]["googlemaps_lines"].forEach(function (google_line){
                    google_line.setMap(null);
                });
            }
        }
    }
}

function center(route){
    let map_element = document.getElementById("map");
    center = route["center"];

    // recenter
    if (route['center'] !== null) {
        center = {
            lat: parseFloat(route['center']['coordinates'][0]),
            lng: parseFloat(route['center']['coordinates'][1])
        };
        map_element.map.setCenter(center);
    }
}

function use_cached_lines(route){
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    route_lines = route["lines"];

    if(lines_cache[pub_id] == null){
        return false;
    }
    if(lines_cache[pub_id][zoom_level] == null) {
        return false;
    }

    let map_element = document.getElementById("map");
    google_lines = lines_cache[pub_id][zoom_level]["googlemaps_lines"];
    google_lines.forEach(function (google_line){
        google_line.setMap(map_element.map);
    });
    return true;
}

function load_route(route) {
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    route_lines = route["lines"];

     // create new
     if (route['lines'] !== null) {
        google_lines = [];
        route['lines'].forEach(function (line) {
            google_lines.push(create_line(line));
        });
        route["googlemaps_lines"] = google_lines;
     }

    // cache
    if(lines_cache[pub_id] == null){
        lines_cache[pub_id] = {};
    }
    if(lines_cache[pub_id][zoom_level] == null) {
        lines_cache[pub_id][zoom_level] = route;
    }
}


function create_line(line_coords) {
    let path = [];
    for (var j = 0; j < line_coords.length; j++) {
        path.push({
            lat: parseFloat(line_coords[j][0]),
            lng: parseFloat(line_coords[j][1])
        })
    }

    let map_element = document.getElementById("map");

    line = new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });
    line.setMap(map_element.map);
    return line;
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

