document.addEventListener("DOMContentLoaded", function () {
    paginateTable(10); // Начальное количество строк на странице
});

function deleteCalculation(event, calcId) {
    event.stopPropagation(); // Остановить всплытие события, чтобы не вызывать openModal

    // Используем SweetAlert2 для подтверждения
    Swal.fire({
        text: 'Вы уверены, что хотите удалить это КП?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ad6c72',
        cancelButtonColor: '#5789b9',
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отменить'
    }).then((result) => {
        if (result.isConfirmed) {
            // Если пользователь подтвердил действие
            fetch(`./calculator/delete/${calcId}`, {
                method: 'POST',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Удаляем строку расчета из таблицы
                        document.querySelector(`i[data-id='${calcId}']`).closest('tr').remove();
                        // Уведомление об успешном удалении
                        Swal.fire({
                            title: 'Удалено!',
                            text: 'КП было успешно удалено.',
                            icon: 'success',
                            timer: 2000,
                            showConfirmButton: false,
                        });
                    } else {
                        // Показать ошибку через SweetAlert2
                        Swal.fire({
                            icon: 'error',
                            title: 'Ошибка',
                            text: 'Ошибка при удалении расчета: ' + data.message,
                            confirmButtonText: 'ОК',
                            confirmButtonColor: '#5789b9'
                        });
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    // Показать ошибку через SweetAlert2
                    Swal.fire({
                        icon: 'error',
                        title: 'Ошибка',
                        text: 'Произошла ошибка при удалении расчета.',
                        confirmButtonText: 'ОК'
                    });
                });
        }
    });
}


function downloadCalculation(event, calcId) {
    event.stopPropagation(); // Остановить всплытие события, чтобы не вызывать openModal

    // Используем SweetAlert2 для подтверждения
    Swal.fire({
        text: 'Вы уверены, что хотите скачать это КП?',
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#5789b9',
        cancelButtonColor: '#ad6c72',
        confirmButtonText: 'Да, скачать',
        cancelButtonText: 'Отменить'
    }).then((result) => {
        if (result.isConfirmed) {
            // Если пользователь подтвердил действие
            window.location.href = `./calculator/download/${calcId}`;
        }
    });
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
