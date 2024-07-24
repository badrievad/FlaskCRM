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
});

document.getElementById('cost-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('cost-value').value = value;
    document.getElementById('cost').value = value;
    updateInitialPaymentValue();
});

document.getElementById('cost-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
});

document.getElementById('initial-payment').addEventListener('input', function () {
    var percentValue = parseFloat(this.value);
    var totalCost = parseInt(document.getElementById('cost-value').value);
    var initialPaymentValue = (percentValue / 100) * totalCost;

    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
    document.getElementById('initial-payment-value-display').value = formatNumber(initialPaymentValue);
});

document.getElementById('initial-payment-value-display').addEventListener('input', function () {
    var totalCost = parseInt(document.getElementById('cost-value').value);
    var initialPaymentValue = parseFormattedNumber(this.value);
    var maxInitialPaymentValue = totalCost * 0.4999;
    if (initialPaymentValue > maxInitialPaymentValue) {
        initialPaymentValue = maxInitialPaymentValue;
    }
    var percentValue = (initialPaymentValue / totalCost) * 100;

    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
    document.getElementById('initial-payment').value = percentValue;
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
});

document.getElementById('initial-payment-value-display').addEventListener('blur', function () {
    var totalCost = parseInt(document.getElementById('cost-value').value);
    var initialPaymentValue = parseFormattedNumber(this.value);
    var maxInitialPaymentValue = totalCost * 0.4999;
    if (initialPaymentValue > maxInitialPaymentValue) {
        initialPaymentValue = maxInitialPaymentValue;
    }
    this.value = formatNumber(initialPaymentValue);
});

document.getElementById('initial-payment-percent').addEventListener('input', function () {
    var percentValue = parseFloat(this.value);
    var totalCost = parseInt(document.getElementById('cost-value').value);
    var initialPaymentValue = (percentValue / 100) * totalCost;

    if (percentValue > 49.99) {
        percentValue = 49.99;
        initialPaymentValue = totalCost * (percentValue / 100);
    }

    document.getElementById('initial-payment').value = percentValue;
    document.getElementById('initial-payment-value').value = initialPaymentValue.toFixed(0);
    document.getElementById('initial-payment-value-display').value = formatNumber(initialPaymentValue);
});

document.getElementById('term').addEventListener('input', function () {
    document.getElementById('term-value').value = this.value;
});

document.getElementById('term-value').addEventListener('input', function () {
    document.getElementById('term').value = this.value;
});

document.getElementById('percent').addEventListener('input', function () {
    document.getElementById('percent-value').value = this.value;
});

document.getElementById('percent-value').addEventListener('input', function () {
    document.getElementById('percent').value = this.value;
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

document.getElementById('foreign-cost').addEventListener('input', function () {
    var value = parseInt(this.value);
    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost-display').value = formatNumber(value);
});

document.getElementById('foreign-cost-display').addEventListener('input', function () {
    var value = parseFormattedNumber(this.value);
    document.getElementById('foreign-cost-value').value = value;
    document.getElementById('foreign-cost').value = value;
});

document.getElementById('foreign-cost-display').addEventListener('blur', function () {
    this.value = formatNumber(parseFormattedNumber(this.value));
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
