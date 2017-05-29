
window.PackingListEditor = class PackingListEditor {

	constructor() {
		this.add_item = this.add_item.bind(this);
		this.add_on_clicks = this.add_on_clicks.bind(this);
		$('.carousel').carousel();
		$( "#search" ).submit( event => {
			event.preventDefault();
			let search_text = $("#search_text").val();
			let search_url = $('#search').data().searchUri;
			let csrf_token = $('#search').data().csrf;
			return $.ajax({
				type: "POST",
				url: search_url,
				data: {
					quantity: 12,
					search_text,
					csrfmiddlewaretoken: csrf_token },
				success: this.add_item,
				failure: this.ajax_failure,
				dataType: 'json'
			});
		}
		);

		this.add_on_clicks();
		$('#packing-list-name').editable({
			showbuttons: false,
			type: 'text',
			success: (response, new_name) => {
				$("#packing-list").data("name", new_name);
				return this.update_packing_list();
			}
		});
	}

	ajax_failure(data) {
		console.log("failed");
		return console.log(data);
	}

	update_packing_list() {
		let data = {
			name: $("#packing-list").data('name'),
		};

		return $.ajax({
			type: "PUT",
			url: `/api/v1/packing_list/${$("#packing-list").data('id')}/`,
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8"
		}
		);
	}

	add_item(data) {
		$("#items").prepend(data.html);
		return this.add_on_clicks();
	}

	delete_item(item) {
		item = $(item);
		return $.ajax({
			type: "DELETE",
			url: item.data("editUri"),
			data: JSON.stringify({}),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",
			success() {
				return item.remove();
			}
		});
	}

	update_item(item) {
		let data = {
			id: $(item).data('id'),
			item: $(item).data('item'),
			item_type: $(item).data('item-type'),
			name: $(item).data('name'),
			quantity: $(item).data('quantity'),
		};

		return $.ajax({
			type: "PUT",
			url: item.data("editUri"),
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8"
		}
		);
	}

	add_on_clicks() {
		let item;
		$(".packing-list-item.carousel").on('slid.bs.carousel', event => {
			item = $(event.target);
			item.data('item', item.find(".item.active").data('itemId'));
			return this.update_item(item);
		}
		);

		$('.packing-list-item .delete-item').on("click", event => {
			return this.delete_item(event.toElement.closest('.packing-list-item'));
		}
		);

		$.fn.editable.defaults.mode = 'inline';

		for (let item_name of Array.from($('.change-item.item-name'))) {
			(item_name => {
				return $(item_name).editable({
					showbuttons: false,
					type: 'text',
					success: (response, new_name) => {
						item = $(item_name).closest(".packing-list-item");
						item.data('name', new_name);
						return this.update_item(item);
					}
				});
			})(item_name);
		}

		return Array.from($('.change-item.item-quantity')).map((item_quantity) =>
			(item_quantity => {
				return $(item_quantity).editable({
					showbuttons: false,
					type: 'select',
					source() {
						let values = [];
						for (let i = 1; i <= 10; i++) {
							values.push({value: i, text: `${i}`});
						}
						return values;
					},
					success: (response, new_quantity) => {
						item = $(item_quantity).closest(".packing-list-item");
						item.data('quantity', new_quantity);
						return this.update_item(item);
					}
				});
			})(item_quantity));
	}
};


$(document).ready(() => new window.PackingListEditor());
