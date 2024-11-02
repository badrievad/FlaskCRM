function createCommercialOffer(scheduleType, leasCalculatorId) {
	// Блокируем все кнопки
	document.getElementById('calculate-button-annuity').disabled = true
	document.getElementById('calculate-button-differentiated').disabled = true
	document.getElementById('calculate-button-regression').disabled = true

	// Изменяем стиль для заблокированных кнопок
	const buttons = document.querySelectorAll('.btn-hover')
	buttons.forEach(button => {
		button.style.opacity = '0.6' // Добавляем полупрозрачность
		button.style.cursor = 'not-allowed' // Изменяем курсор на "запрещено"
	})

	// Блокируем ссылку "Назад"
	const backButton = document.querySelector('.btn-back')
	if (backButton) {
		backButton.style.opacity = '0.6' // Добавляем полупрозрачность
		backButton.style.pointerEvents = 'none' // Отключаем возможность клика
		backButton.style.cursor = 'not-allowed' // Изменяем курсор на "запрещено"
	}

	// Создаем форму для отправки POST-запроса
	const form = document.createElement('form')
	form.method = 'POST'
	form.action = `/crm/calculator/${leasCalculatorId}/create-commercial-offer`

	// Создаем скрытое поле для передачи типа графика
	const input = document.createElement('input')
	input.type = 'hidden'
	input.name = 'type_of_schedule'
	input.value = scheduleType

	// Добавляем скрытое поле в форму
	form.appendChild(input)

	// Отправляем форму
	document.body.appendChild(form)
	form.submit()
}

// Получаем элементы чекбокса и статуса
const includeRateCheckbox = document.getElementById('include-rate')

const increaseRateStatusAnnuity = document.getElementById(
	'increase-rate-status-annuity'
)
const increaseRateStatusDifferentiated = document.getElementById(
	'increase-rate-status-differentiated'
)
const increaseRateStatusRegression = document.getElementById(
	'increase-rate-status-regression'
)

// Функция для обновления текста и класса
function updateIncreaseRateStatus() {
	const isChecked = includeRateCheckbox.checked

	const statusElements = [
		increaseRateStatusAnnuity,
		increaseRateStatusDifferentiated,
		increaseRateStatusRegression,
	]

	statusElements.forEach(element => {
		if (isChecked) {
			element.textContent = '(включена в КП)'
			element.classList.remove('rate-excluded')
			element.classList.add('rate-included')
		} else {
			element.textContent = '(не включена в КП)'
			element.classList.remove('rate-included')
			element.classList.add('rate-excluded')
		}
		// Выводим в консоль текущие классы элемента для отладки
		console.log(`Element ID: ${element.id}, Classes: ${element.className}`)
	})
}

// Добавляем обработчик события изменения состояния чекбокса
includeRateCheckbox.addEventListener('change', updateIncreaseRateStatus)

// Вызываем функцию при загрузке страницы, чтобы установить начальное состояние
updateIncreaseRateStatus()
