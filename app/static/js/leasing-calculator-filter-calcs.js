document.querySelector('.leasing-calculator-date-filter-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Предотвращаем перезагрузку страницы

    // Получаем значения дат из полей
    let startDate = document.getElementById('start_date').value;
    let endDate = document.getElementById('end_date').value;

    // Создаем параметры для запроса
    let params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
    });

    // Отправляем запрос с использованием Fetch API
    fetch(`/crm/calculator/update-table?${params.toString()}`)
        .then(response => response.text())
        .then(data => {
            // Заменяем содержимое таблицы новым HTML
            document.getElementById('calc-list-main').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', function () {
    // Получаем элемент для даты конца
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    const creditDate1 = document.getElementById('tranche1-credit-date');
    const creditDate2 = document.getElementById('tranche2-credit-date');
    const creditDate3 = document.getElementById('tranche3-credit-date');
    const creditDate4 = document.getElementById('tranche4-credit-date');
    const creditDate5 = document.getElementById('tranche5-credit-date');

    // Получаем текущую дату
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Месяцы от 0 до 11, поэтому +1
    const dd = String(today.getDate()).padStart(2, '0');

    // Форматируем дату в строку YYYY-MM-DD
    const currentDate = `${yyyy}-${mm}-${dd}`;

    // Устанавливаем значение по умолчанию для поля end_date
    startDateInput.value = currentDate;
    endDateInput.value = currentDate;
    creditDate1.value = currentDate;
    creditDate2.value = currentDate;
    creditDate3.value = currentDate;
    creditDate4.value = currentDate;
    creditDate5.value = currentDate;
});