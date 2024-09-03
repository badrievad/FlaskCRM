const userIcon = document.getElementById('user-icon');
const userDropdown = document.getElementById('user-dropdown');
let selectedUser = null;
let activeElement = null; // Переменная для хранения активного элемента
let userItems = []; // Массив для хранения всех элементов пользователей
let currentIndex = -1; // Индекс текущего выбранного пользователя

userIcon.addEventListener('click', function () {
    // Очистка списка перед добавлением новых элементов
    userDropdown.innerHTML = '';
    userItems = [];
    currentIndex = -1;

    const currentCreatedBy = document.getElementById('current-created-by').getAttribute('data-user-id'); // Получаем текущего ответственного пользователя

    // Отправка AJAX-запроса на сервер для получения пользователей
    $.ajax({
        url: './get-managers-and-admins',
        method: 'GET',
        data: {current_user_id: currentCreatedBy},  // Передаем ID текущего ответственного пользователя
        success: function (data) {
            // Обработка полученных данных и добавление пользователей в список
            data.forEach((user, index) => {
                const userItem = document.createElement('p');
                userItem.textContent = user.name;
                userItem.style.margin = '0';
                userItem.style.padding = '8px';
                userItem.style.cursor = 'pointer';

                // Добавить обработчик клика по пользователю
                userItem.addEventListener('click', function () {
                    setActiveUser(index);
                });

                userDropdown.appendChild(userItem);
                userItems.push(userItem); // Сохраняем элемент в массив
            });

            // Добавление кнопок "Сохранить" и "Отменить"
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Сохранить';
            saveButton.className = 'save-button'; // Добавляем класс
            saveButton.addEventListener('click', saveSelection);

            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Отменить';
            cancelButton.className = 'cancel-button'; // Добавляем класс
            cancelButton.addEventListener('click', cancelSelection);

            userDropdown.appendChild(saveButton);
            userDropdown.appendChild(cancelButton);

            // Показать dropdown
            userDropdown.style.display = 'block';

            // Фокусируем на первом элементе, если список не пуст
            if (userItems.length > 0) {
                setActiveUser(0);
            }
        },
        error: function (error) {
            console.error('Ошибка при получении данных:', error);
        }
    });
});

// Функция для установки активного пользователя
function setActiveUser(index) {
    if (activeElement) {
        activeElement.classList.remove('active');
    }
    currentIndex = index;
    activeElement = userItems[currentIndex];
    selectedUser = activeElement.textContent;
    activeElement.classList.add('active');
}

// Функция для сохранения выбора
function saveSelection() {
    const path = window.location.pathname;
    const dealId = path.split('/').pop();
    if (selectedUser) {
        // Подтверждение передачи прав
        const isConfirmed = confirm(`Вы точно хотите передать права новому пользователю: ${selectedUser}? У вас больше не будет возможности вносить изменения в сделку`);

        if (!isConfirmed) {
            return; // Если пользователь нажал "Cancel", прерываем выполнение функции
        }

        $.ajax({
            url: `./update-created-by/${dealId}`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({created_by: selectedUser}),
            success: function (response) {
                console.log(response.message);
                userDropdown.style.display = 'none'; // Закрыть dropdown

                // Обновляем текст текущего ответственного
                document.getElementById('current-created-by').textContent = selectedUser;

                // Перезагружаем страницу через небольшую задержку
                setTimeout(function () {
                    window.location.reload();
                }, 2000); // Задержка в 2 секунды перед перезагрузкой

            },
            error: function (error) {
                console.error('Ошибка при обновлении данных:', error);
                showError("Произошла ошибка при обновлении данных", "Ошибка");
            }
        });
    } else {
        alert('Пожалуйста, выберите пользователя.');
    }
}

// Функция для отмены выбора
function cancelSelection() {
    console.log('Отменено');
    userDropdown.style.display = 'none'; // Закрыть dropdown
}

// Обработчик событий клавиатуры
document.addEventListener('keydown', function (event) {
    if (userDropdown.style.display === 'block') {
        switch (event.key) {
            case 'ArrowDown':
                if (currentIndex < userItems.length - 1) {
                    setActiveUser(currentIndex + 1);
                }
                break;
            case 'ArrowUp':
                if (currentIndex > 0) {
                    setActiveUser(currentIndex - 1);
                }
                break;
            case 'Enter':
                saveSelection();
                break;
            case 'Escape':
                cancelSelection();
                break;
        }
    }
});

// Закрытие dropdown при клике вне его
document.addEventListener('click', function (event) {
    if (!userDropdown.contains(event.target) && event.target !== userIcon) {
        userDropdown.style.display = 'none';
    }
});

