function debounce(fn, delay) {
  var timer = null;
  return function () {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}


$(document).ready(function() {
    let search_text = $("#search_text");
    let search_url = $('#search_text').data().searchUri;
    let csrf_token = $('#search_text').data().csrf;
    search_text.keyup(debounce(function(){
        update_search_items()
    }, 200));
})

function update_search_items(){
	search_url = $('#search_text').data().searchUri;
	search_text = $("#search_text").val();
	$.ajax({
		type: "GET",
		url: search_url+"?quantity=12&text="+ search_text,
		success: add_items_to_carousel,
		dataType: 'json'
	});
}

function add_items_to_carousel(data) {
	carousel = $("#search-items");
	carousel.empty();
	data["items"].forEach(function (item){
        href = item["img_href"];
        pub_id = item["pub_id"];
    	item = $(`<div class="packing-item col-lg-3 col-md-3 col-sm-3 col-xs-6" id="search_item_`+pub_id+`">
            <img data-item-pub-id="`+pub_id+`" data-search-text="`+search_text+`" class="item-search-image" src="`+href+`">
        </div>`);
        item.click("click", attach_onclick_handler(pub_id));
        carousel.append(item);
    });
}
function attach_onclick_handler(pub_id){
    return function(event){
        add_item_to_packing_list(pub_id, $("#search_text").val());
    }
}

function add_item_to_packing_list(item_pub_id, title) {
    packing_list_pub_id = $("div#packing-list-pub-id").text();
    item = $("#search_item_"+item_pub_id);
    item.detach()
    $("#packing-list-items").append(item);
    add_item_url = "/packing/list/"+packing_list_pub_id+"/add/"+item_pub_id

    $.ajax({
      type: "GET",
      url: add_item_url,
      dataType: 'json'
    });
}

function add_item_to_packing_list_success(){
}
