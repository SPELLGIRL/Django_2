$(document).on('click', '.products-block a', function (event) {
    if (event.target.hasAttribute('href') || event.target.offsetParent.hasAttribute('href')) {
        let link = event.target.href + 'ajax/';
        if (event.target.offsetParent.hasAttribute('href')) {
            link = event.target.offsetParent.href + 'ajax/';
        }
        let link_array = link.split('/');
        console.log(link_array[3], link_array[4]);
        if (link_array[4] != 'details') {
            if (link_array[3] == 'products') {
                $.ajax({
                    url: link,
                    success: function (data) {
                        $('.products-block').html(data.result);
                    },
                });
                event.preventDefault();
            }
        }
    }
});
