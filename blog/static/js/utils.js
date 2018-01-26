var utils = (function() {
    function postObjectToAPI(resource, obj, success, error, id) {
        success = success || null;
        error = error || null;
        id = id || null;

        var url;
        if (typeof postID !== 'undefined') {
            url = "/api/v1/" + resource + "/edit/" + id;
        }
        else {
            url = "/api/v1/" + resource
        }

        $.ajax(url, {
            method: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(obj, null, '\t'),

            success: [success, function() {
                return true;
            }],
            error: [error, function() {
                return false;
            }]
        });
    };

    function getObjectFromAPI(resource, success, error, id) {
        success = success || null;
        error = error || null;
        id = id || "";

        $.ajax("/api/v1/" + resource + '/' + id, {
            method: 'GET',
            
            success: [success, function() {
                return true;
            }],
            error: [error, function() {
                return false;
            }]
        });
    }

    return {
        postObjectToAPI,
        getObjectFromAPI
    };
})();

$(document).ajaxError(function(event, xhr, ajaxOptions, thrownError) {
    alert("AJAX error: " + thrownError)
})