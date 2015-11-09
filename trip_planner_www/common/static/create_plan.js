

function toggle_view(view_name){
	map_btn = $("#map_btn");
	itn_btn = $("#itn_btn");
	lst_btn = $("#lst_btn");
	map_div = $("#create_map");
	itn_div = $("#create_itn");
	lst_div = $("#create_lst");
	divs = [map_div, itn_div, lst_div];
	btns = [map_btn, itn_btn, lst_btn];

	$.each(divs, function( index, div ) {
		div.hide();
	});
	$.each(btns, function( index, btn ) {
		btn.addClass('btn-warning');
		btn.removeClass('btn-info');
	});

	if(view_name=='map'){
		map_btn.removeClass('btn-warning');
		map_btn.addClass('btn-info');
		map_div.show();
	} else if(view_name=='itinerary') {
		itn_btn.removeClass('btn-warning');
		itn_btn.addClass('btn-info');
		itn_div.show();
	} else if(view_name=='pack_list') {
		lst_btn.removeClass('btn-warning');
		lst_btn.addClass('btn-info');
		lst_div.show();
	}
}

$( document ).ready(function() {
	$("#map_btn").click(function(){
		toggle_view('map');
	});
	$("#itn_btn").click(function(){
		toggle_view('itinerary');
	});
	$("#lst_btn").click(function(){
		toggle_view('pack_list');
	});
	toggle_view('map');
});