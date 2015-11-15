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
    drawingMode: google.maps.drawing.OverlayType.MARKER,
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
    url: "/api/v1/map/1/",
    success: function(data){

      // build markers from string
      markers_str = data['markers'].replace("MULTIPOINT (", "").replace(")", "")
      markers = []
      $.each(markers_str.split(", "), function(i, marker_str){
        p = marker_str.split(" ");
        p[0] = parseFloat(p[0]);
        p[1] = parseFloat(p[1]);
        create_marker(p);
      });
      data['markers'] = markers;

      // build lines from string
      lines_str = data['lines'].replace("MULTILINESTRING ((", "").replace("))", "")
      $.each(lines_str.split("), ("), function(i, line_str){
        line = []
        $.each(line_str.split(", "), function(i, point_str){
          p = point_str.split(" ");
          p[0] = parseFloat(p[0]);
          p[1] = parseFloat(p[1]);
          line.push(p)
        });
        create_line(line);
      });

      map_data = data;
      $.each(map_data['markers'], function(index, pos){
        create_marker(pos);
      });
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

function ajax_update_map(){
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
    method: "POST",
    url: "/plan/1/edit",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),
  });
}

$( document ).ready(function() {
  $('#map').gmap().bind('init', init_map);
});