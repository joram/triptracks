class Route {
    constructor(name, pub_id) {
        this.name = name;
        this.pub_id = pub_id;
        this.lines = {};
        this.map_lines = {};
        this.curr_zoom = -1;
    }

    add_lines(lines, zoom) {
        this.lines[zoom] = lines;


        this.map_lines[zoom] = [];
        $.each(route.lines[zoom], function(i, coords){
            latLngs = [];
            $.each(coords, function (j, coord){
              latLngs.push({lat: coord[0], lng: coord[1]})
            });
            line = new google.maps.Polyline({
              path: latLngs,
              geodesic: true,
              strokeColor: '#FF0000',
              strokeOpacity: 1.0,
              strokeWeight: 2
            });
            line.setMap(map);
            this.map_lines[zoom].push(line);
        });
    }

    show(zoom){
        if(zoom==this.curr_zoom) {
            console.log("already showing ", this.pub_id, " at ", zoom);
            return
        }

        $.each(route.map_lines[zoom], function(i, line){
            line.setMap(map);
        });

        $.each(route.map_lines[this.curr_zoom], function(i, line){
            line.setMap();
        });
        this.curr_zoom = zoom;
    }


}