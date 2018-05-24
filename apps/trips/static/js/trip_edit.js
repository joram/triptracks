
b1 = "#route-button";
b2 = "#packing-button";
b3 = "#time-button";
b4 = "#team-button";

v1 = "#route-view";
v2 = "#packing-view";
v3 = "#time-view";
v4 = "#team-view";

button_ids = [b1, b2, b3, b4];
view_ids = [v1, v2, v3, v4];
views = {
    "#route-button": v1,
    "#packing-button": v2,
    "#time-button": v3,
    "#team-button": v4
};


function toggle_view(button_id) {
    view_ids.forEach(function (view_id){
        $(view_id).hide();
    });
    $(views[button_id]).show();
}

$( document ).ready(function() {
    button_ids.forEach(function (id) {
        (function (button_id) {
            $(button_id).click(function () {
                toggle_view(button_id)
            });
        })(id);
    });
});
