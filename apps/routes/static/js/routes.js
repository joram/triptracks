var lines_cache = {};
var get_routes_calls_in_progress = 0;
var get_routes_max_calls = 10;

function load_google_maps(api_key, route_id) {
    this.route_id = route_id;
    this.lines = {};

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function load_all_routes_google_maps(api_key){
    this.lines = {};

    let fileref = document.createElement('script');
    fileref.setAttribute("async", "");
    fileref.setAttribute("defer", "");
    fileref.setAttribute("type", "text/javascript");

    let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing&callback=build_map_all_routes`;
    fileref.setAttribute("src", url);
    return document.getElementsByTagName("head")[0].appendChild(fileref);
}

function build_map_all_routes() {
    _build_map_routes("all")
}

function build_map_my_routes() {
    _build_map_routes("mine")
}

function _build_map_routes(filter) {

    navigator.geolocation.getCurrentPosition(function(position) {
        var center = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        let map_element = document.getElementById("map");
        map = new google.maps.Map(map_element, {
            zoom: 12,
            center: center,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
        });
        map_element.map = map;


        google.maps.event.addListener(map, 'bounds_changed', function() {
            if(get_routes_calls_in_progress >= get_routes_max_calls){
                return
            }
            get_routes_calls_in_progress +=1;
            bounds = map.getBounds().toUrlValue();
            return $.ajax({
                method: "GET",
                url: `/api/routes?filter=${filter}&bounds=${bounds}&zoom=${map.getZoom()}`,
                success: load_routes_data
            });
        });
    });

}

function build_map() {

    let map_element = document.getElementById("map");
    map = new google.maps.Map(map_element, {});
    map.setZoom(15);
    map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
    map_element.map = map;

    return $.ajax({
        method: "GET",
        url: `/api/v1/route/${this.route_id}/`,
        success: load_route_data
    });
}

function load_routes_data(data) {
    data.forEach(function (route){
        unload_route(route);
        if(!use_cached_lines(route)){
            load_route(route);
        }
    });
    get_routes_calls_in_progress -= 1;
}

function load_route_data(data) {
    load_route(data, true)
}

function unload_route(route) {
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    if (lines_cache[pub_id] != null){
        for(zoom in lines_cache[pub_id]) {
            if(lines_cache[pub_id][zoom] != null && zoom != zoom_level){
                lines_cache[pub_id][zoom]["googlemaps_lines"].forEach(function (google_line){
                    google_line.setMap(null);
                });
            }
        }
    }
}

function center(route){
    map_element = document.getElementById("map");
    center = route["center"];

    // recenter
    if (route['center'] !== null) {
        center = {
            lat: parseFloat(route['center']['coordinates'][0]),
            lng: parseFloat(route['center']['coordinates'][1])
        };
        map_element.map.setCenter(center);
    }
}

function use_cached_lines(route){
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    route_lines = route["lines"];

    if(lines_cache[pub_id] == null){
        return false;
    }
    if(lines_cache[pub_id][zoom_level] == null) {
        return false;
    }

    map_element = document.getElementById("map");
    google_lines = lines_cache[pub_id][zoom_level]["googlemaps_lines"];
    google_lines.forEach(function (google_line){
        google_line.setMap(map_element.map);
    });
    return true;
}

function load_route(route) {
    pub_id = route["pub_id"];
    zoom_level = route["zoom_level"];
    route_lines = route["lines"];

     // create new
     if (route['lines'] !== null) {
        google_lines = [];
        route['lines'].forEach(function (line) {
            google_line = create_line(line);
            (function(route) {
                google_line.addListener('click', function () {
                    show_route_details(route);
                });
            })(route);
            google_lines.push(google_line);
        });
        route["googlemaps_lines"] = google_lines;
     }

    // cache
    if(lines_cache[pub_id] == null){
        lines_cache[pub_id] = {};
    }
    if(lines_cache[pub_id][zoom_level] == null) {
        lines_cache[pub_id][zoom_level] = route;
    }
}

function show_route_details(route){
    $("#route_details_card").remove();
    pub_id = route["pub_id"];
    route_name = route["name"];
    route_description = route["description"];
    route_image_url = route["image_url"];
    is_mine = route["is_mine"];
    is_public = route["is_public"];

    img_top = "";
    if(route_image_url != ""){
        img_top = "<img class='card-img-top' src='https://www.trailpeak.com/"+route_image_url+"' alt='Card image cap'>";
    }
    privacy_buttons = "";
    if(is_mine){
        public_class = "";
        private_class = "active";
        if(is_public){
            public_class = "active";
            private_class = "";
        }
        privacy_buttons = "\
        <div class='btn-group btn-group-toggle public-toggle'> \
          <label class='route-public privacy_btn btn btn-secondary "+ public_class +"'  data-pub_id='"+pub_id+"'> \
            <input type='checkbox' autocomplete='off'> Public \
          </label> \
          <label class='route-private privacy_btn btn btn-secondary "+ private_class +"' data-pub_id='"+pub_id+"'> \
            <input type='checkbox' autocomplete='off' checked> Private \
          </label>  \
        </div>"
    }

    routeDetailsCard = $("<div id='route_details_card' class='card'> \
      <div class='card-header'>"+route_name+"</div>    \
      "+ img_top +"\
      <div class='card-body'> \
        <p class='card-text'>"+route_description+"</p> \
        \
        <div class='btn-group btn-group-toggle' role='group'> \
          <label class='btn btn-secondary'> \
            <input class='route-trip' type='checkbox' autocomplete='off' data-href='/trip/plan/create/?route=\"+pub_id+\"'> Plan Trip \
          </label> \
        </div> \
        "+privacy_buttons+" \
        </div> \
      </div> \
    </div>");

    $("#body").append(routeDetailsCard);

    $(".route-trip > input").on("click", function(e){
        toggle_button_group(e.target.parentNode);
    });

    $(".route-public > input").on("click", function(e){
        toggle_button_group(e.target.parentNode);
        route_pub_id = $(e.target.parentNode).data("pub_id");
        $.ajax({
            method: "POST",
            url: `/api/route/${route_pub_id}`,
            data: {'is_public': true}
        });
    });
    $(".route-private > input").on("click", function(e){
        toggle_button_group(e.target.parentNode);
        route_pub_id = $(e.target.parentNode).data("pub_id");
        $.ajax({
            method: "POST",
            url: `/api/route/${route_pub_id}`,
            data: {'is_public': false}
        });
    });


    function toggle_button_group(enabled_button){
        $(".privacy_btn").removeClass("active").removeAttr("aria-pressed");
        n = $(enabled_button);
        n.addClass("active").attr("aria-pressed", "true");
    }


}

