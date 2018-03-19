
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
                url: `/api/routes/all?bounds=${bounds}&zoom=${map.zoom}`,
                success: load_routes_data
            });
        });
        google.maps.event.addListener(map, 'zoom_changed', function() {
            console.log("zoom: "+map.zoom)
        });

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
        load_route(route, false);
    });
}

function load_route_data(data) {
    load_route(data, true)
}

function load_route(data, recenter) {
    let map_element = document.getElementById("map");

    if (recenter && data['center'] !== null) {
        center = {
            lat: parseFloat(data['center']['coordinates'][0]),
            lng: parseFloat(data['center']['coordinates'][1])
        }
        map_element.map.setCenter(center);
    }

    if (data['lines'] !== null) {
        $.each(data['lines']['coordinates'], (index, line) => {
            add_line(line);
        });
    }
}


function add_line(line_coords) {
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
        map: map_element.map,
    });

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

