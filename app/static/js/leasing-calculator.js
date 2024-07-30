function formatNumber(value) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

function parseFormattedNumber(value) {
    return parseFloat(value.replace(/\s/g, '').replace(',', '.'));
}

document.getElementById('cost').addEventListener('input', function () {
    var value = parseInt(this.value);
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
    var totalCost = parseInt(document.getElementById('cost-value').value);
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

    var totalCost = parseInt(document.getElementById('cost-value').value);
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
    var totalCost = parseInt(document.getElementById('cost-value').value);
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

    var totalCost = parseInt(document.getElementById('cost-value').value);

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
    var totalCost = parseInt(document.getElementById('cost-value').value);
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
    var value = parseInt(this.value);
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
    var value = parseInt(this.value);
    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost-display').value = formatNumber(value);
    updateCostInRubles();  // Обновляем стоимость в рублях при изменении слайдера
});

function updateCreditValue() {
    var totalCost = parseInt(document.getElementById('cost-value').value);
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

    var totalCost = parseInt(document.getElementById('cost-value').value);
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

document.getElementById('commission-value').addEventListener('input', function () {
    if (this.value > 5) {
        this.value = 5;
    }

    document.getElementById('commission').value = this.value;
});

document.getElementById('commission-value').addEventListener('keypress', function (event) {
    if (event.key === '-' || event.key === '+' || (event.key < '0' || event.key > '9') && event.key !== '.') {
        event.preventDefault();
    }
});

// Расходы на страхование КАСКО
document.getElementById('insurance-casko').addEventListener('input', function () {
    document.getElementById('insurance-casko-value').value = this.value;
});

document.getElementById('insurance-casko-value').addEventListener('blur', function () {
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
    document.getElementById('insurance-casko').value = numericValue;
});


document.getElementById('insurance-casko-value').addEventListener('keypress', function () {
    // Разрешить только цифры и блокировать -, +
    if (event.key === '-' || event.key === '+' || event.key === 'e') {
        event.preventDefault();
    }
});

// Расходы на страхование ОСАГО
document.getElementById('insurance-osago').addEventListener('input', function () {
    document.getElementById('insurance-osago-value').value = this.value;
});

document.getElementById('insurance-osago-value').addEventListener('blur', function () {
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
    document.getElementById('insurance-osago').value = numericValue;
});


document.getElementById('insurance-osago-value').addEventListener('keypress', function () {
    // Разрешить только цифры и блокировать -, +
    if (event.key === '-' || event.key === '+' || event.key === 'e') {
        event.preventDefault();
    }
});

// Расходы на страхование ЖИЗНИ и ЗДОРОВЬЯ
document.getElementById('health-insurance').addEventListener('input', function () {
    document.getElementById('health-insurance-value').value = this.value;
    document.getElementById('health-insurance-display').value = this.value;
});

document.getElementById('health-insurance-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);

    if (isNaN(value) || this.value.trim().toLowerCase() === 'не число') {
        value = 0;
    }

    document.getElementById('health-insurance-value').value = value;
    document.getElementById('health-insurance').value = value;
});

// Расходы на страхование ИНОЕ
document.getElementById('other-insurance').addEventListener('input', function () {
    document.getElementById('other-insurance-value').value = this.value;
    document.getElementById('other-insurance-display').value = this.value;
});

document.getElementById('other-insurance-display').addEventListener('input', function () {
    var value = parseInt(this.value.replace(/\D/g, ''), 10);
    document.getElementById('other-insurance-value').value = value;
    document.getElementById('other-insurance').value = value;
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

document.getElementById('health-insurance-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('other-insurance-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('tracker-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('mayak-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('fedresurs-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('gsm-display').addEventListener('keypress', allowOnlyNumbers);
document.getElementById('mail-display').addEventListener('keypress', allowOnlyNumbers);

// Форматирование для health-insurance-display
document.getElementById('health-insurance-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('health-insurance').value = value;
});

document.getElementById('health-insurance-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера health-insurance
document.getElementById('health-insurance').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('health-insurance-display').value = formatNumber(value);
});

// Форматирование для other-insurance-display
document.getElementById('other-insurance-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('other-insurance').value = value;
});

document.getElementById('other-insurance-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера other-insurance
document.getElementById('other-insurance').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('other-insurance-display').value = formatNumber(value);
});

// Форматирование для tracker-display
document.getElementById('tracker-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('tracker').value = value;
});

document.getElementById('tracker-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера tracker
document.getElementById('tracker').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('tracker-display').value = formatNumber(value);
});

// Форматирование для mayak-display
document.getElementById('mayak-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('mayak').value = value;
});

document.getElementById('mayak-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера mayak
document.getElementById('mayak').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('mayak-display').value = formatNumber(value);
});

// Форматирование для fedresurs-display
document.getElementById('fedresurs-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('fedresurs').value = value;
});

document.getElementById('fedresurs-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера fedresurs
document.getElementById('fedresurs').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('fedresurs-display').value = formatNumber(value);
});

// Форматирование для gsm-display
document.getElementById('gsm-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('gsm').value = value;
});

document.getElementById('gsm-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера gsm
document.getElementById('gsm').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('gsm-display').value = formatNumber(value);
});

// Форматирование для mail-display
document.getElementById('mail-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('mail').value = value;
});

document.getElementById('mail-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

// Обработчик для слайдера mail
document.getElementById('mail').addEventListener('input', function () {
    var value = parseInt(this.value, 10);
    document.getElementById('mail-display').value = formatNumber(value);
});

