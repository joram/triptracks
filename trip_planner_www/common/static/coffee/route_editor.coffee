
class window.RouteEditor extends RouteViewer

	constructor: (@element_id, load_js) ->
		super(@element_id, load_js)

	ajax_update_route: () =>
		coordinates = []
		$.each(@markers, (i, marker) ->
			if marker.position.lat() && marker.map != null
				coordinates.push([marker.position.lat(), marker.position.lng()])	
		)

		line_coordinates = []
		$.each(@lines, (i, line) ->
			points = line.getPath().getArray()
			if points.toString() != "(NaN, NaN)" && line.map != null
				line_points = []
				$.each(points, (i, point) ->
					line_points.push([point.lat(), point.lng()])
				)
				line_coordinates.push(line_points)
		)

		data = {
			'action': 'update_map',
			'markers': { "type": "MultiPoint", "coordinates": coordinates },
			'lines': {'type': 'MultiLineString', 'coordinates': line_coordinates},
		}
		console.log(data)

		$.ajax({
		    method: "PUT",
		    url: "/api/v1/route/"+@m.data('routeId')+"/",
		    contentType: "application/json; charset=utf-8",
		    data: JSON.stringify(data),
		})

	# add_marker: (coord) ->
	# 	marker = super(coord)
	# 	marker.setDraggable(true)
	# 	google.maps.event.addListener(marker, "dragend", moved_marker)

	add_line: (line_coords) =>
		line = super(line_coords)
		line.setDraggable(true)
		line.setEditable(true)

		google.maps.event.addListener(line, "dragend", @updated_line);
		google.maps.event.addListener(line.getPath(), "insert_at", @updated_line);
		google.maps.event.addListener(line.getPath(), "remove_at", @updated_line);
		google.maps.event.addListener(line.getPath(), "set_at", @updated_line);

	updated_line: () =>
		@ajax_update_route()

	add_info_window_marker: (marker) ->
		marker.info_window = new google.maps.InfoWindow;
		google.maps.event.addListener(marker, "rightclick", (event) ->
			close_all_info_windows();
			marker.info_window.open(drawingManager.map, marker);
		);
		marker.info_window.setContent("<div style='width:100px'><button onclick='remove_marker("+marker.list_index+");'>remove</button></div>");

	add_info_window_line: (line) ->
		line.info_window = new google.maps.InfoWindow;
		google.maps.event.addListener(line, "rightclick", (event) =>
			@close_all_info_windows();
			line.info_window.setPosition(event.latLng);
			line.info_window.open(@drawingManager.map);
		)
		line.info_window.setContent("<div style='width:100px'><button onclick='remove_line("+line.list_index+");'>remove</button></div>");

	close_all_info_windows: () ->
		$.each(@markers, (i, marker) ->
			marker.info_window.close();
		)
		$.each(@lines, (i, line) ->
			line.info_window.close();
		)
