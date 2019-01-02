
function create_line(line_coords) {
    path = [];
    for (var j = 0; j < line_coords.length; j++) {
        path.push({
            lat: parseFloat(line_coords[j][0]),
            lng: parseFloat(line_coords[j][1])
        })
    }
    map_element = document.getElementById("map");

    line = new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    line.setMap(map_element.map);
    return line;
}

function create_new_line(line_coords) {
    path = [];
    for (var j = 0; j < line_coords.length; j++) {
        path.push({
            lat: parseFloat(line_coords[j][0]),
            lng: parseFloat(line_coords[j][1])
        })
    }
    return new google.maps.Polyline({
        path: path,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
}
