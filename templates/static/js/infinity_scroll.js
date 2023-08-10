$(document).ready(function () {
    var isLoading = false;
    var page = 2;
    var pagination = $('#pagination').html();

    function loadMoreItems() {
        if (isLoading) return;
        isLoading = true;

        $.ajax({
            url: '/home/load-movie',
            type: 'GET',
            data: { page: page },
            success: function (data) {
                if (data.len_items > 0) {
                    $('#content').append(data.html);
                    page++;
                    isLoading = false;
                } else {
                    $(window).off('scroll', onScroll);
                }
            }
        });
    }

    function onScroll() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            loadMoreItems();
        }
    }

    $(window).on('scroll', onScroll);
    loadMoreItems();
});