function formatNumber(value) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

function parseFormattedNumber(value) {
    return parseFloat(value.replace(/\s/g, '').replace(',', '.').replace('-', ''));
}

document.getElementById('cost').addEventListener('input', function () {
    var value = parseFloat(this.value);
    document.getElementById('cost-value').value = value;
    document.getElementById('cost-display').value = formatNumber(value);
    updateInitialPaymentValue();
    updateCreditValue(); // Обновляем значение кредита
});

document.getElementById('cost-display').addEventListener('input', function () {
    var inputValue = this.value.trim().toLowerCase();

    if (inputValue === '' || inputValue === 'не число') {
        this.value = '0';
        var value = 0;
    } else {
        var value = parseFormattedNumber(this.value);
        if (isNaN(value)) {
            value = 0;
        }
    }

    document.getElementById('cost-value').value = value;
    document.getElementById('cost').value = value;

    updateInitialPaymentValue();
    updateCreditValue(); // Обновляем значение кредита
});

document.getElementById('cost-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    updateCreditValue(); // Обновляем значение кредита
});

document.getElementById('initial-payment').addEventListener('input', function () {
    var percentValue = parseFloat(this.value);
    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var initialPaymentValue = (percentValue / 100) * totalCost;

    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
    document.getElementById('initial-payment-value-display').value = formatNumber(initialPaymentValue);
    updateCreditValue(); // Добавлен вызов для обновления значения кредита
});

document.getElementById('initial-payment-value-display').addEventListener('input', function () {
    var inputValue = this.value.trim().toLowerCase();

    if (inputValue === '' || inputValue === 'не число') {
        this.value = '0';
        var initialPaymentValue = 0;
    } else {
        var initialPaymentValue = parseFormattedNumber(this.value);
        if (isNaN(initialPaymentValue)) {
            initialPaymentValue = 0;
        }
    }

    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var maxInitialPaymentValue = totalCost * 0.4999;
    if (initialPaymentValue > maxInitialPaymentValue) {
        initialPaymentValue = maxInitialPaymentValue;
    }
    var percentValue = (initialPaymentValue / totalCost) * 100;

    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
    document.getElementById('initial-payment').value = percentValue;
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
    updateCreditValue(); // Добавлен вызов для обновления значения кредита
});


document.getElementById('initial-payment-value-display').addEventListener('blur', function () {
    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var initialPaymentValue = parseFormattedNumber(this.value);
    var maxInitialPaymentValue = totalCost * 0.4999;
    if (initialPaymentValue > maxInitialPaymentValue) {
        initialPaymentValue = maxInitialPaymentValue;
    }
    this.value = formatNumber(initialPaymentValue);
    updateCreditValue(); // Добавлен вызов для обновления значения кредита
});

document.getElementById('initial-payment-percent').addEventListener('blur', function () {
    var inputValue = this.value.trim().toLowerCase();

    if (inputValue === '' || inputValue === 'не число') {
        this.value = '0';
        var percentValue = 0;
    } else {
        var percentValue = parseFloat(this.value);
        if (isNaN(percentValue)) {
            percentValue = 0;
        }
    }

    var totalCost = parseFloat(document.getElementById('cost-value').value);

    if (percentValue > 49.99) {
        percentValue = 49.99;
    }

    var initialPaymentValue = (percentValue / 100) * totalCost;

    document.getElementById('initial-payment').value = percentValue;
    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);  // Установите значение обратно в поле
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
    document.getElementById('initial-payment-value-display').value = formatNumber(initialPaymentValue);
    updateCreditValue(); // Добавлен вызов для обновления значения кредита
});


document.getElementById('initial-payment-percent').addEventListener('keypress', function (event) {
    // Разрешить только цифры и блокировать -, +
    if (event.key === '-' || event.key === '+' || event.key === 'e') {
        event.preventDefault();
    }
});

document.getElementById('term').addEventListener('input', function () {
    document.getElementById('term-value').value = this.value;
});

document.getElementById('term-value').addEventListener('input', function () {
    if (this.value > 100) {
        this.value = 100;
    }
    document.getElementById('term').value = this.value;
});

document.getElementById('term-value').addEventListener('keypress', function (event) {
    if (event.key === '-' || event.key === '+') {
        event.preventDefault();
    }
});


document.querySelectorAll('.tabs button').forEach(button => {
    button.addEventListener('click', function () {
        document.querySelectorAll('.tabs button').forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
    });
});

function updateInitialPaymentValue() {
    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var percentValue = parseFloat(document.getElementById('initial-payment-percent').value);
    var value = (percentValue / 100) * totalCost;

    document.getElementById('initial-payment').value = percentValue;
    document.getElementById('initial-payment-value').value = value.toFixed(0);
    document.getElementById('initial-payment-value-display').value = formatNumber(value);
}

