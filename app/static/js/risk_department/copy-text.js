// Функция для копирования текста с использованием document.execCommand
function copyToClipboardFallback(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed'; // Фиксируем, чтобы не мешать интерфейсу
    textarea.style.opacity = '0'; // Делаем невидимым
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
        document.execCommand('copy');
    } catch (err) {
        console.error('Ошибка при копировании через execCommand:', err);
    }
    document.body.removeChild(textarea);
}

// Добавляем обработчики клика для элементов с классом "copyable"
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.copyable').forEach(element => {
        element.addEventListener('click', () => {
            const textToCopy = element.getAttribute('data-copy');
            if (textToCopy) {
                copyToClipboardFallback(textToCopy);

                // Находим родительский элемент (data-row) и меняем цвет текста
                const parentRow = element.closest('.data-row');
                if (parentRow) {
                    const dataValue = parentRow.querySelector('.data-value');
                    if (dataValue) {
                        dataValue.style.color = '#FF4C4C'; // Например, светло-красный
                        dataValue.style.transition = 'color 0.3s';

                        // Сбрасываем цвет через 1.5 секунды
                        setTimeout(() => {
                            dataValue.style.color = '';
                        }, 300);
                    }
                }
            }
        });
    });
});
