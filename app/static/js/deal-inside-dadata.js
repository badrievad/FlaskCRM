$("#supplier-name-input").suggestions({
    token: suggestionsToken, type: "PARTY", /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        $("#supplier-name-input").val(suggestion.data.name.short_with_opf);
        $("#supplier-inn-input").val(suggestion.data.inn);
        console.log(suggestion)
    }
});

$("#supplier-inn-input").suggestions({
    token: suggestionsToken, type: "PARTY", /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        $("#supplier-inn-input").val(suggestion.data.inn);
        $("#supplier-name-input").val(suggestion.data.name.short_with_opf);
        console.log(suggestion)
    }
});