// Обработчик для блокировки нечисловых символов
function allowOnlyNumbers(event) {
    var charCode = event.charCode || event.keyCode;
    if (
        (charCode >= 48 && charCode <= 57) || // Цифры
        charCode === 44 || // Запятая
        charCode === 46 || // Точка
        charCode === 8 || // Backspace
        charCode === 37 || // Левая стрелка
        charCode === 39 || // Правая стрелка
        charCode === 46 || // Delete
        charCode === 9 // Tab
    ) {
        return true;
    }
    event.preventDefault();
    return false;
}

document.getElementById('cost-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('initial-payment-value-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('credit-value-display').addEventListener('keypress', allowOnlyNumbers);

document.getElementById('foreign-cost').addEventListener('input', function () {
    var value = parseFloat(this.value);
    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost-display').value = formatNumber(value);
});

document.getElementById('foreign-cost-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);

    if (isNaN(value)) {
        value = 0;
    }

    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost').value = value;
});

document.getElementById('foreign-cost-display').addEventListener('blur', function () {
    var value = parseFormattedNumber(this.value);
    if (isNaN(value)) {
        value = 0;
    }
    this.value = formatNumber(value);
});

document.getElementById('foreign-cost-display').addEventListener('keypress', allowOnlyNumbers);

function getExchangeRate(currency) {
    const exchangeRates = {
        usd: parseFloat(document.getElementById('today-usd').textContent.replace(/[^\d,.-]/g, '').replace(',', '.')),
        eur: parseFloat(document.getElementById('today-eur').textContent.replace(/[^\d,.-]/g, '').replace(',', '.')),
        cny: parseFloat(document.getElementById('today-cny').textContent.replace(/[^\d,.-]/g, '').replace(',', '.'))
    };
    return exchangeRates[currency.toLowerCase()];
}

function convertToRubles(value, rate) {
    return value * rate;
}

function updateCostInRubles() {
    const currency = document.getElementById('currency').value;
    if (currency === 'rub') {
        return;
    }

    const foreignCost = parseFormattedNumber(document.getElementById('foreign-cost-display').value);
    const rate = getExchangeRate(currency);
    const rubleCost = convertToRubles(foreignCost, rate);

    document.getElementById('cost-value').value = rubleCost;
    document.getElementById('cost-display').value = formatNumber(rubleCost);
    document.getElementById('cost').value = rubleCost;
    updateInitialPaymentValue();
    updateCreditValue(); // Обновляем значение кредита
}

document.getElementById('foreign-cost-display').addEventListener('input', function () {
    updateCostInRubles();
});

document.getElementById('foreign-cost-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    updateCostInRubles();
});

document.getElementById('currency').addEventListener('change', function () {
    updateCostInRubles();
});

// Обработчик для слайдера foreign-cost
document.getElementById('foreign-cost').addEventListener('input', function () {
    var value = parseFloat(this.value);
    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost-display').value = formatNumber(value);
    updateCostInRubles();  // Обновляем стоимость в рублях при изменении слайдера
});

function updateCreditValue() {
    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var creditPercent = parseFloat(document.getElementById('credit-percent').value);
    var initialPaymentPercent = parseFloat(document.getElementById('initial-payment-percent').value);
    var maxCreditPercent = 100 - initialPaymentPercent;

    if (creditPercent > maxCreditPercent) {
        creditPercent = maxCreditPercent;
    }

    var creditValue = (creditPercent / 100) * totalCost;

    document.getElementById('credit-value').value = creditValue.toFixed(0);
    document.getElementById('credit-value-display').value = formatNumber(creditValue);
    document.getElementById('credit').value = creditPercent;
    document.getElementById('credit-percent').value = creditPercent.toFixed(2);  // Обновление поля процента кредита
}


// Обработчики для кредитного значения и процента
document.getElementById('credit-percent').addEventListener('blur', function () {
    var inputValue = this.value.trim().toLowerCase();

    if (inputValue === '' || inputValue === 'не число') {
        this.value = '0';
    }

    updateCreditValue();
});

document.getElementById('credit').addEventListener('input', function () {
    document.getElementById('credit-percent').value = this.value;
    updateCreditValue();
});

document.getElementById('credit-value-display').addEventListener('blur', function () {
    var inputValue = this.value.trim().toLowerCase();

    if (inputValue === '' || inputValue === 'не число') {
        this.value = '0';
        var creditValue = 0;
    } else {
        var creditValue = parseFormattedNumber(this.value);
        if (isNaN(creditValue)) {
            creditValue = 0;
        }
    }

    var totalCost = parseFloat(document.getElementById('cost-value').value);
    var initialPaymentPercent = parseFloat(document.getElementById('initial-payment-percent').value);
    var maxCreditPercent = 100 - initialPaymentPercent;
    var maxCreditValue = totalCost * (maxCreditPercent / 100);

    if (creditValue > maxCreditValue) {
        creditValue = maxCreditValue;
    }

    var creditPercent = (creditValue / totalCost) * 100;

    document.getElementById('credit-value').value = creditValue.toFixed(0);
    document.getElementById('credit-value-display').value = formatNumber(creditValue);
    document.getElementById('credit-percent').value = creditPercent.toFixed(2);
    document.getElementById('credit').value = creditPercent;
});


