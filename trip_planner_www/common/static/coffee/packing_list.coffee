
class window.PackingListEditor

	constructor: () ->
		$( "#search" ).submit( (event) =>
			event.preventDefault()
			search_text = $("#search_text").val()
			search_url = $('#search').data().searchUri
			csrf_token = $('#search').data().csrf
			$.ajax({
				type: "POST",
				url: search_url,
				data: {
					search_text: search_text,
					csrfmiddlewaretoken: csrf_token },
				success: @update_items,
				failure: @ajax_failure,
				dataType: 'json'
			});	
		)

	ajax_failure: ->
		console.log "failed"

	update_items: (data) ->
		all_html = "<div class='row'>"
		for item in data.items
			html = '
			<div class="col-xs-3">
	        	<a href="#" class="thumbnail">
	            	<img src="'+item.img_href+'" class="img-responsive">
	        	</a>
			</div>'
			all_html += html

		all_html += "</div>"
		console.log all_html
		$("#possible_items").html all_html

$(document).ready ->
  new window.PackingListEditor()
