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
    const endDateInput = document.getElementById('end_date');

    // Получаем текущую дату
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Месяцы от 0 до 11, поэтому +1
    const dd = String(today.getDate()).padStart(2, '0');

    // Форматируем дату в строку YYYY-MM-DD
    const currentDate = `${yyyy}-${mm}-${dd}`;

    // Устанавливаем значение по умолчанию для поля end_date
    endDateInput.value = currentDate;
});