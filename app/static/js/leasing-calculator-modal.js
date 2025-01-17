// Функция для получения активных сделок
function fetchActiveDeals(userFullname, selectElementId, dealId) {
    return fetch(`/crm/deals/active-for-bind?user_fullname=${encodeURIComponent(userFullname)}`)
        .then(response => response.json())
        .then(data => {
            // Обработка данных после получения ответа
            updateSelectElement(data.deals, selectElementId, dealId);
        })
        .catch(error => {
            console.error('Error fetching deals:', error);
        });
}

function updateSelectElement(deals, selectElementId, dealId) {
    var selectElement = document.getElementById(selectElementId);
    selectElement.innerHTML = ""; // Очищаем текущее содержимое

    // Добавляем опцию "" в начале
    var defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.text = "";
    selectElement.appendChild(defaultOption);

    // Добавляем остальные опции
    deals.forEach(deal => {
        var option = document.createElement("option");
        option.value = deal.id;
        // Используем тернарный оператор для проверки наличия leas_calc
        option.text = deal.leas_calc ?
            "ДЛ " + deal.dl_number + " | " + deal.title + " " + deal.leas_calc :
            "!ДЛ " + deal.dl_number + " | " + deal.title + " " + deal.leas_calc;

        // Если option.value равно переданному dealId, делаем его selected
        if (option.value == dealId) {
            option.selected = true;
        }

        selectElement.appendChild(option);
    });
}


function openModal(name, date, itemPrice, itemType, itemDeal, calcId, userFullName, dealId) {
    fetchActiveDeals(userFullName, 'item-deal-modal-select', dealId);

    var modalContent = `
                            <table class="modal-table" id="modal-table" data-calc-id="${calcId}">
                                <tr>
                                    <th>Наименование ПЛ</th>
                                    <td>
                                        <span id="item-name-modal">${name}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Дата</th>
                                    <td>${date}</td>
                                </tr>
                                <tr>
                                    <th>Цена ПЛ</th>
                                    <td>
                                        <span id="item-price-modal">${itemPrice}</span> руб.
                                    </td>
                                </tr>
                                <tr>
                                    <th>Тип ПЛ</th>
                                    <td>
                                        <span id="item-type-modal">${itemType}</span>
                                        <select id="item-type-modal-select" class="hidden item-type-modal-select">
                                            <option value="Легковые" ${itemType === 'Легковые' ? 'selected' : ''}>Легковые</option>
                                            <option value="Грузовые и прицепы" ${itemType === 'Грузовые и прицепы' ? 'selected' : ''}>Грузовые и прицепы</option>
                                            <option value="Оборудование" ${itemType === 'Оборудование' ? 'selected' : ''}>Оборудование</option>
                                            <option value="Спецтехника" ${itemType === 'Спецтехника' ? 'selected' : ''}>Спецтехника</option>
                                            <option value="Автобусы" ${itemType === 'Автобусы' ? 'selected' : ''}>Автобусы</option>
                                            <option value="Недвижимость" ${itemType === 'Недвижимость' ? 'selected' : ''}>Недвижимость</option>
                                        </select>
                                        <i class="fa-regular fa-pen-to-square" onclick="makeEditable('item-type-modal', true)"></i>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Привязать к сделке</th>
                                    <td>
                                        <span id="item-deal-modal">${itemDeal}</span>
                                        <select id="item-deal-modal-select" class="hidden item-deal-modal-select">
                                        </select>
                                        <i class="fa-regular fa-pen-to-square" onclick="makeEditable('item-deal-modal', true)"></i>
                                    </td>
                                </tr>
                            </table>
                        `;

    document.querySelector('.modal-body').innerHTML = modalContent;

    var modal = document.getElementById('modal');
    modal.style.display = "block";
    document.getElementById('item-type-modal-select').value = itemType;
    document.getElementById('item-deal-modal-select').value = itemDeal;
}


function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Закрыть модальное окно при нажатии клавиши ESC
document.addEventListener('keydown', function (event) {
    var modal = document.getElementById('modal');
    if (event.key === "Escape" && modal.style.display === "block") {
        closeModal();
    }
});

// Когда пользователь нажимает в любом месте вне модального окна, увеличить и уменьшить его
window.onclick = function (event) {
    var modal = document.getElementById('modal');
    var modalContent = document.querySelector('.modal-content');
    if (event.target == modal) {
        modalContent.classList.add('modal-shake');
        setTimeout(() => {
            modalContent.classList.remove('modal-shake');
        }, 300);
    }
}

