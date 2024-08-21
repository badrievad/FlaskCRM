// URL для загрузки JSON данных с сервера
const apiUrl = './calculator/overheads';

// Функция для загрузки JSON данных с API
async function loadJSON() {
    const response = await fetch(apiUrl);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Функция для обновления значений на странице
function updateValues(data) {
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            // Находим элемент по id и обновляем его значение
            let element = document.getElementById(key);
            if (element) {
                element.value = data[key];
            }
        }
    }
}

// Обработчик нажатия на кнопку "По умолчанию"
document.getElementById('default-button').addEventListener('click', async () => {
    try {
        const jsonData = await loadJSON();
        updateValues(jsonData.default);
    } catch (error) {
        console.error('Error loading JSON:', error);
    }
});

// Обработчик нажатия на кнопку "Очистить"
document.getElementById('clear-button').addEventListener('click', async () => {
    try {
        const jsonData = await loadJSON();
        updateValues(jsonData.clear);
    } catch (error) {
        console.error('Error loading JSON:', error);
    }
});
