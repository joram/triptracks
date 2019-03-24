let EventEmitter = require('events').EventEmitter;

let emitter = new EventEmitter();
emitter.setMaxListeners(1000);


module.exports = {
  zoomChanged: function(zoom){
    emitter.emit("zoom_change", {zoom:zoom});
  },
  subscribeZoomChange: function(callback){
    emitter.addListener("zoom_change", callback);
  }

};