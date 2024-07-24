document.getElementById('add-tranche').addEventListener('click', function () {
    var table = document.getElementById('tranches-table');
    var headers = table.querySelectorAll('thead th');
    var tbodyRows = table.querySelectorAll('tbody tr');

    if (headers.length >= 6) { // включая пустой th
        alert('Можно добавить до 5 траншей');
        return;
    }

    var trancheNumber = headers.length;

    // Добавляем новый заголовок
    var newTh = document.createElement('th');
    newTh.id = 'tranche-' + trancheNumber;
    newTh.textContent = 'Транш ' + trancheNumber;
    headers[0].parentElement.appendChild(newTh);

    // Добавляем новые ячейки в каждую строку тела таблицы
    tbodyRows.forEach(function (row, index) {
        var newTd = document.createElement('td');
        var input = document.createElement('input');
        if (index === 4 || index === 5) { // Для строк с датами
            input.type = 'date';
        } else {
            input.type = 'text';
        }
        newTd.appendChild(input);
        row.appendChild(newTd);
    });
});

document.getElementById('remove-tranche').addEventListener('click', function () {
    var table = document.getElementById('tranches-table');
    var headers = table.querySelectorAll('thead th');
    var tbodyRows = table.querySelectorAll('tbody tr');

    if (headers.length <= 3) { // включая пустой th, первые два транша не удаляются
        alert('Нельзя удалить первые два транша');
        return;
    }

    var trancheNumber = headers.length - 1;

    // Удаляем последний заголовок транша
    headers[trancheNumber].remove();

    // Удаляем соответствующие ячейки из каждой строки тела таблицы
    tbodyRows.forEach(function (row) {
        row.removeChild(row.children[trancheNumber]);
    });
});
