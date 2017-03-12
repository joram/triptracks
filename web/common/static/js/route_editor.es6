
window.RouteEditor = class RouteEditor extends window.RouteViewer {

	constructor(element_id, load_js) {
    	super(element_id, load_js)
		this.ajax_update_route = this.ajax_update_route.bind(this);
		this.add_line = this.add_line.bind(this);
		this.updated_line = this.updated_line.bind(this);
        console.log("created route Editor")
    }

	ajax_update_route() {
		let coordinates = [];
		$.each(this.markers, function(i, marker) {
			if (marker.position.lat() && (marker.map !== null)) {
				return coordinates.push([marker.position.lat(), marker.position.lng()]);
			}
		});

		let line_coordinates = [];
		$.each(this.lines, function(i, line) {
			let points = line.getPath().getArray();
			if ((points.toString() !== "(NaN, NaN)") && (line.map !== null)) {
				let line_points = [];
				$.each(points, (i, point) => line_points.push([point.lat(), point.lng()]));
				return line_coordinates.push(line_points);
			}
		});

		let data = {
			'action': 'update_map',
			'markers': { "type": "MultiPoint", "coordinates": coordinates },
			'lines': {'type': 'MultiLineString', 'coordinates': line_coordinates},
		};
		console.log(data);

		return $.ajax({
		    method: "PUT",
		    url: `/api/v1/route/${this.m.data('routeId')}/`,
		    contentType: "application/json; charset=utf-8",
		    data: JSON.stringify(data),
		});
	}

	// add_marker: (coord) ->
	// 	marker = super(coord)
	// 	marker.setDraggable(true)
	// 	google.maps.event.addListener(marker, "dragend", moved_marker)

	add_line(line_coords) {
		let line = super.add_line(line_coords);
		line.setDraggable(true);
		line.setEditable(true);

		google.maps.event.addListener(line, "dragend", this.updated_line);
		google.maps.event.addListener(line.getPath(), "insert_at", this.updated_line);
		google.maps.event.addListener(line.getPath(), "remove_at", this.updated_line);
		return google.maps.event.addListener(line.getPath(), "set_at", this.updated_line);
	}

	updated_line() {
		return this.ajax_update_route();
	}

	add_info_window_marker(marker) {
		marker.info_window = new google.maps.InfoWindow;
		google.maps.event.addListener(marker, "rightclick", function(event) {
			close_all_info_windows();
			return marker.info_window.open(drawingManager.map, marker);
		});
		return marker.info_window.setContent(`<div style='width:100px'><button onclick='remove_marker(${marker.list_index});'>remove</button></div>`);
	}

	add_info_window_line(line) {
		line.info_window = new google.maps.InfoWindow;
		google.maps.event.addListener(line, "rightclick", event => {
			this.close_all_info_windows();
			line.info_window.setPosition(event.latLng);
			return line.info_window.open(this.drawingManager.map);
		}
		);
		return line.info_window.setContent(`<div style='width:100px'><button onclick='remove_line(${line.list_index});'>remove</button></div>`);
	}

	close_all_info_windows() {
		$.each(this.markers, (i, marker) => marker.info_window.close());
		return $.each(this.lines, (i, line) => line.info_window.close());
	}
};
