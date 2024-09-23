$("#client-bank-input").suggestions({
    token: token,
    type: "BANK",
    /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        var bankData = {
            name: suggestion.value,
            inn: suggestion.data.inn,
            kpp: suggestion.data.kpp,
            bic: suggestion.data.bic,
            address: suggestion.data.address.unrestricted_value,
            correspondent_account: suggestion.data.correspondent_account
        };
        $("#client-bank-info").val(JSON.stringify(bankData));
        $("#client-bank-display").text(suggestion.value);
        $("#client-bank-input").val(suggestion.value);
    }
});
