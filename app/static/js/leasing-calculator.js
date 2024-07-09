document.getElementById('cost').addEventListener('input', function () {
    document.getElementById('cost-value').value = this.value;
});
document.getElementById('cost-value').addEventListener('input', function () {
    document.getElementById('cost').value = this.value;
});

document.getElementById('initial-payment').addEventListener('input', function () {
    var totalCost = parseInt(document.getElementById('cost').value);
    var percentValue = (this.value / totalCost) * 100;
    document.getElementById('initial-payment-value').value = this.value;
    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
});

document.getElementById('initial-payment-value').addEventListener('input', function () {
    var totalCost = parseInt(document.getElementById('cost').value);
    var percentValue = (this.value / totalCost) * 100;
    document.getElementById('initial-payment').value = this.value;
    document.getElementById('initial-payment-percent').value = percentValue.toFixed(2);
});

document.getElementById('initial-payment-percent').addEventListener('input', function () {
    var totalCost = parseInt(document.getElementById('cost').value);
    var value = (this.value / 100) * totalCost;
    document.getElementById('initial-payment').value = value;
    document.getElementById('initial-payment-value').value = value.toFixed(0);
});

document.getElementById('term').addEventListener('input', function () {
    document.getElementById('term-value').value = this.value;
});
document.getElementById('term-value').addEventListener('input', function () {
    document.getElementById('term').value = this.value;
});


document.querySelectorAll('.tabs button').forEach(button => {
    button.addEventListener('click', function () {
        document.querySelectorAll('.tabs button').forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
    });
});
