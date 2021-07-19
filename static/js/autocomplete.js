window.addEventListener('DOMContentLoaded', event => {
    $( "#searchMessagePrefix" ).keyup(function() {
        $.ajax({
            type: "GET",
            url: "/autocomplete/prefix/" + $(this).val(),
            success: function(data){
                console.log(data.has_data);
                if (data.has_data) {
                    $("#suggestBoxMatchPrefix").show();
                    $("#suggestBoxMatchPrefix").html(data.data);
                } else {
                    $("#suggestBoxMatchPrefix").html("");
                }
            },
            error: function(data) {
                $("#suggestBoxMatchPrefix").html("");
            }
        });
    });

    $( "#searchMessageNGram" ).keyup(function() {
        $.ajax({
            type: "GET",
            url: "/autocomplete/ngram/" + $(this).val(),
            success: function(data){
                if (data.has_data) {
                    $("#suggestBoxNgram").show();
                    $("#suggestBoxNgram").html(data.data);
                } else {
                    $("#suggestBoxNgram").html("");
                }
            },
            error: function(data) {
                $("#suggestBoxNgram").html("");
            }
        });
    });
});