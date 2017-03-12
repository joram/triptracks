
window.google_maps_loaded = () => $("#map").trigger('google_maps_loaded');

window.RouteViewer = class RouteViewer {

	load_google_maps(api_key, callback_func) {
		let fileref = document.createElement('script');
		fileref.setAttribute("async", "");
		fileref.setAttribute("defer", "");
		fileref.setAttribute("type", "text/javascript");
		let url = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=drawing`;
		if (callback_func !== null) {
			url += `&callback=${callback_func}`;
		}
		fileref.setAttribute("src", url);
		return document.getElementsByTagName("head")[0].appendChild(fileref);
	}

	constructor(element_id, load_js) {
		this.build_map = this.build_map.bind(this);
		this.load_map_data = this.load_map_data.bind(this);
		this.add_line = this.add_line.bind(this);
		this.element_id = element_id;
		this.lines = [];
		this.markers = [];
		this.m = $(`#${this.element_id}`);
		this.m.on('google_maps_loaded', this.build_map);
		this.load_google_maps(this.m.data('googleMapsApiKey'), "google_maps_loaded" );
	}

	build_map() {
		let map = new google.maps.Map(document.getElementById(this.element_id), {});

		// config
		map.setCenter({
			lat: parseFloat(this.m.data('centerLat')),
			lng: parseFloat(this.m.data('centerLng'))});
		map.setZoom(15);
		map.setMapTypeId(google.maps.MapTypeId.TERRAIN);


		this.drawingManager = new google.maps.drawing.DrawingManager({
			drawingControl: true,
			drawingControlOptions: {
				position: google.maps.ControlPosition.TOP_LEFT,
				drawingModes: [
					google.maps.drawing.OverlayType.MARKER,
					google.maps.drawing.OverlayType.POLYLINE,
				]},
		});
		this.drawingManager.setMap(map);

		return $.ajax({
			method: "GET",
			url: `/api/v1/route/${this.m.data('routeId')}/`,
			success: this.load_map_data
		});
	}

	load_map_data(data) {
//        if (data['center'] == null) {
//            data['center'] = {x:49, y:-123}
//        }
		console.log(data);

		if (data['markers'] !== null) {
			$.each(data['markers']['coordinates'], this.add_marker);
		}

		if (data['lines'] !== null) {
		 	return $.each(data['lines']['coordinates'], (index, line) => {
		 		return this.add_line(line);
	}
		 	);
	}
	}

	add_line(line_coords) {
		let line_coordinates = [];
		$.each(line_coords, (index, point) => line_coordinates.push({lat: point[1], lng: point[0]}));
		let line = new google.maps.Polyline({path: line_coordinates});
		this.lines.push(line);

		line.setMap(this.drawingManager.map);
		line.list_index = this.lines.indexOf(line);
		return line;
	}

	add_marker(coord) {
		let marker = new google.maps.Marker({
			'position': new google.maps.LatLng(coord[0], coord[1]),
			'draggable': false,
			'map': this.drawingManager.map });
		this.markers.add(marker);
		marker.list_index = markers.indexOf(marker);
		return marker;
	}
};

