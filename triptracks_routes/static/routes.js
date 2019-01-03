class Route {
  constructor(name, pub_id) {
    this.name = name;
    this.pub_id = pub_id;
    this.lines = {};
    this.map_lines = {};
    this.curr_zoom = -1;
    var self = this;

    this.add_lines = function (lines, zoom) {
        // console.log("adding line ", this.pub_id, zoom, lines[0].length);
        self.lines[zoom] = lines;


        self.map_lines[zoom] = [];
        $.each(lines, function (i, coords) {
          var latLngs = [];
          $.each(coords, function (j, coord) {
            latLngs.push({lat: coord[0], lng: coord[1]})
          });
          var line = new google.maps.Polyline({
            path: latLngs,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
          });
          line.setMap(map);
          self.map_lines[zoom].push(line);
        });
      };


    this.show = function (zoom) {

        if (zoom === self.curr_zoom) {
          console.log("already showing ", self.pub_id, " at ", zoom);
          return
        }
        console.log("showing new route", self.lines.length, self.map_lines.length);

        $.each(self.map_lines[zoom], function (i, line) {
          line.setMap(map);
        });

        $.each(self.map_lines[self.curr_zoom], function (i, line) {
          line.setMap();
        });
        self.curr_zoom = zoom;
      }
    }
}
