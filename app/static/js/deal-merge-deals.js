document.getElementById('merge-deals-button').addEventListener('click', function () {
    var selectedDeals = getSelectedDeals();

    if (selectedDeals.length < 2) {
        Swal.fire({
            icon: 'warning',
            title: 'Недостаточно сделок',
            text: 'Выберите как минимум 2 сделки для объединения',
            confirmButtonText: 'ОК'
        });
        return; // Если выбрано меньше 2 сделок, не продолжаем выполнение
    }

    // Извлекаем только ID сделок из массива объектов
    var dealIds = selectedDeals.map(deal => deal.id);

    // Используем SweetAlert2 для подтверждения действия
    Swal.fire({
        text: `Вы действительно хотите объединить ${selectedDeals.length} сделки?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#67a2d5',
        cancelButtonColor: '#ad6c72',
        confirmButtonText: 'Да, объединить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            // Если пользователь подтвердил, выполняем AJAX-запрос
            $.ajax({
                url: '/crm/deals/merge-deals',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    deals: dealIds // Отправляем только идентификаторы сделок
                }),
                success: function (response) {
                    // Обновляем таблицу
                    Swal.fire({
                        icon: 'success',
                        text: 'Сделки успешно объединены',
                        timer: 1000,
                        width: 400,
                        showConfirmButton: false,
                    });
                    console.log(response.message);
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Ошибка',
                        text: 'Ошибка при объединении сделок: ' + xhr.responseText,
                        confirmButtonText: 'ОК'
                    });
                    console.error('Ошибка при объединении сделок:', xhr.responseText);
                }
            });
        }
    });
});


function toggleCheckbox(dealId, event) {
    // Останавливаем всплытие события для предотвращения клика на строке
    event.stopPropagation();

    // Проверка: если клик был по самому чекбоксу, не меняем состояние чекбокса вручную,
    // но продолжаем проверку состояния кнопки
    if (event.target.tagName === 'INPUT' && event.target.type === 'checkbox') {
        // Чекбокс уже переключается самим браузером, мы просто продолжаем
        // проверку состояния после клика
    } else {
        // Получаем сам чекбокс
        var checkbox = document.getElementById(`checkbox-${dealId}`);
        // Переключаем состояние чекбокса вручную, если клик был не по самому чекбоксу
        checkbox.checked = !checkbox.checked;
    }

    // Проверяем, можно ли объединять сделки после изменения состояния чекбокса
    var selectedDeals = getSelectedDeals();

    if (canMergeDeals(selectedDeals)) {
        document.getElementById('merge-deals-button').disabled = false;
    } else {
        document.getElementById('merge-deals-button').disabled = true;
    }
}


function getSelectedDeals() {
    var selectedDeals = [];
    document.querySelectorAll('.deal-checkbox:checked').forEach(checkbox => {
        selectedDeals.push({
            id: checkbox.dataset.dealId,
            company: checkbox.closest('tr').querySelector('.deal-title').textContent.trim(),
            manager: checkbox.closest('tr').querySelector('.deal-manager').textContent.trim()
        });
    });
    return selectedDeals;
}


function canMergeDeals(deals) {
    if (deals.length < 2) {
        return false; // Нужно минимум 2 сделки для объединения
    }

    const firstDealCompany = deals[0].company;
    const firstDealManager = deals[0].manager;

    // Проверяем, что все выбранные сделки принадлежат одной компании и менеджеру
    const canMerge = deals.every(deal => deal.company === firstDealCompany && deal.manager === firstDealManager);

    if (!canMerge) {
    }

    return canMerge;
}
