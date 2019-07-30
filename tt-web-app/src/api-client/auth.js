let sessionToken = null;


export default {

    isAuthed: function(){
        return sessionToken != null
    },

    setSessionToken: function(token){
        sessionToken = token
    },

    getRequestHeaders: function() {
        let headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        };
        if (sessionToken !== null) {
            headers["x-session-token"] = sessionToken
        }
        return headers
    }

};