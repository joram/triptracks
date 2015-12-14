
window.google_maps_loaded = () ->
	$("#map").trigger('google_maps_loaded')

class window.RouteViewer

	load_google_maps: (api_key, callback_func) ->
		fileref = document.createElement('script')
		fileref.setAttribute("async", "")
		fileref.setAttribute("defer", "")
		fileref.setAttribute("type", "text/javascript")
		url = "https://maps.googleapis.com/maps/api/js?key=" + api_key + "&libraries=drawing"
		if callback_func != null
			url += "&callback="+callback_func
		fileref.setAttribute("src", url)
		document.getElementsByTagName("head")[0].appendChild(fileref)

	constructor: (@element_id, load_js) ->
		@lines = []
		@markers = []
		@m = $("#"+@element_id)
		@m.on('google_maps_loaded', @build_map)
		@load_google_maps(@m.data('googleMapsApiKey'), "google_maps_loaded" )

	build_map: () =>
		map = new google.maps.Map(document.getElementById(@element_id), {})

		# config
		map.setCenter({
			lat: parseFloat(@m.data('centerLat')),
			lng: parseFloat(@m.data('centerLng'))})
		map.setZoom(15)
		map.setMapTypeId(google.maps.MapTypeId.TERRAIN)


		@drawingManager = new google.maps.drawing.DrawingManager({
			drawingControl: true,
			drawingControlOptions: {
				position: google.maps.ControlPosition.TOP_LEFT,
				drawingModes: [
					google.maps.drawing.OverlayType.MARKER,
					google.maps.drawing.OverlayType.POLYLINE,
				]},
		})
		@drawingManager.setMap(map);

		$.ajax({
			method: "GET",
			url: "/api/v1/route/"+@m.data('routeId')+"/",
			success: @load_map_data
		})

	load_map_data: (data) =>
		console.log(data)

		if data['markers'] != null
			$.each(data['markers']['coordinates'], @add_marker)

		if data['lines'] != null
		 	$.each(data['lines']['coordinates'], (index, line) =>
		 		@add_line(line)
		 	)

	add_line: (line_coords) =>
		line_coordinates = []
		$.each(line_coords, (index, point) ->
			line_coordinates.push({lat: point[1], lng: point[0]})
		)
		line = new google.maps.Polyline({path: line_coordinates})
		@lines.push(line)

		line.setMap(@drawingManager.map)
		line.list_index = @lines.indexOf(line)
		return line

	add_marker: (coord) ->
		marker = new google.maps.Marker({
			'position': new google.maps.LatLng(coord[0], coord[1]),
			'draggable': false,
			'map': @drawingManager.map })
		@markers.add(marker)
		marker.list_index = markers.indexOf(marker)
		return marker

