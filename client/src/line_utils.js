module.exports = {

  string_to_bbox: function (s) {
    try{
      let b = JSON.parse(s);
      let lat_1 = parseFloat(b[0][0]);
      let lng_1 = parseFloat(b[0][1]);
      let lat_2 = parseFloat(b[1][0]);
      let lng_2 = parseFloat(b[1][1]);
      let bounds = new google.maps.LatLngBounds();
      bounds.extend({lat: lat_1, lng: lng_1});
      bounds.extend({lat: lat_2, lng: lng_2});
      return bounds
    }
    catch (e) {
      console.log(s);
      console.log(e)
    }
  },

};