document.getElementById('commission').addEventListener('input', function () {
    document.getElementById('commission-value').value = this.value;
});

document.getElementById('commission-value').addEventListener('blur', function () {
    if (this.value > 3) {
        this.value = 3;
    }

    document.getElementById('commission').value = this.value;
    if (this.value.trim() === "") {
        this.value = "0";
        document.getElementById('commission').value = 0;
    }
});

document.getElementById('commission-value').addEventListener('keypress', function (event) {
    if (event.key === '-' || event.key === '+' || (event.key < '0' || event.key > '9') && event.key !== '.') {
        event.preventDefault();
    }
});

document.getElementById('commission-lkmb').addEventListener('input', function () {
    document.getElementById('commission-lkmb-value').value = this.value;
});

document.getElementById('commission-lkmb-value').addEventListener('blur', function () {
    if (this.value > 3) {
        this.value = 3;
    }

    document.getElementById('commission-lkmb').value = this.value;
    if (this.value.trim() === "") {
        this.value = "0";
        document.getElementById('commission-lkmb').value = 0;
    }
});

document.getElementById('commission-lkmb-value').addEventListener('keypress', function (event) {
    if (event.key === '-' || event.key === '+' || (event.key < '0' || event.key > '9') && event.key !== '.') {
        event.preventDefault();
    }
});

// Агентское вознаграждение
document.getElementById('agent-commission').addEventListener('input', function () {
    document.getElementById('agent-commission-value').value = this.value;
});

document.getElementById('agent-commission-value').addEventListener('blur', function () {
    var value = this.value;

    // Ограничение на длину значения (например, 5 символов)
    if (value.length > 5) {
        value = value.slice(0, 5);
    }

    // Преобразование в число и проверка на превышение 20
    var numericValue = parseFloat(value);

    if (numericValue > 20) {
        numericValue = 20;
    }

    this.value = numericValue; // Обновить значение поля, если оно было изменено
    document.getElementById('agent-commission').value = numericValue;
    if (this.value.trim() === "") {
        this.value = "0";
        document.getElementById('agent-commission').value = 0;
    }
});

document.getElementById('agent-commission-value').addEventListener('keypress', function () {
    // Разрешить только цифры и блокировать -, +
    if (event.key === '-' || event.key === '+' || event.key === 'e') {
        event.preventDefault();
    }
});

// Бонус менеджера
document.getElementById('manager-bonus').addEventListener('input', function () {
    document.getElementById('manager-bonus-value').value = this.value;
});

document.getElementById('manager-bonus-value').addEventListener('blur', function () {
    var value = this.value;

    // Ограничение на длину значения (например, 5 символов)
    if (value.length > 5) {
        value = value.slice(0, 5);
    }

    // Преобразование в число и проверка на превышение 20
    var numericValue = parseFloat(value);

    if (numericValue > 20) {
        numericValue = 20;
    }

    this.value = numericValue; // Обновить значение поля, если оно было изменено
    document.getElementById('manager-bonus').value = numericValue;
    if (this.value.trim() === "") {
        this.value = "0";
        document.getElementById('manager-bonus').value = 0;
    }
});


// Трекеры
document.getElementById('tracker').addEventListener('input', function () {
    document.getElementById('tracker-value').value = this.value;
    document.getElementById('tracker-display').value = this.value;
});

document.getElementById('tracker-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('tracker-value').value = value;
    document.getElementById('tracker').value = value;
});

// Маячки
document.getElementById('mayak').addEventListener('input', function () {
    document.getElementById('mayak-value').value = this.value;
    document.getElementById('mayak-display').value = this.value;
});

document.getElementById('mayak-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('mayak-value').value = value;
    document.getElementById('mayak').value = value;
});

// Федресурс
document.getElementById('fedresurs').addEventListener('input', function () {
    document.getElementById('fedresurs-value').value = this.value;
    document.getElementById('fedresurs-display').value = this.value;
});

document.getElementById('fedresurs-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('fedresurs-value').value = value;
    document.getElementById('fedresurs').value = value;
});

// ГСМ
document.getElementById('gsm').addEventListener('input', function () {
    document.getElementById('gsm-value').value = this.value;
    document.getElementById('gsm-display').value = this.value;
});

document.getElementById('gsm-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('gsm-value').value = value;
    document.getElementById('gsm').value = value;
});

// Почтовые расходы
document.getElementById('mail').addEventListener('input', function () {
    document.getElementById('mail-value').value = this.value;
    document.getElementById('mail-display').value = this.value;
});

document.getElementById('mail-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('mail-value').value = value;
    document.getElementById('mail').value = value;
});

document.getElementById('depr-transport').addEventListener('input', function () {
    document.getElementById('depr-transport-value').value = this.value;
    document.getElementById('depr-transport-display').value = this.value;
})

document.getElementById('depr-transport-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('depr-transport-value').value = value;
    document.getElementById('depr-transport').value = value;
})

