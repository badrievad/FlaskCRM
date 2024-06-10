$("#deal-title").suggestions({
    token: suggestionsToken, type: "PARTY", /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        $("#deal-title").val(suggestion.data.name.short_with_opf);
        $("#deal-info").val(JSON.stringify(suggestion));
        console.log(suggestion)
    }
});
