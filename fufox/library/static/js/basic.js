// This is in order to update the dropdown with the correct name of the filter applied
$(".dropdown-menu a").click(function () {

    $(".filter-dropdown:first").html($(this).text() + ' <span class="substitute"></span>');

});


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$('#filter-action').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Action")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});
$('#filter-adventure').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Adventure")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});

$('#filter-comedy').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Comedy")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});

$('#filter-drama').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Drama")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});

$('#filter-crime').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Crime")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});

$('#filter-scifi').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().genres.includes("Sci-Fi")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});


$('#filter-none').click(function () {
    featureList.filter();
    return false;
});

featureList.on('updated', function (list) {
    if (list.matchingItems.length > 0) {
        $('.no-result').hide()
    } else {
        $('.no-result').show()
    }
});


$('#filter-actors').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().capacity.includes("Actor")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});


$('#filter-directors').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().capacity.includes("Director")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});


$('#filter-writers').click(function () {
    featureList.filter(function (item) {
        // console.log(item.values().genres)
        if (item.values().capacity.includes("Writer")) {
            return true;
        } else {
            return false;
        }
    });
    return false;
});
