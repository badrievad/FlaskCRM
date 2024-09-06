document.getElementById('merge-deals-button').addEventListener('click', async function () {
    // Ждем выполнения getSelectedDeals и получения массива сделок
    var selectedDeals = await getSelectedDeals();

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
                },
                error: function (xhr, status, error) {
                    var response = JSON.parse(xhr.responseText);
                    Swal.fire({
                        icon: 'error',
                        title: 'Ошибка',
                        text: 'Ошибка при объединении сделок: ' + response.message,
                        confirmButtonText: 'ОК',
                        confirmButtonColor: '#7892ad',
                    });
                    console.error('Ошибка при объединении сделок:', response.message);
                }
            });
        }
    });
});


async function toggleCheckbox(dealId, event) {
    // Останавливаем всплытие события для предотвращения клика на строке
    event.stopPropagation();

    // Проверка: если клик был по самому чекбоксу, не меняем состояние чекбокса вручную
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
    try {
        var selectedDeals = await getSelectedDeals();  // Ждём выполнения async функции

        if (canMergeDeals(selectedDeals)) {
            document.getElementById('merge-deals-button').disabled = false;
        } else {
            document.getElementById('merge-deals-button').disabled = true;
        }
    } catch (error) {
        console.error('Ошибка при получении сделок:', error);
    }
}


async function getSelectedDeals() {
    var selectedDeals = [];

    // Асинхронный цикл для обработки всех чекбоксов
    for (let checkbox of document.querySelectorAll('.deal-checkbox:checked')) {
        var dealId = checkbox.dataset.dealId;
        var company = checkbox.closest('tr').querySelector('.deal-title').textContent.trim();
        var manager = checkbox.closest('tr').querySelector('.deal-manager').textContent.trim();

        // Проверяем, есть ли у сделки group_id
        let response = await fetch(`/crm/deals/group/${dealId}`);
        let data = await response.json();

        if (data.group_id) {
            // Если у сделки есть group_id, добавляем все сделки в этой группе
            data.deals.forEach(deal => {
                // Проверяем, что сделка ещё не добавлена
                if (!selectedDeals.some(d => d.id === deal.id)) {
                    selectedDeals.push({
                        id: deal.id,
                        company: deal.company || company,  // Используем компанию из ответа
                        manager: deal.manager || manager   // Используем менеджера из ответа
                    });
                }
            });
        } else {
            // Если group_id нет, добавляем только эту сделку
            selectedDeals.push({
                id: dealId,
                company: company,
                manager: manager
            });
        }
    }

    return selectedDeals;
}


function canMergeDeals(deals) {
    if (!Array.isArray(deals) || deals.length === 0) {
        return false; // Если массив сделок пустой или не является массивом
    }

    // Проверка: если выбрано меньше 2 чекбоксов, то нельзя объединить
    const checkedCheckboxes = document.querySelectorAll('.deal-checkbox:checked').length;
    if (checkedCheckboxes < 2) {
        return false;
    }

    const firstDealCompany = deals[0].company;
    const firstDealManager = deals[0].manager;

    // Проверяем, что все выбранные сделки принадлежат одной компании и менеджеру
    const canMerge = deals.every(deal => deal.company === firstDealCompany && deal.manager === firstDealManager);

    return canMerge;
}

