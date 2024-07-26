function deleteCalculation(event, calcId) {
    event.stopPropagation(); // Остановить всплытие события, чтобы не вызывать openModal
    if (confirm("Вы уверены, что хотите удалить этот расчет?")) {
        fetch(`./calculator/delete/${calcId}`, {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector(`i[data-id='${calcId}']`).closest('tr').remove();
                } else {
                    alert('Ошибка при удалении расчета: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при удалении расчета.');
            });
    }
}

function downloadCalculation(event, calcId) {
    event.stopPropagation(); // Остановить всплытие события, чтобы не вызывать openModal
    if (confirm("Вы уверены, что хотите скачать этот расчет?")) {
        window.location.href = `./calculator/download/${calcId}`;
    }
}