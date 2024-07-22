document.addEventListener('DOMContentLoaded', function () {
    fetch('./calculator/get_exchange_rates')
        .then(response => response.json())
        .then(data => {
            document.getElementById('today-date').innerText = data.today.date;
            document.getElementById('previous-date').innerText = data.previous_day.date;

            document.getElementById('today-cny').innerText = data.today.cny + ' ₽';
            document.getElementById('previous-cny').innerText = data.previous_day.cny + ' ₽';

            document.getElementById('today-usd').innerText = data.today.usd + ' ₽';
            document.getElementById('previous-usd').innerText = data.previous_day.usd + ' ₽';

            document.getElementById('today-eur').innerText = data.today.eur + ' ₽';
            document.getElementById('previous-eur').innerText = data.previous_day.eur + ' ₽';
        })
        .catch(error => console.error('Error fetching exchange rates:', error));
});