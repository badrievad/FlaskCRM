document.addEventListener('DOMContentLoaded', () => {
	// Находим все элементы с классом "icon-item"
	document.querySelectorAll('.icon-item').forEach(item => {
		item.addEventListener('click', () => {
			const url = item.getAttribute('data-url')
			if (url) {
				window.location.href = url // Перенаправление на URL
			}
		})
	})
})
