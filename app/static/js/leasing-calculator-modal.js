function openModal(name, date, itemPrice, itemType, itemDeal, calcId) {
    var modalTable = document.getElementById('modal-table');

    var modalContent = `
                            <table class="modal-table" id="modal-table" data-calc-id="${calcId}">
                                <tr>
                                    <th>Наименование ПЛ</th>
                                    <td>
                                        <span id="item-name-modal">${name}</span>
                                        <i class="fa-regular fa-pen-to-square" onclick="makeEditable('item-name-modal')"></i>
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
                                        <select id="item-type-modal-select" class="hidden">
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
                                        <i class="fa-regular fa-pen-to-square" onclick="makeEditable('item-deal-modal')"></i>
                                    </td>
                                </tr>
                            </table>
                        `;

    document.querySelector('.modal-body').innerHTML = modalContent;

    var modal = document.getElementById('modal');
    modal.style.display = "block";
    document.getElementById('item-type-modal-select').value = itemType;
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

function saveChanges() {
    var data = {
        item_name: document.getElementById('item-name-modal').innerText,
        item_type: document.getElementById('item-type-modal-select').value || document.getElementById('item-type-modal').innerText,
        deal_id: document.getElementById('item-deal-modal').innerText
    };

    var calcId = document.getElementById('modal-table').getAttribute('data-calc-id');
    // Удаляем поле deal_id, если его значение "-"
    if (data.deal_id === "-") {
        delete data.deal_id;
    }
    console.log(data);
    if (confirm('Вы уверены, что хотите сохранить изменения?')) {
        fetch(`/crm/calculator/update/${calcId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }).then(response => response.json())
            .then(responseData => {
                if (responseData.success) {
                    updateTableRow(calcId, responseData.data);
                    closeModal(); // Закрываем модальное окно после сохранения
                } else {
                    alert('Ошибка сохранения изменений: ' + responseData.message);
                }
            }).catch(error => console.error('Error:', error));
    }
}

function updateTableRow(calcId, updatedData) {
    var row = document.querySelector(`tr[data-id="${calcId}"]`);
    if (row) {
        row.querySelector('.item-name').innerText = updatedData.item_name;
        row.querySelector('.item-price').innerText = updatedData.item_price;
        row.querySelector('.item-type').innerText = updatedData.item_type;
        row.querySelector('.date-ru').innerText = updatedData.date_ru;

        // Обновление атрибута onclick в строке
        row.setAttribute('onclick', `openModal('${updatedData.item_name}', '${updatedData.date_ru}', '${updatedData.item_price}', '${updatedData.item_type}', '-', '${calcId}')`);
    }
}