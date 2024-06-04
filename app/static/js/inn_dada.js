$("#deal-title").suggestions({
    token: suggestionsToken, type: "PARTY", /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        $("#deal-title").val(suggestion.value);
    }
});
