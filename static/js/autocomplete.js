function generateAjaxRequest(autocomplete_value, autocomplete_type, suggestBoxName) {
    $.ajax({
        type: "GET",
        url: "/autocomplete/" + autocomplete_type + "/" + autocomplete_value,
        success: function(data){
            if (data.has_data) {
                $(suggestBoxName).show();
                $(suggestBoxName).html(data.data);
            } else {
                $(suggestBoxName).html("");
            }
        },
        error: function(data) {
            $(suggestBoxName).html("");
        }
    });
}

function increaseWeight(cityId) {
    $.ajax({
        type: "POST",
        url: "/cities/" + cityId.replace("city-", "") + "/increase_weight",
        data: {},
        success: function(data){
            console.log("OK");
        },
        error: function(data) {
            console.log("NOT OK");
        }
    });
}

window.addEventListener('DOMContentLoaded', event => {
    $("#searchMessagePrefix").keyup(function() {
        generateAjaxRequest($(this).val(), "prefix", "#suggestBoxMatchPrefix");
    });

    $("#searchMessageNGram").keyup(function() {
        generateAjaxRequest($(this).val(), "ngram", "#suggestBoxNgram");
    });

    $("#searchMessageMatch").keyup(function() {
        generateAjaxRequest($(this).val(), "match", "#suggestBoxMatch");
    });

    $("#searchMessageSuggest").keyup(function() {
        generateAjaxRequest($(this).val(), "suggest", "#suggestBoxSuggest");
    });

    $("#suggest-item").on("click", function(){
        alert("CLICKED");
    });
});