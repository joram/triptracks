
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
				success: @add_item,
				failure: @ajax_failure,
				dataType: 'json'
			});	
		)
		@add_on_clicks()

	ajax_failure: (data) ->
		console.log "failed"
		console.log data

	uuid = ->
	  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) ->
	    r = Math.random() * 16 | 0
	    v = if c is 'x' then r else (r & 0x3|0x8)
	    v.toString(16)
	  )

	add_item: (data) =>
		console.log data.html
		$("#items").prepend data.html
		@add_on_clicks()

	delete_item: (item) ->
		item = $(item)
		$.ajax
			type: "DELETE",
			url: item.data("editUri"),
			data: JSON.stringify({}),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",
			success: ->
				item.remove()

	update_item: (data) ->
		console.log data.item
		item = $(data.item)
		data.id = item.attr('id')
		data.name = data.name || item.find(".item-name").innerHTML
		data.quantity = data.quantity || item.find(".item-quantity")[0].innerHTML
		data.csrfmiddlewaretoken = item.data('csrf')
		data.item_type = "P"
		data.item = item.find('.item.active').data('itemId')

		console.log data

		$.ajax
			type: "PUT",
			url: item.data("editUri"),
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",

	add_on_clicks: =>
		for control in $(".change-item.carousel-control")
			do (control) =>
				$(control).on "click", (event) =>
					setTimeout(=>
						item_id = $(control).data('itemId')
						item = $("#"+item_id)[0]
						@update_item {item:item}
					, 1000)
		
		$.fn.editable.defaults.mode = 'inline'
		for item_name in $('.change-item.item-name')
			do (item_name) =>
				$(item_name).editable {
					showbuttons: false,
					type: 'text',
					success: (response, new_name) =>
						item_id = $(item_name).data('itemId')
						item = $("#"+item_id)[0]
						@update_item {item: item, name:new_name}
				}

		for item_quantity in $('.change-item.item-quantity')
			do (item_quantity) =>
				$(item_quantity).editable {
					showbuttons: false,
					type: 'select',
					source: ->
						values = []
						for i in [1..10]
							values.push {value: i, text: ""+i}
						return values
					success: (response, new_quantity) =>
						item_id = $(item_quantity).data('itemId')
						item = $("#"+item_id)[0]
						@update_item {item:item, quantity:new_quantity}
				}
		$('.packing-list-item .delete-item').on "click", (event) =>
			@delete_item event.toElement.closest('.packing-list-item')


$(document).ready ->
  new window.PackingListEditor()
