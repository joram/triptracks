function geohashBounds(){
    bbox = map.getBounds();
    ne = bbox.getNorthEast();
    sw = bbox.getSouthWest();
    h1 = Geohash.encode(ne.lat(), ne.lng());
    h2 = Geohash.encode(sw.lat(), sw.lng());
    for(i=0; i<h1.length; i++){
      prefix1 = h1.substring(0, i);
      prefix2 = h2.substring(0, i);
        if(prefix1 !== prefix2){
            return h1.substring(0, i-1);
        }
    }
    return "";
}


class RoutesCache {
    constructor() {
        this.fetched_hashes = {};
        this.routes = {};
        this.curr_zoom = -1;
        var self = this;
        this.have = function (zoom, geohash){
            if (!(geohash in this.fetched_hashes)){
                return false;
            }
            return this.fetched_hashes[geohash].contains(map.zoom);
        };

        this.update_zoom = function () {
          $.each(this.routes, function(pub_id, route){
            route.show(map.zoom);
          });
        };

        this.update_bounds = function () {
            console.log("updating bounds");
            var geohash = geohashBounds();
            if(self.have(map.zoom, geohash)){
                console.log("already have ", geohash, zoom);
                return false;
            }
            self.getRoutes();
            return true;
        };

        this.getRoutes = function () {
          console.log("getting routes");
          var url = window.location.href;
          if(!url.endsWith("/")){url += "/"}
          url += "routes?bbox="+map.getBounds().toUrlValue()+"&zoom="+map.getZoom();
          $.ajax({
            url: url,
            success: this.loadRoutes,
          });
        };

        this.loadRoutes = function (data){
            data = JSON.parse(data);
            $.each(data.routes, function(pub_id, route){
              self.loadRoute(pub_id, route, data.zoom);
            });
        };

        this.loadRoute = function (pub_id, route, zoom){
          if(!(pub_id in this.routes)){
                this.routes[pub_id] = new Route(route.name, pub_id)
          }
          this.routes[pub_id].add_lines(route.lines, zoom);
          this.routes[pub_id].show(zoom);
          }
        }

}
