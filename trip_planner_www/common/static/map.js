var lines = [];
var markers = [];

var drawingManager;
var map_data = {};

function init_map(event, map) {
  map_id = $('#map').data('mapId')
  map.setCenter({lat: 48.4, lng: -123.0});
  map.setZoom(10);
  map.setMapTypeId(google.maps.MapTypeId.TERRAIN);

  drawingManager = new google.maps.drawing.DrawingManager({
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_LEFT,
      drawingModes: [
        google.maps.drawing.OverlayType.MARKER,
        google.maps.drawing.OverlayType.POLYLINE,
      ]
    },
  });
  drawingManager.setMap(map);

  $.ajax({
    method: "GET",
    url: "/api/v1/route/1/",
    success: function(data){
      init_markers(data);
      init_lines(data);
      map_data = data;
    }
  });
  
  google.maps.event.addListener(drawingManager, 'polylinecomplete', created_line);
  google.maps.event.addListener(drawingManager, "markercomplete", added_marker);
}

function close_all_info_windows(){
  $.each(markers, function(i, marker){
    marker.info_window.close();
  });
  $.each(lines, function(i, line){
    line.info_window.close();
  });
}

function ajax_update_route(){
  coordinates = [];
  $.each(markers, function(i, marker){
    if(marker.position.lat() && marker.map != null){
      coordinates.push([marker.position.lat(),marker.position.lng()])}});

  line_coordinates = [];
  $.each(lines, function(i, line){
    points = line.getPath().getArray();
    if(points.toString() != "(NaN, NaN)" && line.map != null){
      line_points = [];
      $.each(points, function(i, point){
        line_points.push([point.lat(), point.lng()]);
      });
      line_coordinates.push(line_points);
    }
  });

  data = {
    'action': 'update_map',
    'markers': { "type": "MultiPoint", "coordinates": coordinates },
    'lines': {'type': 'MultiLineString', 'coordinates': line_coordinates},
  }

  $.ajax({
    method: "PUT",
    url: "/api/v1/route/1/",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),
  });
}

$( document ).ready(function() {
  $('#map').gmap().bind('init', init_map);
});