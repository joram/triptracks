(function() {
  window.PackingListEditor = (function() {
    function PackingListEditor() {
      $("#search").submit(function(event) {
        var csrf_token, search_text, search_url;
        event.preventDefault();
        search_text = $("#search_text").val();
        search_url = $('#search').data().searchUri;
        csrf_token = $('#search').data().csrf;
        console.log(search_text);
        console.log(search_url);
        return $.ajax({
          type: "POST",
          url: search_url,
          data: {
            search_text: search_text,
            csrfmiddlewaretoken: csrf_token
          },
          success: this.update_items,
          dataType: 'json'
        });
      });
    }

    PackingListEditor.prototype.update_items = function(data) {
      return console.log(data);
    };

    return PackingListEditor;

  })();

  $(document).ready(function() {
    return new window.PackingListEditor();
  });

}).call(this);
