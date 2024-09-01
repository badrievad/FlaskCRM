document.addEventListener("DOMContentLoaded", function () {
    paginateTable(10); // Начальное количество строк на странице
});

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

function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toLowerCase();
    table = document.querySelector(".custom-table");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByClassName("item-name")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
