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
	let confirmMessage = ''
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

	// Используем SweetAlert2 для подтверждения
	Swal.fire({
		title: 'Подтверждение',
		text: confirmMessage,
		icon: 'warning',
		showCancelButton: true,
		confirmButtonText: 'Да',
		confirmButtonColor: '#67a2d5',
		cancelButtonText: 'Отмена',
	}).then(result => {
		if (result.isConfirmed) {
			// Получаем текущий URL
			const currentUrl = window.location.href

			// Извлекаем deal_id из URL
			const dealIdMatch = currentUrl.match(/risk-department\/(\d+)/)
			const deal_id = dealIdMatch ? dealIdMatch[1] : null

			if (!deal_id) {
				console.error('Не удалось получить deal_id из URL')
				Swal.fire({
					title: 'Ошибка',
					text: 'Не удалось получить идентификатор сделки.',
					icon: 'error',
				})
				return
			}

			// Получаем базовый URL до 'risk-department'
			const baseUrlMatch = currentUrl.match(/(.*risk-department\/\d+)/)
			const baseUrl = baseUrlMatch ? baseUrlMatch[1] : ''

			if (!baseUrl) {
				console.error('Не удалось получить базовый URL')
				Swal.fire({
					title: 'Ошибка',
					text: 'Не удалось получить базовый URL.',
					icon: 'error',
				})
				return
			}

			// Отправляем AJAX-запрос с помощью fetch
			fetch(`./process_decision/${deal_id}`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ decision: decision }),
			})
				.then(response => response.json())
				.then(data => {
					// Обработка ответа от сервера
					if (data.success) {
						Swal.fire({
							title: 'Успех',
							text: data.message,
							icon: 'success',
						}).then(() => {
							// Обновляем страницу или выполняем другие действия
							location.reload()
						})
					} else {
						Swal.fire({
							title: 'Ошибка',
							text: data.message,
							icon: 'error',
						})
					}
				})
				.catch(error => {
					console.error('Ошибка:', error)
					Swal.fire({
						title: 'Ошибка',
						text: 'Произошла ошибка при обработке запроса.',
						icon: 'error',
					})
				})
		}
	})
}
