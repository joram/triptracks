
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
					quantity: 12,
					search_text: search_text,
					csrfmiddlewaretoken: csrf_token },
				success: @update_items,
				failure: @ajax_failure,
				dataType: 'json'
			});	
		)

	ajax_failure: ->
		console.log "failed"

	uuid = ->
	  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) ->
	    r = Math.random() * 16 | 0
	    v = if c is 'x' then r else (r & 0x3|0x8)
	    v.toString(16)
	  )

	update_items: (data) ->
		id = uuid()
		item_carousel = $('<div />', {
			"id": id,
			"class": "packing-list-item carousel slide col-md-2",
			"data-ride": "carousel"})
		$("#items").prepend item_carousel

		item_html = $('<div />', {
			"class": 'carousel-inner',
			"role": "listbox",
		})
		item_carousel.prepend item_html

		first = true
		for item in data.items
			div_class = "item"
			if first
				div_class += " active"
				first = false

			slide = $('<div />', {"class": div_class,})
			slide.appendTo(item_html)
			img = $('<img />', {"src": item.img_href,})
			img.appendTo(slide)

		left_html = $('<a class="left carousel-control" href="#'+id+'" role="button" data-slide="prev">
			<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
			<span class="sr-only">Previous</span>
		</a>')
		item_carousel.append left_html

		right_html = $('<a class="right carousel-control" href="#'+id+'" role="button" data-slide="next">
			<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
			<span class="sr-only">Next</span>
		</a>')
		item_carousel.append right_html

		item_carousel.carousel({
        	interval: 0
    	})

$(document).ready ->
  new window.PackingListEditor()
