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
    $("#search_text").keyup(debounce(function(){
        update_search_items()
    }, 200));

    $('#packing-list-name').editable({
        mode:'inline',
        showbuttons:false,
    });
    $('#packing-list-name').on('save', function(e, params) {
        update_packing_list_meta(params.newValue);
    })
})

function update_packing_list_meta(name){
    packing_list_pub_id = $("div#packing-list-pub-id").text();
    $.ajax({
        type: "POST",
        url: "/packing/list/"+packing_list_pub_id+"/edit",
        data: {
            name: name,
        },
        dataType: 'json'
    });
}

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

        item = $('' +
        '<div class="col-sm-3 packing-item" id="search_item_'+pub_id+'">'+
        '  <div class="card">'+
        '    <div class="card-body">'+
        '      <img class="card-img-top item-search-image" data-item-pub-id="'+pub_id+'" src="'+href+'" alt="Card image cap">'+
        '    </div>'+
        '  </div>'+
        '</div>')

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
