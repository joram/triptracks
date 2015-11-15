var lines = [];
var markers = [];

var drawingManager;
var map_data = {};

function init_map(event, map) {
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
      console.log(data);

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
  
  google.maps.event.addListener(drawingManager, "overlaycomplete", overlay_added);
}

function create_line(points){
  var flightPlanCoordinates = [];
  $.each(points, function(index, point){
    flightPlanCoordinates.push({lat: point[0], lng: point[1]});
  });

  var flightPath = new google.maps.Polyline({
    path: flightPlanCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });
  flightPath.setMap(drawingManager.map);
  lines.push(points);
}

function created_line(event){
  line = [];
  $.each(event.overlay.getPath().getArray(), function(index, point){
    line.push([point.lat(), point.lng()]);
  });
  lines.push(line);
}

function overlay_added(event){
  if (event.type == google.maps.drawing.OverlayType.POLYLINE) {
    created_line(event);
  }
  if (event.type == google.maps.drawing.OverlayType.MARKER) {
    pos = [event.overlay.position.lat(), event.overlay.position.lng()];
    create_marker(pos);
  }
  ajax_update_map();
};

function ajax_update_map(){
  coordinates = []
  $.each(markers, function(i, marker){
    if(marker.position.lat() && marker.map != null){
      coordinates.push([marker.position.lat(),marker.position.lng()])}});

  $.ajax({
    method: "POST",
    url: "/plan/1/edit",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({
      'action': 'update_map',
      'markers': { "type": "MultiPoint", "coordinates": coordinates },
      'lines': {'type': 'MultiLineString', 'coordinates': lines},
    }),
  });
}

$( document ).ready(function() {
  $('#map').gmap().bind('init', init_map);
  map_id = $('#map').data('mapId')
});