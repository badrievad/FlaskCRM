// Обработчик для кнопки удаления
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('edit-delete-icon')) {
        var index = event.target.getAttribute('data-index');
        console.log(index)
        deleteSellerId(index);
    }
});

// Функция для удаления seller_id
function deleteSellerId(index) {
    var calcId = getCalcIdFromSection(index); // Получаем calc_id по индексу

    Swal.fire({
        text: `Вы точно хотите удалить поставщика для этого договора?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#67a2d5',
        cancelButtonColor: '#ad6c72',
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отменить'
    }).then((result) => {
        if (result.isConfirmed) {
            // Отправляем AJAX-запрос для удаления seller_id
            $.ajax({
                url: '/crm/deal/inside/delete-seller', // Ваш серверный маршрут
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    calc_id: calcId
                }),
                success: function (response) {
                    // Обновляем отображаемые значения на фронтенде после успешного удаления
                    document.getElementById(`supplier-name-display-${index}`).textContent = '';
                    document.getElementById(`supplier-inn-display-${index}`).textContent = '';
                    document.getElementById(`supplier-ogrn-display-${index}`).textContent = '';
                    document.getElementById(`supplier-address-display-${index}`).textContent = '';
                    document.getElementById(`supplier-phone-display-${index}`).textContent = '';
                    document.getElementById(`supplier-email-display-${index}`).textContent = '';
                    document.getElementById(`supplier-signer-display-${index}`).textContent = '';

                    document.getElementById(`supplier-name-input-${index}`).value = '';
                    document.getElementById(`supplier-inn-input-${index}`).value = '';
                    document.getElementById(`supplier-ogrn-input-${index}`).value = '';
                    document.getElementById(`supplier-address-input-${index}`).value = '';
                    document.getElementById(`supplier-phone-input-${index}`).value = '';
                    document.getElementById(`supplier-email-input-${index}`).value = '';
                    document.getElementById(`supplier-signer-input-${index}`).value = '';

                    // Удаляем иконку удаления
                    var deleteIcon = document.getElementById(`edit-delete-icon-${index}`);
                    if (deleteIcon) {
                        deleteIcon.remove();
                    }

                    const Toast = Swal.mixin({
                        toast: true,
                        position: "top-end",
                        showConfirmButton: false,
                        timer: 2000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                            toast.onmouseenter = Swal.stopTimer;
                            toast.onmouseleave = Swal.resumeTimer;
                        }
                    });
                    Toast.fire({
                        icon: "success",
                        title: "Поставщик успешно удален."
                    });
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        text: 'Ошибка при удалении поставщика',
                        confirmButtonColor: '#67a2d5',
                    });
                }
            });
        }
    });
}

