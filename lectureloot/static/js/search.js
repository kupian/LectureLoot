$(document).ready(function() {
    $("#search").submit(function(event) {
        event.preventDefault();

        var query = $("#query").val().trim();

        if (query) {
            var encodedQuery = encodeURIComponent(query);
            window.location.href = `/search/${encodedQuery}/`;
        }
    });
});