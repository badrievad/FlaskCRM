// Функция для пересчета даты первого платежа
function calculateFirstPaymentDate() {
    // Получаем значения полей
    const leasDay = document.getElementById('leas-day').value;
    const creditDate = document.getElementById('tranche1-credit-date').value;
    const deferment = document.getElementById('payment-deferment1').value || 0; // Если отсрочка не указана, считаем её как 0
    const preCalculateButton = document.getElementById('pre-calculate-button');

    // Если дата выдачи кредита не выбрана, не производим расчеты
    if (!creditDate) {
        document.getElementById('calculated-payment-date').textContent = 'Укажите дату выдачи кредита';
        return;
    }

    // Преобразуем значения
    const creditDateObj = new Date(creditDate); // Дата выдачи кредита
    const leasDayInt = parseInt(leasDay); // День лизингового платежа
    const defermentInt = parseInt(deferment); // Отсрочка по уплате платежей в месяцах

    // Если день лизингового платежа не указан, выводим ошибку
    if (isNaN(leasDayInt) || leasDayInt < 1 || leasDayInt > 31) {
        document.getElementById('calculated-payment-date').textContent = 'Укажите корректный день лизингового платежа';
        document.getElementById('calculated-payment-date').style.color = '#5e2626';
        return;
    }

    // Прибавляем к дате выдачи кредита количество месяцев отсрочки
    creditDateObj.setMonth(creditDateObj.getMonth() + defermentInt);

    // Устанавливаем день лизингового платежа
    creditDateObj.setDate(leasDayInt);

    // Проверка на случай перехода месяца (если, например, 31-й день в месяце с 30 днями)
    if (creditDateObj.getDate() !== leasDayInt) {
        creditDateObj.setDate(0); // Устанавливаем на последний день предыдущего месяца
    }

    // Преобразуем дату в формат dd.mm.yyyy
    const day = String(creditDateObj.getDate()).padStart(2, '0');
    const month = String(creditDateObj.getMonth() + 1).padStart(2, '0'); // Месяцы от 0 до 11
    const year = creditDateObj.getFullYear();
    const formattedDate = `${day}.${month}.${year}`;

    // Обновляем текст с рассчитанной датой
    const calculatedDateElement = document.getElementById('calculated-payment-date');
    const calcIcon = document.getElementById('date-warning-icon');
    calculatedDateElement.textContent = formattedDate;

    // Получаем текущую дату
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Обнуляем часы для сравнения только по дате

    // Сравниваем даты
    if (creditDateObj < today) {
        // Если дата меньше или равна текущей, окрашиваем в красный и показываем предупреждающую иконку
        calculatedDateElement.style.color = '#5e2626';
        document.getElementById('date-warning-icon').style.display = 'inline'; // Показываем иконку
        preCalculateButton.disabled = true; // Заблокировать кнопку
        preCalculateButton.classList.add('button-disabled'); // Добавить класс для изменения цвета
    } else {
        // Если дата больше текущей, окрашиваем в зеленый и скрываем иконку
        calculatedDateElement.style.color = 'green';
        document.getElementById('date-warning-icon').style.display = 'none'; // Скрываем иконку
        preCalculateButton.disabled = false; // Разблокировать кнопку
        preCalculateButton.classList.remove('button-disabled'); // Убрать класс для изменения цвета
    }
}

// Отслеживание изменений в полях
document.getElementById('leas-day').addEventListener('input', calculateFirstPaymentDate);
document.getElementById('tranche1-credit-date').addEventListener('change', calculateFirstPaymentDate);
document.getElementById('payment-deferment1').addEventListener('input', calculateFirstPaymentDate);

// Рассчет даты при загрузке страницы
document.addEventListener('DOMContentLoaded', calculateFirstPaymentDate);