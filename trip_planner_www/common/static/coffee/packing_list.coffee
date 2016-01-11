
class window.PackingListEditor

	constructor: () ->
		$('.carousel').carousel()
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
		$('#packing-list-name').editable {
			showbuttons: false,
			type: 'text',
			success: (response, new_name) =>
				@update_packing_list({name:new_name})
		}

	ajax_failure: (data) ->
		console.log "failed"
		console.log data

	update_packing_list: (data) ->
		console.log data
		list_id = 1
		$.ajax
			type: "PUT",
			url: "/api/v1/packing_list/"+list_id+"/",
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",

	add_item: (data) =>
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

	update_item: (item) ->
		data = {
			id: $(item).data('id'),
			item: $(item).data('item'),
			item_type: $(item).data('item-type'),
			name: $(item).data('name'),
			quantity: $(item).data('quantity'),
		}

		$.ajax
			type: "PUT",
			url: item.data("editUri"),
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",

	add_on_clicks: =>
		$(".packing-list-item.carousel").on 'slid.bs.carousel', (event) =>
			item = $(event.target)
			item.data('item', item.find(".item.active").data('itemId'))
			@update_item item

		$('.packing-list-item .delete-item').on "click", (event) =>
			@delete_item event.toElement.closest('.packing-list-item')
		
		$.fn.editable.defaults.mode = 'inline'

		for item_name in $('.change-item.item-name')
			do (item_name) =>
				$(item_name).editable {
					showbuttons: false,
					type: 'text',
					success: (response, new_name) =>
						item = $(item_name).closest(".packing-list-item")
						item.data('name', new_name)
						@update_item item
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
						item = $(item_quantity).closest(".packing-list-item")
						item.data('quantity', new_quantity)
						@update_item item
				}


$(document).ready ->
	new window.PackingListEditor()
