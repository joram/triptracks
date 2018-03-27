$(document).ready(function() {
    let search_text = $("#search_text");
    let search_url = $('#search_text').data().searchUri;
    let csrf_token = $('#search_text').data().csrf;
    console.log("hello");
    search_text.change(function () {
        console.log("search results changed");
        update_search_items()
    });
})

function update_search_items(){
	console.log("updating search results");
	search_url = $('#search_text').data().searchUri;
	search_text = $("#search_text").val();

	$.ajax({
		type: "GET",
		url: search_url+"?quantity=6&text="+ search_text,
		success: add_items_to_carousel,
		dataType: 'json'
	});

}

function create_item_image(href, pub_id, total){
	col_width = Math.floor(12/total);
    return $(`<div class="col-md-`+col_width+`">`+
        `<img data-item-pub-id="`+pub_id+`" class="item-search-image" src="`+href+`">`+
    	`</div>`);
}

function add_items_to_carousel(data) {
	console.log(data);
	carousel = $("#search-items");
	carousel.empty();
	data["items"].forEach(function (item){
        carousel.append(create_item_image(item["img_href"], item["pub_id"], data["count"]));
    });
}
//
// 	add_item(data) {
// 		$("#items").prepend(data.html);
// 		return this.add_on_clicks();
// 	}
//
// 	delete_item(item) {
// 		item = $(item);
// 		return $.ajax({
// 			type: "DELETE",
// 			url: item.data("editUri"),
// 			data: JSON.stringify({}),
// 			dataType: 'json',
// 			contentType: "application/json; charset=UTF-8",
// 			success() {
// 				return item.remove();
// 			}
// 		});
// 	}
//
// 	update_item(item) {
// 		let data = {
// 			id: $(item).data('id'),
// 			item: $(item).data('item'),
// 			item_type: $(item).data('item-type'),
// 			name: $(item).data('name'),
// 			quantity: $(item).data('quantity'),
// 		};
//
// 		return $.ajax({
// 			type: "PUT",
// 			url: item.data("editUri"),
// 			data: JSON.stringify(data),
// 			dataType: 'json',
// 			contentType: "application/json; charset=UTF-8"
// 		}
// 		);
// 	}
//
// 	add_on_clicks() {
// 		let item;
// 		$(".packing-list-item.carousel").on('slid.bs.carousel', event => {
// 			item = $(event.target);
// 			item.data('item', item.find(".item.active").data('itemId'));
// 			return this.update_item(item);
// 		}
// 		);
//
// 		$('.packing-list-item .delete-item').on("click", event => {
// 			return this.delete_item(event.toElement.closest('.packing-list-item'));
// 		}
// 		);
//
// 		$.fn.editable.defaults.mode = 'inline';
//
// 		for (let item_name of Array.from($('.change-item.item-name'))) {
// 			(item_name => {
// 				return $(item_name).editable({
// 					showbuttons: false,
// 					type: 'text',
// 					success: (response, new_name) => {
// 						item = $(item_name).closest(".packing-list-item");
// 						item.data('name', new_name);
// 						return this.update_item(item);
// 					}
// 				});
// 			})(item_name);
// 		}
//
// 		return Array.from($('.change-item.item-quantity')).map((item_quantity) =>
// 			(item_quantity => {
// 				return $(item_quantity).editable({
// 					showbuttons: false,
// 					type: 'select',
// 					source() {
// 						let values = [];
// 						for (let i = 1; i <= 10; i++) {
// 							values.push({value: i, text: `${i}`});
// 						}
// 						return values;
// 					},
// 					success: (response, new_quantity) => {
// 						item = $(item_quantity).closest(".packing-list-item");
// 						item.data('quantity', new_quantity);
// 						return this.update_item(item);
// 					}
// 				});
// 			})(item_quantity));
// 	}
// };
//
