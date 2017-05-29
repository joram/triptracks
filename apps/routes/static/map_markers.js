
function init_markers(data){
  if(data['markers'] != null){
    $.each(data['markers']['coordinates'], function (index, coord){
      create_marker(coord);
    });
  }
}

function create_marker(pos){
  var marker = new google.maps.Marker({
    'position': new google.maps.LatLng(pos[0], pos[1]),
    'draggable': true, 
    'map': drawingManager.map });
  added_marker(marker);
}

function added_marker(marker){
  marker.setDraggable(true);
  google.maps.event.addListener(marker, "dragend", moved_marker);
  google.maps.event.addListener(marker, "rightclick", function(event){
    close_all_info_windows();
    marker.info_window.open(drawingManager.map, marker);
  });

  markers.push(marker);
  marker.list_index = markers.indexOf(marker);
  marker.info_window = new google.maps.InfoWindow({});
  marker.info_window.setContent("<div style='width:100px'><button onclick='remove_marker("+marker.list_index+");'>remove</button></div>");
  ajax_update_route();
}

function moved_marker(event){
  ajax_update_route();
}

function remove_marker(list_index) {
  $.each(markers, function(index, marker){
    if(marker.list_index == list_index){
      marker.setMap(null);
    }
  });
  ajax_update_route();
}
