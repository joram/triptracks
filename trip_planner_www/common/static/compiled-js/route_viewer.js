(function() {
  var bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  window.google_maps_loaded = function() {
    return $("#map").trigger('google_maps_loaded');
  };

  window.RouteViewer = (function() {
    RouteViewer.prototype.load_google_maps = function(api_key, callback_func) {
      var fileref, url;
      fileref = document.createElement('script');
      fileref.setAttribute("async", "");
      fileref.setAttribute("defer", "");
      fileref.setAttribute("type", "text/javascript");
      url = "https://maps.googleapis.com/maps/api/js?key=" + api_key + "&libraries=drawing";
      if (callback_func !== null) {
        url += "&callback=" + callback_func;
      }
      fileref.setAttribute("src", url);
      return document.getElementsByTagName("head")[0].appendChild(fileref);
    };

    function RouteViewer(element_id, load_js) {
      this.element_id = element_id;
      this.add_line = bind(this.add_line, this);
      this.load_map_data = bind(this.load_map_data, this);
      this.build_map = bind(this.build_map, this);
      this.lines = [];
      this.markers = [];
      this.m = $("#" + this.element_id);
      this.m.on('google_maps_loaded', this.build_map);
      this.load_google_maps(this.m.data('googleMapsApiKey'), "google_maps_loaded");
    }

    RouteViewer.prototype.build_map = function() {
      var map;
      map = new google.maps.Map(document.getElementById(this.element_id), {});
      map.setCenter({
        lat: parseFloat(this.m.data('centerLat')),
        lng: parseFloat(this.m.data('centerLng'))
      });
      map.setZoom(15);
      map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
      this.drawingManager = new google.maps.drawing.DrawingManager({
        drawingControl: true,
        drawingControlOptions: {
          position: google.maps.ControlPosition.TOP_LEFT,
          drawingModes: [google.maps.drawing.OverlayType.MARKER, google.maps.drawing.OverlayType.POLYLINE]
        }
      });
      this.drawingManager.setMap(map);
      return $.ajax({
        method: "GET",
        url: "/api/v1/route/" + this.m.data('routeId') + "/",
        success: this.load_map_data
      });
    };

    RouteViewer.prototype.load_map_data = function(data) {
      console.log(data);
      if (data['markers'] !== null) {
        $.each(data['markers']['coordinates'], this.add_marker);
      }
      if (data['lines'] !== null) {
        return $.each(data['lines']['coordinates'], (function(_this) {
          return function(index, line) {
            return _this.add_line(line);
          };
        })(this));
      }
    };

    RouteViewer.prototype.add_line = function(line_coords) {
      var line, line_coordinates;
      line_coordinates = [];
      $.each(line_coords, function(index, point) {
        return line_coordinates.push({
          lat: point[1],
          lng: point[0]
        });
      });
      line = new google.maps.Polyline({
        path: line_coordinates
      });
      this.lines.push(line);
      line.setMap(this.drawingManager.map);
      line.list_index = this.lines.indexOf(line);
      return line;
    };

    RouteViewer.prototype.add_marker = function(coord) {
      var marker;
      marker = new google.maps.Marker({
        'position': new google.maps.LatLng(coord[0], coord[1]),
        'draggable': false,
        'map': this.drawingManager.map
      });
      this.markers.add(marker);
      marker.list_index = markers.indexOf(marker);
      return marker;
    };

    return RouteViewer;

  })();

}).call(this);
