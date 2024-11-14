document.addEventListener('DOMContentLoaded', function () {
	// Получаем элементы
	var modal = document.getElementById('decision-modal')
	var makeDecisionButton = document.getElementById('make-decision-button')
	var closeModalButton = document.getElementById('close-modal')

	// Открытие модального окна при клике на кнопку "Принять решение"
	makeDecisionButton.addEventListener('click', function () {
		modal.classList.add('modal-visible')
	})

	// Функция для закрытия модального окна
	function closeModal() {
		modal.classList.remove('modal-visible')
	}

	// Закрытие модального окна при клике на крестик
	closeModalButton.addEventListener('click', closeModal)

	// Закрытие модального окна при клике вне его
	window.addEventListener('click', function (event) {
		if (event.target == modal) {
			closeModal()
		}
	})
})

// Функция для отправки решения на сервер (остается без изменений)
function submitDecision(decision) {
	// Подтверждение действия
	var confirmMessage = ''
	switch (decision) {
		case 'approve':
			confirmMessage = 'Вы уверены, что хотите одобрить сделку?'
			break
		case 'send_to_committee':
			confirmMessage =
				'Вы уверены, что хотите отправить сделку на инвестиционный комитет?'
			break
		case 'reject':
			confirmMessage = 'Вы уверены, что хотите отказать по сделке?'
			break
	}

	if (confirm(confirmMessage)) {
		// Создаем форму для отправки POST-запроса
		var form = document.createElement('form')
		form.method = 'POST'
		form.action =
			'{{ url_for("risk_department.process_decision", deal_id=deal_id) }}'

		// Добавляем скрытое поле с решением
		var input = document.createElement('input')
		input.type = 'hidden'
		input.name = 'decision'
		input.value = decision
		form.appendChild(input)

		// Добавляем форму на страницу и отправляем ее
		document.body.appendChild(form)
		form.submit()
	}
}
