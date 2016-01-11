(function() {
  var bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  window.PackingListEditor = (function() {
    function PackingListEditor() {
      this.add_on_clicks = bind(this.add_on_clicks, this);
      this.add_item = bind(this.add_item, this);
      $("#search").submit((function(_this) {
        return function(event) {
          var csrf_token, search_text, search_url;
          event.preventDefault();
          search_text = $("#search_text").val();
          search_url = $('#search').data().searchUri;
          csrf_token = $('#search').data().csrf;
          return $.ajax({
            type: "POST",
            url: search_url,
            data: {
              quantity: 12,
              search_text: search_text,
              csrfmiddlewaretoken: csrf_token
            },
            success: _this.add_item,
            failure: _this.ajax_failure,
            dataType: 'json'
          });
        };
      })(this));
      this.add_on_clicks();
      $('#packing-list-name').editable({
        showbuttons: false,
        type: 'text',
        success: (function(_this) {
          return function(response, new_name) {
            return _this.update_list({
              name: new_name
            });
          };
        })(this)
      });
    }

    PackingListEditor.prototype.ajax_failure = function(data) {
      console.log("failed");
      return console.log(data);
    };

    PackingListEditor.prototype.update_list = function(data) {
      var list_id;
      console.log(data);
      list_id = 1;
      return $.ajax({
        type: "PUT",
        url: "/api/v1/packing_list/" + list_id + "/",
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json; charset=UTF-8"
      });
    };

    PackingListEditor.prototype.add_item = function(data) {
      console.log(data.html);
      $("#items").prepend(data.html);
      return this.add_on_clicks();
    };

    PackingListEditor.prototype.delete_item = function(item) {
      item = $(item);
      return $.ajax({
        type: "DELETE",
        url: item.data("editUri"),
        data: JSON.stringify({}),
        dataType: 'json',
        contentType: "application/json; charset=UTF-8",
        success: function() {
          return item.remove();
        }
      });
    };

    PackingListEditor.prototype.update_item = function(data) {
      var item;
      console.log(data.item);
      item = $(data.item);
      data.id = item.attr('id');
      data.name = data.name || item.find(".item-name").innerHTML;
      data.quantity = data.quantity || item.find(".item-quantity")[0].innerHTML;
      data.csrfmiddlewaretoken = item.data('csrf');
      data.item_type = "P";
      data.item = item.find('.item.active').data('itemId');
      console.log(data);
      return $.ajax({
        type: "PUT",
        url: item.data("editUri"),
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json; charset=UTF-8"
      });
    };

    PackingListEditor.prototype.add_on_clicks = function() {
      var control, fn, fn1, fn2, item_name, item_quantity, j, k, l, len, len1, len2, ref, ref1, ref2;
      ref = $(".change-item.carousel-control");
      fn = (function(_this) {
        return function(control) {
          return $(control).on("click", function(event) {
            return setTimeout(function() {
              var item, item_id;
              item_id = $(control).data('itemId');
              item = $("#" + item_id)[0];
              return _this.update_item({
                item: item
              });
            }, 1000);
          });
        };
      })(this);
      for (j = 0, len = ref.length; j < len; j++) {
        control = ref[j];
        fn(control);
      }
      $.fn.editable.defaults.mode = 'inline';
      ref1 = $('.change-item.item-name');
      fn1 = (function(_this) {
        return function(item_name) {
          return $(item_name).editable({
            showbuttons: false,
            type: 'text',
            success: function(response, new_name) {
              var item, item_id;
              item_id = $(item_name).data('itemId');
              item = $("#" + item_id)[0];
              return _this.update_item({
                item: item,
                name: new_name
              });
            }
          });
        };
      })(this);
      for (k = 0, len1 = ref1.length; k < len1; k++) {
        item_name = ref1[k];
        fn1(item_name);
      }
      ref2 = $('.change-item.item-quantity');
      fn2 = (function(_this) {
        return function(item_quantity) {
          return $(item_quantity).editable({
            showbuttons: false,
            type: 'select',
            source: function() {
              var i, m, values;
              values = [];
              for (i = m = 1; m <= 10; i = ++m) {
                values.push({
                  value: i,
                  text: "" + i
                });
              }
              return values;
            },
            success: function(response, new_quantity) {
              var item, item_id;
              item_id = $(item_quantity).data('itemId');
              item = $("#" + item_id)[0];
              return _this.update_item({
                item: item,
                quantity: new_quantity
              });
            }
          });
        };
      })(this);
      for (l = 0, len2 = ref2.length; l < len2; l++) {
        item_quantity = ref2[l];
        fn2(item_quantity);
      }
      return $('.packing-list-item .delete-item').on("click", (function(_this) {
        return function(event) {
          return _this.delete_item(event.toElement.closest('.packing-list-item'));
        };
      })(this));
    };

    return PackingListEditor;

  })();

  $(document).ready(function() {
    return new window.PackingListEditor();
  });

}).call(this);
