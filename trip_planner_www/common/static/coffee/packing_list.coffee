
class window.PackingListEditor

	constructor: () ->
		$( "#search" ).submit( (event) ->
			event.preventDefault()
			search_text = $("#search_text").val()
			search_url = $('#search').data().searchUri
			csrf_token = $('#search').data().csrf
			console.log(search_text)
			console.log(search_url)
			$.ajax({
				type: "POST",
				url: search_url,
				data: {
					search_text: search_text,
					csrfmiddlewaretoken: csrf_token },
				success: @update_items,
				dataType: 'json'
			});	
		)

	update_items: (data) ->
		console.log(data)

$(document).ready ->
  new window.PackingListEditor()
