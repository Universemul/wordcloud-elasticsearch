window.addEventListener('DOMContentLoaded', event => {
    $( "#searchMessagePrefix" ).keyup(function() {
        console.log($(this).val());
        $.ajax({
            type: "GET",
            url: "/autocomplete/prefix/" + $(this).val(),
            success: function(data){
                console.log(data.has_data);
                if (data.has_data) {
                    $("#searchMessagePrefix").show();
                    $("#searchMessagePrefix").html(data.data);
                } else {
                    $("#searchMessagePrefix").html("");
                }
            }
        });
    });

    $( "#autocompleteNgramForm" ).keyup(function() {
        console.log($(this).val());
        $.ajax({
            type: "GET",
            url: "/autocomplete/ngram/" + $(this).val(),
            success: function(data){
                console.log(data.has_data);
                if (data.has_data) {
                    $("#suggestBoxNgram").show();
                    $("#suggestBoxNgram").html(data.data);
                } else {
                    $("#suggestBoxNgram").html("");
                }
            }
        });
    });
});