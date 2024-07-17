$(document).ready(function() {
    $("#item-name").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "./calculator/autocomplete",
                data: {
                    query: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        }
    });
});
