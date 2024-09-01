function paginateTable(rowsPerPage) {
    var table, tr, pageCount, paginationContainer, i, j;
    table = document.querySelector(".custom-table");
    tr = table.getElementsByTagName("tr");
    paginationContainer = document.getElementById("pagination-container");
    paginationContainer.innerHTML = ""; // Очищаем контейнер пагинации

    // Считаем количество страниц
    pageCount = Math.ceil((tr.length - 1) / rowsPerPage);

    // Создаем кнопки пагинации
    for (i = 1; i <= pageCount; i++) {
        var btn = document.createElement("button");
        btn.textContent = i;
        btn.setAttribute("data-page", i);
        btn.className = "pagination-button";
        btn.onclick = function () {
            var page = parseInt(this.getAttribute("data-page"));
            showPage(page, rowsPerPage);
        };
        paginationContainer.appendChild(btn);
    }

    // Показываем первую страницу и выделяем первую кнопку
    showPage(1, rowsPerPage);
}

function showPage(page, rowsPerPage) {
    var table, tr, start, end, i, paginationContainer, buttons;
    table = document.querySelector(".custom-table");
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
    paginationContainer = document.getElementById("pagination-container");
    buttons = paginationContainer.getElementsByClassName("pagination-button");

    for (i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("active");
    }

    buttons[page - 1].classList.add("active");
}
