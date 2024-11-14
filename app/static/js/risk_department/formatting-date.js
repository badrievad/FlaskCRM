document.addEventListener('DOMContentLoaded', function () {
	// Получаем элемент с датой
	var dateElement = document.getElementById('registration-date')
	var dateString = dateElement.textContent.trim()

	// Преобразуем строку в объект Date
	var date = new Date(dateString)

	// Проверяем, что дата корректна
	if (!isNaN(date)) {
		// Опции форматирования
		var options = {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
		}

		// Форматируем дату в российском формате
		var formattedDate = date.toLocaleDateString('ru-RU', options)

		// Обновляем содержимое элемента
		dateElement.textContent = formattedDate
	} else {
		console.error('Некорректная дата:', dateString)
	}
})
