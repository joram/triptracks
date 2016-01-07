(function() {
  window.PackingListEditor = (function() {
    var uuid;

    function PackingListEditor() {
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
            success: _this.update_items,
            failure: _this.ajax_failure,
            dataType: 'json'
          });
        };
      })(this));
    }

    PackingListEditor.prototype.ajax_failure = function() {
      return console.log("failed");
    };

    uuid = function() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r, v;
        r = Math.random() * 16 | 0;
        v = c === 'x' ? r : r & 0x3 | 0x8;
        return v.toString(16);
      });
    };

    PackingListEditor.prototype.update_items = function(data) {
      var div_class, first, i, id, img, item, item_carousel, item_html, left_html, len, ref, right_html, slide;
      id = uuid();
      item_carousel = $('<div />', {
        "id": id,
        "class": "packing-list-item carousel slide col-md-2",
        "data-ride": "carousel"
      });
      $("#items").prepend(item_carousel);
      item_html = $('<div />', {
        "class": 'carousel-inner',
        "role": "listbox"
      });
      item_carousel.prepend(item_html);
      first = true;
      ref = data.items;
      for (i = 0, len = ref.length; i < len; i++) {
        item = ref[i];
        div_class = "item";
        if (first) {
          div_class += " active";
          first = false;
        }
        slide = $('<div />', {
          "class": div_class
        });
        slide.appendTo(item_html);
        img = $('<img />', {
          "src": item.img_href
        });
        img.appendTo(slide);
      }
      left_html = $('<a class="left carousel-control" href="#' + id + '" role="button" data-slide="prev"> <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> <span class="sr-only">Previous</span> </a>');
      item_carousel.append(left_html);
      right_html = $('<a class="right carousel-control" href="#' + id + '" role="button" data-slide="next"> <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> <span class="sr-only">Next</span> </a>');
      item_carousel.append(right_html);
      return item_carousel.carousel({
        interval: 0
      });
    };

    return PackingListEditor;

  })();

  $(document).ready(function() {
    return new window.PackingListEditor();
  });

}).call(this);