function showSuccess(message, title) {
    toastr.options = {
        closeButton: true,
        debug: false,
        newestOnTop: false,
        progressBar: true,
        positionClass: "toast-bottom-right",
        preventDuplicates: false,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "5000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    };
    toastr.success(message, title);
}

function showError(message, title) {
    toastr.options = {
        closeButton: true,
        debug: false,
        newestOnTop: false,
        progressBar: true,
        positionClass: "toast-bottom-right",
        preventDuplicates: false,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "6000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    };
    toastr.error(message, title);
}

function showInfo(message, title) {
    toastr.options = {
        closeButton: true,
        debug: false,
        newestOnTop: false,
        progressBar: true,
        positionClass: "toast-bottom-right",
        preventDuplicates: false,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "2000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    };
    toastr.info(message, title);
}

// Редактирование названия поставщика
document.getElementById('edit-supplier-name-icon').addEventListener('click', function () {
    var nameDisplay = document.getElementById('supplier-name-display');
    var nameInput = document.getElementById('supplier-name-input');
    var saveButton = document.getElementById('save-supplier-name');
    var cancelButton = document.getElementById('cancel-supplier-name');
    var editIcon = document.getElementById('edit-supplier-name-icon');

    nameDisplay.style.display = 'none';
    nameInput.style.display = 'inline';
    nameInput.focus();
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';
    editIcon.style.display = 'none'; // Скрываем иконку

    // Обработчик клавиш на поле ввода
    nameInput.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            cancelEditingName();
        } else if (event.key === 'Enter') {
            saveEditingName();
        }
    });
});

// Редактирование ИНН поставщика
document.getElementById('edit-supplier-inn-icon').addEventListener('click', function () {
    var innDisplay = document.getElementById('supplier-inn-display');
    var innInput = document.getElementById('supplier-inn-input');
    var saveButton = document.getElementById('save-supplier-inn');
    var cancelButton = document.getElementById('cancel-supplier-inn');
    var editIcon = document.getElementById('edit-supplier-inn-icon');

    innDisplay.style.display = 'none';
    innInput.style.display = 'inline';
    innInput.focus();
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';
    editIcon.style.display = 'none'; // Скрываем иконку

    // Обработчик клавиш на поле ввода
    innInput.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            cancelEditingInn();
        } else if (event.key === 'Enter') {
            saveEditingInn();
        }
    });
});

// Кнопка "Отменить" для имени поставщика
document.getElementById('cancel-supplier-name').addEventListener('click', cancelEditingName);

// Кнопка "Сохранить" для имени поставщика
document.getElementById('save-supplier-name').addEventListener('click', saveEditingName);

// Кнопка "Отменить" для ИНН поставщика
document.getElementById('cancel-supplier-inn').addEventListener('click', cancelEditingInn);

// Кнопка "Сохранить" для ИНН поставщика
document.getElementById('save-supplier-inn').addEventListener('click', saveEditingInn);

// Функции для отмены редактирования
function cancelEditingName() {
    var editIcon = document.getElementById('edit-supplier-name-icon');
    document.getElementById('supplier-name-display').style.display = 'inline';
    document.getElementById('supplier-name-input').style.display = 'none';
    document.getElementById('save-supplier-name').style.display = 'none';
    document.getElementById('cancel-supplier-name').style.display = 'none';
    editIcon.style.display = 'inline'; // Показываем иконку
}

function cancelEditingInn() {
    var editIcon = document.getElementById('edit-supplier-inn-icon');
    document.getElementById('supplier-inn-display').style.display = 'inline';
    document.getElementById('supplier-inn-input').style.display = 'none';
    document.getElementById('save-supplier-inn').style.display = 'none';
    document.getElementById('cancel-supplier-inn').style.display = 'none';
    editIcon.style.display = 'inline'; // Показываем иконку
}

// Функции для сохранения редактирования
function saveEditingName() {
    var newName = document.getElementById('supplier-name-input').value;
    var editIcon = document.getElementById('edit-supplier-name-icon');
    document.getElementById('supplier-name-display').textContent = newName;
    cancelEditingName();
    editIcon.style.display = 'inline'; // Показываем иконку
    // Здесь можно добавить AJAX-запрос для сохранения изменений на сервере
}

function saveEditingInn() {
    var newInn = document.getElementById('supplier-inn-input').value;
    var editIcon = document.getElementById('edit-supplier-inn-icon');
    document.getElementById('supplier-inn-display').textContent = newInn;
    cancelEditingInn();
    editIcon.style.display = 'inline'; // Показываем иконку
    // Здесь можно добавить AJAX-запрос для сохранения изменений на сервере
}


