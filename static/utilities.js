/**
 * Created by Andrew on 4/2/2016.
 */


$(function () {
    $('#btn-login').click(function () {
        $.ajax({
            url: '/linkToSpotify',
            type: 'POST',
            success: function (response) {
                alert(response)
            },
            error: function (response) {
                alert(response)
            }
        });
    });
});


