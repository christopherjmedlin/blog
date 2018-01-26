var simplemde;

var newPost = (function () {

    function initSimpleMDE() {
        var config = { element: $(".md-editor")[0] };
        var simplemde = new SimpleMDE(config);
        return simplemde;
    };

    function post(content, title, topics) {
        data = { "title": title, "content": content };
        data['topics'] = topics.split(', ');
        
        if (typeof postID == 'undefined')
            utils.postObjectToAPI('posts', data, transitionToSuccess);
        else
            utils.postObjectToAPI('posts', data, transitionToSuccess, null, postID);

    };

    function validateForms(content) {
        var success = true;
        var topics = $(".topics").val().split(', ')
        var title = $("#title-input input").val()

        if (title.length > 100) {
            success = false;
            $(".err-title-too-long").show();
        }
        else {
            $(".err-title-too-long").hide();
        }
        
        if (topics.length > 15) {
            success = false;
            $(".err-too-many-topics").show();
        }
        else {
            $(".err-too-many-topics").hide();
        }

        if (content.length && title.length) {
            $(".err-missing-field").hide()
        }
        else {
            success = false;
            $(".err-missing-field").show()
        }

        return success
    };

    function transitionToSuccess() {
        $("#post-form").hide();
        $("#success").show();
    };

    return {
        initSimpleMDE,
        post,
        validateForms
    };

})();

$(document).ready(function() {
    $("#ajax-loader").hide();

    simplemde = newPost.initSimpleMDE();

    $(document).keyup(function () {
        newPost.validateForms(simplemde.value());
    });

    $(".post-button").click(function() {
        title = $("#title-input input").val();
        topics = $(".topics").val();
        if (newPost.validateForms(simplemde.value()))
            newPost.post(simplemde.value(), title, topics);
        else
            $("html, body").animate({ scrollTop: 0 }, "slow");
    });
    $(".cancel-button").click(function() {
        window.location.pathname = '/';
    });
});