document.getElementById('travel').addEventListener('input', function () {
    document.getElementById('travel-value').value = this.value;
    document.getElementById('travel-display').value = this.value;
})

document.getElementById('travel-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('travel-value').value = value;
    document.getElementById('travel').value = value;
})

document.getElementById('stationery').addEventListener('input', function () {
    document.getElementById('stationery-value').value = this.value;
    document.getElementById('stationery-display').value = this.value;
})

document.getElementById('stationery-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('stationery-value').value = value;
    document.getElementById('stationery').value = value;
})

document.getElementById('internet').addEventListener('input', function () {
    document.getElementById('internet-value').value = this.value;
    document.getElementById('internet-display').value = this.value;
})

document.getElementById('internet-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('internet-value').value = value;
    document.getElementById('internet').value = value;
})

document.getElementById('pledge').addEventListener('input', function () {
    document.getElementById('pledge-value').value = this.value;
    document.getElementById('pledge-display').value = this.value;
})

document.getElementById('pledge-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('pledge-value').value = value;
    document.getElementById('pledge').value = value;
})

document.getElementById('bank-pledge').addEventListener('input', function () {
    document.getElementById('bank-pledge-value').value = this.value;
    document.getElementById('bank-pledge-display').value = this.value;
})

document.getElementById('bank-pledge-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('bank-pledge-value').value = value;
    document.getElementById('bank-pledge').value = value;
})

document.getElementById('express').addEventListener('input', function () {
    document.getElementById('express-value').value = this.value;
    document.getElementById('express-display').value = this.value;
})

document.getElementById('express-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('express-value').value = value;
    document.getElementById('express').value = value;
})

document.getElementById('egrn').addEventListener('input', function () {
    document.getElementById('egrn-value').value = this.value;
    document.getElementById('egrn-display').value = this.value;
})

document.getElementById('egrn-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('egrn-value').value = value;
    document.getElementById('egrn').value = value;
})

document.getElementById('egrul').addEventListener('input', function () {
    document.getElementById('egrul-value').value = this.value;
    document.getElementById('egrul-display').value = this.value;
})
document.getElementById('egrul-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('egrul-value').value = value;
    document.getElementById('egrul').value = value;
})

document.getElementById('tracker-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('mayak-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('fedresurs-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('gsm-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('mail-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('depr-transport-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('travel-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('stationery-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('internet-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('pledge-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('bank-pledge-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('express-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('egrn-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('egrul-display').addEventListener('keypress', allowOnlyNumbers);


document.getElementById('tracker-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('tracker').value = 0;
    }
});

// Обработчик для слайдера tracker
document.getElementById('tracker').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('tracker-display').value = formatNumber(value);
});

document.getElementById('mayak-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('mayak').value = 0;
    }
});

// Обработчик для слайдера mayak
document.getElementById('mayak').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('mayak-display').value = formatNumber(value);
});


document.getElementById('fedresurs-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('fedresurs').value = 0;
    }
});

// Обработчик для слайдера fedresurs
document.getElementById('fedresurs').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('fedresurs-display').value = formatNumber(value);
});

// Форматирование для gsm-display
document.getElementById('gsm-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('gsm').value = 0;
    }
});

// Обработчик для слайдера gsm
document.getElementById('gsm').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('gsm-display').value = formatNumber(value);
});

// Форматирование для mail-display
document.getElementById('mail-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('mail').value = 0;
    }
});

// Обработчик для слайдера mail
document.getElementById('mail').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('mail-display').value = formatNumber(value);
});

// Форматирование для depr-transport-display
document.getElementById('depr-transport-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('depr-transport').value = 0;
    }
});

// Обработчик для слайдера depr-transport
document.getElementById('depr-transport').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('depr-transport-display').value = formatNumber(value);
});

// Форматирование для travel-display
document.getElementById('travel-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('travel').value = 0;
    }
});

// Обработчик для слайдера travel
document.getElementById('travel').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('travel-display').value = formatNumber(value);
});

// Форматирование для stationery-display
document.getElementById('stationery-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('stationery').value = 0;
    }
});

// Обработчик для слайдера stationery
document.getElementById('stationery').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('stationery-display').value = formatNumber(value);
});

// Форматирование для internet-display
document.getElementById('internet-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('internet').value = 0;
    }
});

// Обработчик для слайдера internet
document.getElementById('internet').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('internet-display').value = formatNumber(value);
});

// Форматирование для pledge-display
document.getElementById('pledge-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('pledge').value = 0;
    }
});

// Обработчик для слайдера pledge
document.getElementById('pledge').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('pledge-display').value = formatNumber(value);
});

// Форматирование для bank-pledge-display
document.getElementById('bank-pledge-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('bank-pledge').value = 0;
    }
});

// Обработчик для слайдера bank-pledge
document.getElementById('bank-pledge').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('bank-pledge-display').value = formatNumber(value);
});

// Форматирование для express-display
document.getElementById('express-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('express').value = 0;
    }
});

