document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('.icon-item').forEach(item => {
		item.addEventListener('click', async () => {
			const folderPath = item.getAttribute('data-folder-path')
			if (folderPath) {
				try {
					const response = await fetch('http://localhost:5001/open-deal-folder', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({ folder_path: folderPath }),
					})

					if (!response.ok) {
						// Обработка HTTP ошибок
						console.error(
							`HTTP ошибка: ${response.status} ${response.statusText}`
						)
						return
					}

					const data = await response.json()
					if (data.status === 'success') {
						console.log('Папка успешно открыта.')
					} else {
						console.error('Ошибка на сервере:', data.message)
					}
				} catch (error) {
					console.error('Ошибка запроса:', error.message)
				}
			} else {
				console.error('Путь к папке не найден.')
			}
		})
	})
})
