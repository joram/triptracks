function geohashBounds(){
    bbox = map.getBounds();
    ne = bbox.getNorthEast();
    sw = bbox.getSouthWest();
    h1 = Geohash.encode(ne.lat(), ne.lng());
    h2 = Geohash.encode(sw.lat(), sw.lng());
    for(i=0; i<h1.length; i++){
      prefix1 = h1.substring(0, i);
      prefix2 = h2.substring(0, i);
        if(prefix1 != prefix2){
            return h1.substring(0, i-1);
        }
    }
    return "";
}


class RoutesCache {
    constructor() {
        this.fetched_hashes = {};
        this.routes = {};
        this.curr_zoom = map.zoom;
    }

    have(zoom, geohash){
        if (!(geohash in this.fetched_hashes)){
            return false;
        }
        return this.fetched_hashes[geohash].contains(map.zoom);
    }

    update_zoom() {
      $.each(this.routes, function(pub_id, route){
        route.show(map.zoom);
      });
    }

    update_bounds() {
        var geohash = geohashBounds();
        if(this.have(map.zoom, geohash)){
            console.log("already have ", geohash, zoom);
            return false;
        }
        return true;
    }

    getRoutes() {
	  url = window.location.href;
	  if(!url.endsWith("/")){url += "/"}
	  url += "routes?bbox="+map.getBounds().toUrlValue()+"&zoom="+map.getZoom();
	  $.ajax({
	    url: url,
	    success: this.loadRoutes,
	  });
    }

    loadRoutes(data){
      data = JSON.parse(data);
      $.each(data.routes, function(pub_id, route){
        loadRoute(pub_id, route, data.zoom);
      });
      showRoutes();
    }

    loadRoute(pub_id, route, zoom){
	  if(!(pub_id in this.routes)){
          this.routes[pub_id] = new Route(route.name, pub_id)
	  }
	  this.routes[pub_id].add_lines(route.lines, zoom);
    }

}