// Обработчик для слайдера express
document.getElementById('express').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('express-display').value = formatNumber(value);
});

// Форматирование для egrn-display
document.getElementById('egrn-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('egrn').value = 0;
    }
});

// Обработчик для слайдера egrn
document.getElementById('egrn').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('egrn-display').value = formatNumber(value);
});

// Форматирование для egrul-display
document.getElementById('egrul-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
    if (this.value.trim() === "не число") {
        this.value = "0,00";
        document.getElementById('egrul').value = 0;
    }
});

// Обработчик для слайдера egrul
document.getElementById('egrul').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('egrul-display').value = formatNumber(value);
});


// Применяем обработчик событий 'blur' ко всем элементам с id 'health-insurance1' до 'health-insurance5'
document.querySelectorAll('[id^="health-insurance"]').forEach(function (element) {
    element.addEventListener('blur', function () {
        this.value = formatNumber(parseFormattedNumber(this.value));
        console.log(this.value)
        if (this.value.trim() === "не число") {
            this.value = "0,00";
        }
    });
});

document.querySelectorAll('[id^="other-insurance"]').forEach(function (element) {
    element.addEventListener('blur', function () {
        this.value = formatNumber(parseFormattedNumber(this.value));
        if (this.value.trim() === "не число") {
            this.value = "0,00";
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const newBtn = document.getElementById('new-btn');
    const usedBtn = document.getElementById('used-btn');
    const itemCondition = document.getElementById('item-condition');

    function setActiveButton(activeBtn, inactiveBtn) {
        activeBtn.classList.add('active');
        inactiveBtn.classList.remove('active');
        itemCondition.value = activeBtn.getAttribute('data-value');
    }

    newBtn.addEventListener('click', function () {
        setActiveButton(newBtn, usedBtn);
    });

    usedBtn.addEventListener('click', function () {
        setActiveButton(usedBtn, newBtn);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const yearInput = document.getElementById('production-year-value');
    const currentYear = new Date().getFullYear();
    const maxYear = currentYear + 1;

    yearInput.value = currentYear;

    yearInput.addEventListener('blur', function () {
        let value = this.value.replace(/[^0-9]/g, '').slice(0, 4); // Удаляем все символы, кроме цифр, и ограничиваем до 4 символов
        this.value = value;

        if (value && parseInt(value) < 1950) {
            this.value = 1950;
        } else if (value && parseInt(value) > maxYear) {
            this.value = maxYear;
        }
        // });

        yearInput.addEventListener('blur', function () {
            if (parseInt(this.value) < 1950) {
                this.value = 1950;
            } else if (parseInt(this.value) > maxYear) {
                this.value = maxYear;
            }
        });

        yearInput.addEventListener('keypress', function (e) {
            const charCode = e.charCode || e.keyCode;
            if (charCode === 43 || charCode === 45 || charCode === 101) {
                e.preventDefault();
            }
        });
    });

    function populateForm(data) {
        var calc = data.data.calc;
        var tranches = data.data.tranches;
        var insurances = data.data.insurances;

        console.log(data);

        if (calc.currency !== 'rub') {
            document.getElementById('foreign-cost-section').classList.add('show');
            // Обновление лейблов валюты
        } else {
            document.getElementById('foreign-cost-section').classList.remove('show');
        }

        // Заполните основные поля
        document.getElementById('item-name').value = calc.item_name;
        document.getElementById('production-year-value').value = calc.item_year;
        document.getElementById('cost-value').value = calc.item_price;
        document.getElementById('cost-display').value = calc.item_price_str;
        document.getElementById('cost').value = calc.item_price;
        document.getElementById('foreign-cost-value').value = calc.foreign_price;
        document.getElementById('foreign-cost-display').value = calc.foreign_price_str;
        document.getElementById('foreign-cost').value = calc.foreign_price;
        document.getElementById('initial-payment').value = calc.initial_payment_percent;
        document.getElementById('initial-payment-percent').value = calc.initial_payment_percent.toFixed(2);
        document.getElementById('credit').value = calc.credit_sum_percent;
        document.getElementById('credit-percent').value = calc.credit_sum_percent;
        updateInitialPaymentValue();
        updateCreditValue();
        document.getElementById('term-value').value = calc.agreement_term;
        document.getElementById('term').value = calc.agreement_term;
        document.getElementById('commission-value').value = calc.bank_commission;
        document.getElementById('commission').value = calc.bank_commission;
        document.getElementById('commission-lkmb-value').value = calc.lkmb_commission;
        document.getElementById('commission-lkmb').value = calc.lkmb_commission;
        document.getElementById('agent-commission-value').value = calc.agent_commission;
        document.getElementById('agent-commission').value = calc.agent_commission;
        document.getElementById('manager-bonus-value').value = calc.manager_bonus;
        document.getElementById('manager-bonus').value = calc.manager_bonus;
        document.getElementById('tracker-value').value = calc.tracker;
        document.getElementById('tracker-display').value = calc.tracker_str;
        document.getElementById('tracker').value = calc.tracker;
        document.getElementById('mayak-value').value = calc.mayak;
        document.getElementById('mayak-display').value = calc.mayak_str;
        document.getElementById('mayak').value = calc.mayak;
        document.getElementById('fedresurs-value').value = calc.fedresurs;
        document.getElementById('fedresurs-display').value = calc.fedresurs_str;
        document.getElementById('fedresurs').value = calc.fedresurs;
        document.getElementById('gsm-value').value = calc.gsm;
        document.getElementById('gsm-display').value = calc.gsm_str;
        document.getElementById('gsm').value = calc.gsm;
        document.getElementById('mail-value').value = calc.mail;
        document.getElementById('mail-display').value = calc.mail_str;
        document.getElementById('mail').value = calc.mail;
        document.getElementById('depr-transport-value').value = calc.depr_transport;
        document.getElementById('depr-transport-display').value = calc.depr_transport_str;
        document.getElementById('depr-transport').value = calc.depr_transport;
        document.getElementById('travel-value').value = calc.travel;
        document.getElementById('travel-display').value = calc.travel_str;
        document.getElementById('travel').value = calc.travel;
        document.getElementById('stationery-value').value = calc.stationery;
        document.getElementById('stationery-display').value = calc.stationery_str;
        document.getElementById('stationery').value = calc.stationery;
        document.getElementById('internet-value').value = calc.internet;
        document.getElementById('internet-display').value = calc.internet_str;
        document.getElementById('internet').value = calc.internet;
        document.getElementById('pledge-value').value = calc.pledge;
        document.getElementById('pledge-display').value = calc.pledge_str;
        document.getElementById('pledge').value = calc.pledge;
        document.getElementById('bank-pledge-value').value = calc.bank_pledge;
        document.getElementById('bank-pledge-display').value = calc.bank_pledge_str;
        document.getElementById('bank-pledge').value = calc.bank_pledge;
        document.getElementById('express-value').value = calc.express;
        document.getElementById('express-display').value = calc.express_str;
        document.getElementById('express').value = calc.express;
        document.getElementById('egrn-value').value = calc.egrn;
        document.getElementById('egrn-display').value = calc.egrn_str;
        document.getElementById('egrn').value = calc.egrn;
        document.getElementById('egrul-value').value = calc.egrul;
        document.getElementById('egrul-display').value = calc.egrul_str;
        document.getElementById('egrul').value = calc.egrul;
        document.getElementById('input-period').value = formatDate(calc.input_period);
        document.getElementById('leas-day').value = calc.leas_day;
        document.getElementById('credit-term').value = calc.credit_term;
        document.getElementById('reduce-percent').value = calc.reduce_percent;
        document.getElementById('service-life').value = calc.service_life;
        document.getElementById('amortization-group').value = calc.amortization;
        document.getElementById('nds-size').value = calc.nds_size;

        // Установите правильное значение для item_type
        var itemTypeButtons = document.querySelectorAll('.tabs button');
        itemTypeButtons.forEach(button => {
            if (button.innerText.trim() === calc.item_type) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Установите правильное значение для item_condition
        var conditionButtons = document.querySelectorAll('.button-group button');
        conditionButtons.forEach(button => {
            if (button.innerText.trim() === calc.item_condition) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Установите правильное значение для выделения НДС
        var vatButtons = document.querySelectorAll('.button-group-nds button');
        vatButtons.forEach(button => {
            if (button.innerText.trim() === calc.allocate_vat) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        })

        // Установите правильное значение для распределения задатка
        var depositButtons = document.querySelectorAll('.button-group-deposit button');
        depositButtons.forEach(button => {
            if (button.innerText.trim() === calc.allocate_deposit) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        })

        // Установите правильное значение для распределения выкупного
        var redemptionButtons = document.querySelectorAll('.button-group-redemption button');
        redemptionButtons.forEach(button => {
            if (button.innerText.trim() === calc.allocate_redemption) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        })

        // Установите правильное значение для currency
        var currencySelector = document.getElementById('currency');
        var currencyOptions = currencySelector.options;
        for (var i = 0; i < currencyOptions.length; i++) {
            if (currencyOptions[i].value === calc.currency) {
                currencySelector.selectedIndex = i;
                break;
            }
        }

        // Заполните поля траншей
        if (tranches) {
            document.getElementById('tranche1-size').value = tranches.tranche_1_size;
            document.getElementById('tranche1-rate').value = tranches.tranche_1_rate;
            document.getElementById('tranche1-fee').value = tranches.tranche_1_fee;
            document.getElementById('tranche1-own-fee').value = tranches.tranche_1_own_fee;
            document.getElementById('tranche1-credit-date').value = formatDate(tranches.tranche_1_credit_date);
            document.getElementById('payment-deferment1').value = tranches.tranche_1_payment_deferment;
            document.getElementById('tranche2-size').value = tranches.tranche_2_size;
            document.getElementById('tranche2-rate').value = tranches.tranche_2_rate;
            document.getElementById('tranche2-fee').value = tranches.tranche_2_fee;
            document.getElementById('tranche2-own-fee').value = tranches.tranche_2_own_fee;
            document.getElementById('tranche2-credit-date').value = formatDate(tranches.tranche_2_credit_date);
            document.getElementById('payment-deferment2').value = tranches.tranche_2_payment_deferment;
            document.getElementById('tranche3-size').value = tranches.tranche_3_size;
            document.getElementById('tranche3-rate').value = tranches.tranche_3_rate;
            document.getElementById('tranche3-fee').value = tranches.tranche_3_fee;
            document.getElementById('tranche3-own-fee').value = tranches.tranche_3_own_fee;
            document.getElementById('tranche3-credit-date').value = formatDate(tranches.tranche_3_credit_date);
            document.getElementById('payment-deferment3').value = tranches.tranche_3_payment_deferment;
            document.getElementById('tranche4-size').value = tranches.tranche_4_size;
            document.getElementById('tranche4-rate').value = tranches.tranche_4_rate;
            document.getElementById('tranche4-fee').value = tranches.tranche_4_fee;
            document.getElementById('tranche4-own-fee').value = tranches.tranche_4_own_fee;
            document.getElementById('tranche4-credit-date').value = formatDate(tranches.tranche_4_credit_date);
            document.getElementById('payment-deferment4').value = tranches.tranche_4_payment_deferment;
            document.getElementById('tranche5-size').value = tranches.tranche_5_size;
            document.getElementById('tranche5-rate').value = tranches.tranche_5_rate;
            document.getElementById('tranche5-fee').value = tranches.tranche_5_fee;
            document.getElementById('tranche5-own-fee').value = tranches.tranche_5_own_fee;
            document.getElementById('tranche5-credit-date').value = formatDate(tranches.tranche_5_credit_date);
            document.getElementById('payment-deferment5').value = tranches.tranche_5_payment_deferment;
        }
        if (insurances) {
            document.getElementById('insurance-casko1').value = insurances.insurance_casko1;
            document.getElementById('insurance-osago1').value = insurances.insurance_osago1;
            document.getElementById('health-insurance1').value = insurances.health_insurance1_str;
            document.getElementById('other-insurance1').value = insurances.other_insurance1_str;

            document.getElementById('insurance-casko2').value = insurances.insurance_casko2;
            document.getElementById('insurance-osago2').value = insurances.insurance_osago2;
            document.getElementById('health-insurance2').value = insurances.health_insurance2_str;
            document.getElementById('other-insurance2').value = insurances.other_insurance2_str;

            document.getElementById('insurance-casko3').value = insurances.insurance_casko3;
            document.getElementById('insurance-osago3').value = insurances.insurance_osago3;
            document.getElementById('health-insurance3').value = insurances.health_insurance3_str;
            document.getElementById('other-insurance3').value = insurances.other_insurance3_str;

            document.getElementById('insurance-casko4').value = insurances.insurance_casko4;
            document.getElementById('insurance-osago4').value = insurances.insurance_osago4;
            document.getElementById('health-insurance4').value = insurances.health_insurance4_str;
            document.getElementById('other-insurance4').value = insurances.other_insurance4_str;

            document.getElementById('insurance-casko5').value = insurances.insurance_casko5;
            document.getElementById('insurance-osago5').value = insurances.insurance_osago5;
            document.getElementById('health-insurance5').value = insurances.health_insurance5_str;
            document.getElementById('other-insurance5').value = insurances.other_insurance5_str;
        }
        // обновляем цену в рублях, если валюта не рубль
        if (calc.currency !== 'rub') {
            updateCostInRubles();
        }
        closeModal();
        const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            }
        });
        Toast.fire({
            icon: "success",
            title: "Данные из предыдущего КП были успешно скопированы."
        });
    }

    function simpleScrollTest() {
        window.scroll({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    }


    document.querySelector('.copy-btn').addEventListener('click', function () {
        var calcId = document.getElementById('modal-table').getAttribute('data-calc-id');

        // Используем SweetAlert2 для подтверждения
        Swal.fire({
            text: 'Вы хотите создать КП на основе этой?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#5182ad',
            cancelButtonColor: '#ad6c72',
            confirmButtonText: 'Да, скопировать все поля',
            cancelButtonText: 'Отменить'
        }).then((result) => {
            if (result.isConfirmed) {
                // Если пользователь подтвердил действие
                fetch(`./calculator/copy-commercial-offer/${calcId}`, {
                    method: 'GET',
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            populateForm(data);
                            // Плавная прокрутка страницы наверх
                            window.scrollTo({top: 0, behavior: 'smooth'});
                        } else {
                            // Используем SweetAlert2 для ошибки
                            Swal.fire({
                                icon: 'error',
                                title: 'Ошибка',
                                text: 'Ошибка при получении данных КП',
                                confirmButtonText: 'ОК'
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка:', error);
                        // Используем SweetAlert2 для ошибки
                        Swal.fire({
                            icon: 'error',
                            title: 'Ошибка',
                            text: 'Ошибка при получении данных КП',
                            confirmButtonText: 'ОК'
                        });
                    });
            }
        });
    });


    function formatDate(dateString) {
        if (!dateString) return "";
        var date = new Date(dateString);
        var year = date.getFullYear();
        var month = String(date.getMonth() + 1).padStart(2, '0');
        var day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
})

function simpleScrollTest() {
    window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
}

function scrollToOffers() {
    const element = document.getElementById('created-proposals');
    if (element) {
        window.scroll({
            top: element.offsetTop,
            left: 0,
            behavior: 'smooth'
        });
    }
}

document.querySelectorAll('.button-group-nds, .button-group-deposit, .button-group-redemption').forEach(group => {
    group.addEventListener('click', function (e) {
        if (e.target.classList.contains('toggle-btn')) {
            // Удаляем класс 'active' со всех кнопок в группе
            group.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
            // Добавляем класс 'active' на нажатую кнопку
            e.target.classList.add('active');
        }
    });
});

// Функция для проверки и корректировки значения в поле ввода
function validateInput(element) {
    let value = parseFloat(element.value);

    if (isNaN(value) || value < 0) {
        element.value = 0;
    } else if (value > 100) {
        element.value = 100;
    } else {
        element.value = value;
    }
}

// Функция для установки обработчиков событий на все поля
function setValidationHandlers() {
    const inputs = document.querySelectorAll('input[type="text"][id^="insurance-casko"], input[type="text"][id^="insurance-osago"], input[type="text"][id^="tranche"]');

    inputs.forEach(input => {
        // Ограничение ввода при изменении значения

        // Проверка и корректировка значения при потере фокуса
        input.addEventListener('blur', function () {
            validateInput(input);
        });
    });
}

// Установка обработчиков при загрузке страницы
document.addEventListener('DOMContentLoaded', setValidationHandlers);


document.getElementById('leas-day').addEventListener('input', function () {
    // Remove any non-digit characters
    let value = this.value.replace(/\D/g, '');

    // Limit value to 2 digits
    value = value.substring(0, 2);

    // Convert to a number
    let num = parseInt(value, 10);

    // Check if num is a valid number
    if (!isNaN(num)) {
        if (num > 31) {
            num = 31;
        } else if (num < 1) {
            num = 1;
        }
    } else {
        num = '';
    }

    // Update the input value
    this.value = num;
});

// Select all input fields with IDs starting with 'payment-deferment'
document.querySelectorAll('input[id^="payment-deferment"]').forEach(function (input) {
    input.addEventListener('input', function () {
        // Remove any non-digit characters
        this.value = this.value.replace(/\D/g, '').substring(0, 2);
    });
});

const termSlider = document.getElementById('term');
const termInput = document.getElementById('term-value');
const creditTermInput = document.getElementById('credit-term');

// Функция для синхронизации срока кредита с сроком договора
function syncCreditTerm() {
    creditTermInput.value = termInput.value;
}

// Синхронизация при загрузке страницы
window.addEventListener('DOMContentLoaded', function () {
    syncCreditTerm();
});

// Обработчик изменения срока договора через слайдер
termSlider.addEventListener('input', function () {
    termInput.value = this.value;
    syncCreditTerm();
});

// Обработчик изменения срока договора через числовой ввод
termInput.addEventListener('input', function () {
    let value = parseInt(this.value, 10);

    // Проверка и корректировка значения
    if (isNaN(value) || value < 1) {
        value = 1;
    } else if (value > 60) {
        value = 60;
    }
    this.value = value;
    termSlider.value = value;
    syncCreditTerm();
});

// Обработчик изменения срока кредита
creditTermInput.addEventListener('input', function () {
    let contractTerm = parseInt(termInput.value, 10);
    let creditTerm = parseInt(this.value, 10);

    // Проверка и корректировка значения
    if (isNaN(creditTerm)) {
        creditTerm = '';
    } else if (creditTerm > contractTerm) {
        creditTerm = contractTerm;
    }
    this.value = creditTerm;
});

// Выбираем все поля с классом 'digits-only' и добавляем общий обработчик события
document.querySelectorAll('.digits-only').forEach(function (input) {
    input.addEventListener('input', function () {
        // Удаляем все символы, кроме цифр
        let value = this.value.replace(/\D/g, '').substring(0, 3);
        let num = parseInt(value, 10);

        // Проверки для конкретных полей по их ID
        if (this.id === 'nds-size' && num > 100) {
            num = 100; // Максимальное значение для НДС - 100%
        }

        this.value = isNaN(num) ? '' : num;
    });
});

document.getElementById('payment-deferment1').addEventListener('input', function () {
    const value = this.value;

    // Обновляем другие поля
    const fields = ['payment-deferment2', 'payment-deferment3', 'payment-deferment4', 'payment-deferment5'];
    fields.forEach(function (id) {
        document.getElementById(id).value = value;
    });
});
