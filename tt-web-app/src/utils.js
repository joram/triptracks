function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        args[0].persist();
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function get_params(props){
    let params = props.location.search;
    params = params.replace("?", "");
    params = params.split("&");
    let args = {};
    params.forEach(s => {
      let parts = s.split("=", 2);
      args[parts[0]] = parts[1]
    });
    return args
}

export {
    debounce,
    get_params
}