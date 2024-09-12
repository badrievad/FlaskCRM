document.getElementById('merge-deals-button').addEventListener('click', async function () {
    var selectedDeals = await getSelectedDeals();  // Получаем выбранные сделки

    if (selectedDeals.length < 2) {
        Swal.fire({
            icon: 'warning',
            title: 'Недостаточно сделок',
            text: 'Выберите как минимум 2 сделки для объединения',
            confirmButtonText: 'ОК',
            confirmButtonColor: '#67a2d5',
        });
        return;  // Если выбрано меньше 2 сделок, не продолжаем выполнение
    }

    var dealIds = selectedDeals.map(deal => deal.id);  // Извлекаем только ID сделок

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
            // Выполняем AJAX-запрос к вашему роуту
            $.ajax({
                url: '/crm/deals/merge-deals',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({deals: dealIds}),
                success: function (response) {
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
                        title: "Сделки успешно объединены"
                    }).then(() => {
                        // После успешного уведомления перезагружаем страницу
                        updateDealsTable();
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

// Функция для проверки состояния кнопки "Объединить сделки"
async function checkSelectedDeals() {
    var selectedDeals = await getSelectedDeals();
    document.getElementById('merge-deals-button').disabled = !canMergeDeals(selectedDeals);
}

// Функция для управления состоянием чекбоксов и объединения сделок
async function toggleCheckbox(dealId, event) {
    // Останавливаем всплытие события для предотвращения клика на строке
    event.stopPropagation();

    // Если клик был по самому чекбоксу, позволим браузеру обработать событие
    if (event.target.tagName === 'INPUT' && event.target.type === 'checkbox') {
        // Просто вызываем проверку состояния после обработки клика браузером
        await checkSelectedDeals();
        return; // Выход из функции, так как мы не хотим переключать чекбокс вручную
    }

    // Переключаем состояние чекбокса вручную, если клик был не по чекбоксу
    var checkbox = document.getElementById(`checkbox-${dealId}`);
    checkbox.checked = !checkbox.checked;

    // Проверяем состояние кнопки
    await checkSelectedDeals();
}

// Функция для обновления таблицы сделок
function updateDealsTable() {
    fetch('/crm/deals/active')
        .then(response => response.json())
        .then(data => {
            var dealsList = document.getElementById('deal-rows');
            dealsList.innerHTML = ''; // Очищаем существующие строки

            data.deals.forEach((deal, index) => {
                var dealItem = `
                    <tr id="deal-${deal.id}" onclick="enterIntoDeal(${deal.id})">
                        <td onclick="toggleCheckbox(${deal.id}, event)">
                            <input type="checkbox" class="deal-checkbox" data-deal-id="${deal.id}" id="checkbox-${deal.id}" style="cursor: pointer;">
                        </td>
                        <td>${index + 1}</td>
                        <td class="deal-dl">${deal.dl_number}</td>
                        <td class="deal-title">${deal.title}</td>
                        <td class="deal-product">${deal.product}</td>
                        <td class="deal-manager">${deal.created_by}</td>
                        <td class="deal-created">${new Date(deal.created_at).toLocaleString()}</td>
                        <td>
                            <div class="btn-container">
                                <button class="icon-button" onclick="event.stopPropagation(); confirmArchive(${deal.id})">
                                    <i class="fa-regular fa-square-minus"></i>
                                </button>
                            </div>
                        </td>
                    </tr>`;
                dealsList.insertAdjacentHTML('beforeend', dealItem);
            });

            // После перерисовки таблицы заново прикрепляем события для чекбоксов
            attachCheckboxEvents();
            checkSelectedDeals();  // Проверяем состояние кнопки после обновления таблицы
        })
        .catch(error => {
            console.error('Ошибка при получении сделок:', error);
        });
}

// Функция для привязки событий к чекбоксам
function attachCheckboxEvents() {
    document.querySelectorAll('.deal-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', async function (event) {
            await checkSelectedDeals();  // Проверяем состояние кнопки при изменении чекбокса
        });
    });
}

// Проверка и активация кнопки при загрузке
document.addEventListener('DOMContentLoaded', function () {
    attachCheckboxEvents();
    checkSelectedDeals();  // Проверяем состояние кнопки после загрузки страницы
});



