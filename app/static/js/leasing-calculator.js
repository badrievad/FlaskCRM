document.addEventListener('DOMContentLoaded', function () {
    const propertyValue = document.getElementById('property-value');
    const propertyValueOutput = document.getElementById('property-value-output');
    const initialPayment = document.getElementById('initial-payment');
    const initialPaymentOutput = document.getElementById('initial-payment-output');
    const initialPaymentPercent = document.getElementById('initial-payment-percent');
    const contractTerm = document.getElementById('contract-term');
    const contractTermOutput = document.getElementById('contract-term-output');
    const finalPayment = document.getElementById('final-payment');
    const finalPaymentOutput = document.getElementById('final-payment-output');
    const calculateBtn = document.querySelector('.calculate-btn');

    propertyValue.addEventListener('input', function () {
        propertyValueOutput.textContent = `${Number(propertyValue.value).toLocaleString()} ₽`;
    });

    initialPayment.addEventListener('input', function () {
        const value = (propertyValue.value * initialPayment.value / 100).toLocaleString();
        initialPaymentOutput.textContent = `${value} ₽`;
        initialPaymentPercent.textContent = `${initialPayment.value}%`;
    });

    contractTerm.addEventListener('input', function () {
        contractTermOutput.textContent = `${contractTerm.value} месяцев`;
    });

    finalPayment.addEventListener('input', function () {
        finalPaymentOutput.textContent = `${finalPayment.value}%`;
    });

    calculateBtn.addEventListener('click', function () {
        // Здесь можно добавить расчет на основе введенных данных
        alert('Расчет произведен!');
    });
});
