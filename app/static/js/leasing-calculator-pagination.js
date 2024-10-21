function paginateTable(tableClass, paginationContainerId, rowsPerPage) {
    let table, tr, pageCount, paginationContainer, i;
    table = document.querySelector(tableClass);
    tr = table.getElementsByTagName("tr");
    paginationContainer = document.getElementById(paginationContainerId);
    paginationContainer.innerHTML = ""; // Очищаем контейнер пагинации

    // Считаем количество страниц
    pageCount = Math.ceil((tr.length - 1) / rowsPerPage); // Предполагаем, что первая строка — заголовок

    // Создаем кнопки пагинации
    for (i = 1; i <= pageCount; i++) {
        let btn = document.createElement("button");
        btn.textContent = i;
        btn.setAttribute("data-page", i);
        btn.className = `pagination-button-${paginationContainerId}`;  // Уникальный класс для каждой таблицы
        btn.onclick = function () {
            let page = parseInt(this.getAttribute("data-page"));
            showPage(page, rowsPerPage, tableClass, paginationContainerId);
        };
        paginationContainer.appendChild(btn);
    }

    // Показываем первую страницу и выделяем первую кнопку
    showPage(1, rowsPerPage, tableClass, paginationContainerId);
}

function showPage(page, rowsPerPage, tableClass, paginationContainerId) {
    let table, tr, start, end, i, paginationContainer, buttons;
    table = document.querySelector(tableClass);
    tr = table.getElementsByTagName("tr");

    start = (page - 1) * rowsPerPage + 1; // Начальный индекс строки
    end = start + rowsPerPage; // Конечный индекс строки

    // Перебираем строки и показываем только те, которые принадлежат текущей странице
    for (i = 1; i < tr.length; i++) {
        if (i >= start && i < end) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }

    // Обновляем выделение активной кнопки
    paginationContainer = document.getElementById(paginationContainerId);
    buttons = paginationContainer.getElementsByClassName(`pagination-button-${paginationContainerId}`);

    // Убираем выделение с предыдущих кнопок
    for (i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("active");
    }

    // Проверяем, что кнопка существует, прежде чем добавлять класс active
    if (buttons[page - 1]) {
        buttons[page - 1].classList.add("active");
    }
}


document.addEventListener("DOMContentLoaded", function () {
    // Для первой таблицы
    paginateTable(".custom-table", "pagination-container", 10);

// Для второй таблицы
    paginateTable(".calc-list-table", "pagination-container-calc", 10);
});

