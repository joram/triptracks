var drawingManager;

function init_static_map(event, map) {
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
    url: "/api/v1/route/",
    success: function(data){
      console.log(data)
      init_lines(data);
    }
  });
}


$( document ).ready(function() {
  $('#map').gmap().bind('init', init_static_map);
});