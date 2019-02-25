let config = {
    selectors: {
        add: '.basket-item-add',
        remove: '.basket-item-remove',
        delete: '.basket-item-delete',
        item: '.basket-item',
        item_none: '.basket-item-none',
        page_counters: '.basket-total-counters',
        info: '.basket-info'
    },
    counters: {
        quantity: '.basket-item-quantity',
        cost: '.basket-item-cost'
    },
    total_counters: {
        total_quantity: '.basket-item-total-quantity',
        total_cost: '.basket-item-total-cost'
    },
    urls: {
        add: '/basket/add/',
        remove: '/basket/remove/',
        delete: '/basket/delete/',
    }
};

$(document).ready(function () {

    $(config.selectors.add).on('click', function () {
        let item_id = $(this).data('id');
        let parent_item = $(".basket-item-" + item_id);
        let item_url = config.urls.add + item_id + '/';


        $.ajax({
            url: item_url,

            success: function (data) {
                if (data.quantity > 1) {
                    let remove_button = $(parent_item).find(config.selectors.remove);
                    $(remove_button).show()
                }
                $.each(config.counters, function (key, value) {
                    let counter = $(parent_item).find(value);
                    counter.text(data[key]);
                });
                $.each(config.total_counters, function (key, value) {
                    let total_counter = $("body").find(value);
                    total_counter.text(data[key]);
                });
            }
        });
    });

    $(config.selectors.remove).on('click', function () {
        let item_id = $(this).data('id');
        let parent_item = $(".basket-item-" + item_id);
        let item_url = config.urls.remove + item_id + '/';

        let remove_button = $(parent_item).find(config.selectors.remove);


        $.ajax({
            url: item_url,

            success: function (data) {
                if (data.quantity === 1) {
                    $(remove_button).hide()
                }
                $.each(config.counters, function (key, value) {
                    let counter = $(parent_item).find(value);
                    counter.text(data[key]);
                });
                $.each(config.total_counters, function (key, value) {
                    let total_counter = $("body").find(value);
                    total_counter.text(data[key]);
                });
            }
        });
    });

    $(config.selectors.delete).on('click', function () {
        let item_id = $(this).data('id');
        let parent_item = $(".basket-item-" + item_id);
        let item_url = config.urls.delete + item_id + '/';

        $.ajax({
            url: item_url,

            success: function (data) {
                $(parent_item).hide();
                if (data.total_quantity === 0) {
                    $(config.selectors.page_counters).hide();
                    $(config.selectors.info).hide();
                    $(config.selectors.item_none).show()
                } else {
                    $.each(config.total_counters, function (key, value) {
                        let total_counter = $("body").find(value);
                        total_counter.text(data[key]);
                    });
                }
            }
        });
    })
});