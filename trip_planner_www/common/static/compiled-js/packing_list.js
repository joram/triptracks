(function() {
  window.PackingListEditor = (function() {
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

    PackingListEditor.prototype.update_items = function(data) {
      var all_html, html, i, item, len, ref;
      all_html = "<div class='row'>";
      ref = data.items;
      for (i = 0, len = ref.length; i < len; i++) {
        item = ref[i];
        html = '<div class="col-xs-3"> <a href="#" class="thumbnail"> <img src="' + item.img_href + '" class="img-responsive"> </a> </div>';
        all_html += html;
      }
      all_html += "</div>";
      console.log(all_html);
      return $("#possible_items").html(all_html);
    };

    return PackingListEditor;

  })();

  $(document).ready(function() {
    return new window.PackingListEditor();
  });

}).call(this);
