(function() {
  var bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    hasProp = {}.hasOwnProperty;

  window.RouteEditor = (function(superClass) {
    extend(RouteEditor, superClass);

    function RouteEditor(element_id, load_js) {
      this.element_id = element_id;
      this.updated_line = bind(this.updated_line, this);
      this.add_line = bind(this.add_line, this);
      this.ajax_update_route = bind(this.ajax_update_route, this);
      RouteEditor.__super__.constructor.call(this, this.element_id, load_js);
    }

    RouteEditor.prototype.ajax_update_route = function() {
      var coordinates, data, line_coordinates;
      coordinates = [];
      $.each(this.markers, function(i, marker) {
        if (marker.position.lat() && marker.map !== null) {
          return coordinates.push([marker.position.lat(), marker.position.lng()]);
        }
      });
      line_coordinates = [];
      $.each(this.lines, function(i, line) {
        var line_points, points;
        points = line.getPath().getArray();
        if (points.toString() !== "(NaN, NaN)" && line.map !== null) {
          line_points = [];
          $.each(points, function(i, point) {
            return line_points.push([point.lat(), point.lng()]);
          });
          return line_coordinates.push(line_points);
        }
      });
      data = {
        'action': 'update_map',
        'markers': {
          "type": "MultiPoint",
          "coordinates": coordinates
        },
        'lines': {
          'type': 'MultiLineString',
          'coordinates': line_coordinates
        }
      };
      console.log(data);
      return $.ajax({
        method: "PUT",
        url: "/api/v1/route/" + this.m.data('routeId') + "/",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data)
      });
    };

    RouteEditor.prototype.add_line = function(line_coords) {
      var line;
      line = RouteEditor.__super__.add_line.call(this, line_coords);
      line.setDraggable(true);
      line.setEditable(true);
      google.maps.event.addListener(line, "dragend", this.updated_line);
      google.maps.event.addListener(line.getPath(), "insert_at", this.updated_line);
      google.maps.event.addListener(line.getPath(), "remove_at", this.updated_line);
      return google.maps.event.addListener(line.getPath(), "set_at", this.updated_line);
    };

    RouteEditor.prototype.updated_line = function() {
      return this.ajax_update_route();
    };

    RouteEditor.prototype.add_info_window_marker = function(marker) {
      marker.info_window = new google.maps.InfoWindow;
      google.maps.event.addListener(marker, "rightclick", function(event) {
        close_all_info_windows();
        return marker.info_window.open(drawingManager.map, marker);
      });
      return marker.info_window.setContent("<div style='width:100px'><button onclick='remove_marker(" + marker.list_index + ");'>remove</button></div>");
    };

    RouteEditor.prototype.add_info_window_line = function(line) {
      line.info_window = new google.maps.InfoWindow;
      google.maps.event.addListener(line, "rightclick", (function(_this) {
        return function(event) {
          _this.close_all_info_windows();
          line.info_window.setPosition(event.latLng);
          return line.info_window.open(_this.drawingManager.map);
        };
      })(this));
      return line.info_window.setContent("<div style='width:100px'><button onclick='remove_line(" + line.list_index + ");'>remove</button></div>");
    };

    RouteEditor.prototype.close_all_info_windows = function() {
      $.each(this.markers, function(i, marker) {
        return marker.info_window.close();
      });
      return $.each(this.lines, function(i, line) {
        return line.info_window.close();
      });
    };

    return RouteEditor;

  })(RouteViewer);

}).call(this);