function makeEditable(id, isSelect = false) {
    if (isSelect) {
        var span = document.getElementById(id);
        var select = document.getElementById(id + '-select');
        span.classList.add('hidden');
        select.classList.remove('hidden');
        select.focus();
    } else {
        var element = document.getElementById(id);
        element.contentEditable = true;
        element.classList.add('editable');
        element.focus();
    }
}

function toggleButtons(disabled) {
    const buttons = document.querySelectorAll('.copy-btn, .save-btn, .close-btn');

    buttons.forEach(button => {
        button.disabled = disabled;
        if (disabled) {
            button.classList.add('disabled');
        } else {
            button.classList.remove('disabled');
        }
    });
}

function saveChanges(userFullName) {
    // Блокируем кнопки перед началом операции
    toggleButtons(true);

    var dealId = document.getElementById('item-deal-modal-select').value;
    var dealText = dealId ? document.getElementById('item-deal-modal-select').options[document.getElementById('item-deal-modal-select').selectedIndex].text : '';

    var data = {
        item_name: document.getElementById('item-name-modal').innerText,
        item_type: document.getElementById('item-type-modal-select').value || document.getElementById('item-type-modal').innerText,
        deal_id: dealId,
        deal_text: dealText  // Сохраняем текст сделки только если deal_id не пустой
    };

    var calcId = document.getElementById('modal-table').getAttribute('data-calc-id');

    // Вместо стандартного confirm используем SweetAlert2
    Swal.fire({
        text: 'Вы уверены, что хотите сохранить изменения?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#5182ad',
        cancelButtonColor: '#ad6c72',
        confirmButtonText: 'Да, сохранить',
        cancelButtonText: 'Отменить'
    }).then((result) => {
        if (result.isConfirmed) {
            // Если пользователь подтвердил действие
            fetch(`/crm/calculator/update/${calcId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            }).then(response => response.json())
                .then(responseData => {
                    if (responseData.success) {
                        updateTableRow(calcId, responseData.data, userFullName, data.deal_id, data.deal_text);
                        closeModal(); // Закрываем модальное окно после сохранения
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
                            title: "Данные успешно обновлены."
                        });
                    } else {
                        showError(responseData.message, "Ошибка сохранения изменений:");
                    }
                }).catch(error => console.error('Error:', error))
                .finally(() => {
                    // Разблокируем кнопки после завершения операции
                    toggleButtons(false);
                });
        } else {
            // Разблокируем кнопки, если пользователь отменил действие
            toggleButtons(false);
        }
    });
}


function updateTableRow(calcId, updatedData, userFullName, dealId, dealText) {
    // Находим строку таблицы по calcId
    var row = document.querySelector(`tr[data-id="${calcId}"]`);
    if (row) {
        // Сохраняем dealText в атрибуте данных строки таблицы
        var itemNameElement = row.querySelector('.item-name');
        if (itemNameElement) {
            itemNameElement.innerText = updatedData.item_name;
        }

        // Обновляем цену предмета
        var itemPriceElement = row.querySelector('.item-price');
        if (itemPriceElement) {
            itemPriceElement.innerText = updatedData.item_price;
        }

        // Обновляем тип предмета
        var itemTypeElement = row.querySelector('.item-type');
        if (itemTypeElement) {
            itemTypeElement.innerText = updatedData.item_type;
        }

        // Обновляем иконку сделки
        var dealIconElement = row.querySelector('td i.fa-link, td i.fa-unlink');
        if (dealIconElement) {

            if (dealId) {
                // Если есть dealId, используем иконку fa-link
                dealIconElement.className = 'fa-solid fa-link';
                dealIconElement.id = 'fa-link'; // Меняем id на fa-link

            } else {
                // Если dealId нет, используем иконку fa-unlink
                dealIconElement.className = 'fa-solid fa-unlink';
                dealIconElement.id = 'fa-unlink'; // Меняем id на fa-unlink
                showInfo("", "КП не привязано к сделке");
            }
        }

        // Обновляем атрибут onclick в строке
        row.setAttribute('onclick', `openModal('${updatedData.item_name}', '${updatedData.date_ru}', '${updatedData.item_price}', '${updatedData.item_type}', '${dealText}', '${calcId}', '${userFullName}', '${dealId}')`);
        row.setAttribute('data-deal-text', dealText.replace("(КП подвязано)", ""));
    }
}


// Инициализация тултипов при загрузке страницы
function initializeTooltips() {
    const dealIconElements = document.querySelectorAll('i.fa-link, i.fa-unlink');

    dealIconElements.forEach(dealIconElement => {
        var dealText = dealIconElement.closest('tr').getAttribute('data-deal-text') || '';

        if (dealIconElement.id === 'fa-link') {
        } else if (dealIconElement.id === 'fa-unlink') {
        }
    });
}

document.addEventListener("DOMContentLoaded", initializeTooltips);

