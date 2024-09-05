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
        // Вместо стандартного confirm используем SweetAlert2
        Swal.fire({
            text: `Вы точно хотите передать права новому пользователю: ${selectedUser}? У вас больше не будет возможности вносить изменения в сделку.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#67a2d5',
            cancelButtonColor: '#ad6c72',
            confirmButtonText: 'Да, передать права',
            cancelButtonText: 'Отменить'
        }).then((result) => {
            if (result.isConfirmed) {
                // Если пользователь подтвердил действие
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
            }
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: 'Ошибка',
            text: 'Пожалуйста, выберите пользователя.',
            confirmButtonText: 'ОК'
        });
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

// Редактирование информации о поставщике
document.getElementById('edit-name-icon').addEventListener('click', function () {
    var nameDisplay = document.getElementById('supplier-name-display');
    var nameInput = document.getElementById('supplier-name-input');
    var innDisplay = document.getElementById('supplier-inn-display');
    var innInput = document.getElementById('supplier-inn-input');
    var saveButton = document.getElementById('save-supplier');
    var cancelButton = document.getElementById('cancel-supplier');
    var editIcon = document.getElementById('edit-name-icon');

    // Скрываем отображение текста и показываем поля ввода
    nameDisplay.style.display = 'none';
    nameInput.style.display = 'inline';
    innDisplay.style.display = 'none';
    innInput.style.display = 'inline';

    // Скрываем иконку редактирования и показываем кнопки
    editIcon.style.display = 'none';
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';

    // Фокусируемся на первом поле ввода
    nameInput.focus();

    // Обработчик клавиш на полях ввода
    nameInput.addEventListener('keydown', handleKeyEvents);
    innInput.addEventListener('keydown', handleKeyEvents);
});

// Обработчик для кнопки "Отменить"
document.getElementById('cancel-supplier').addEventListener('click', cancelEditing);

// Обработчик для кнопки "Сохранить"
document.getElementById('save-supplier').addEventListener('click', saveEditing);

// Функции для отмены редактирования
function cancelEditing() {
    var nameDisplay = document.getElementById('supplier-name-display');
    var nameInput = document.getElementById('supplier-name-input');
    var innDisplay = document.getElementById('supplier-inn-display');
    var innInput = document.getElementById('supplier-inn-input');
    var saveButton = document.getElementById('save-supplier');
    var cancelButton = document.getElementById('cancel-supplier');
    var editIcon = document.getElementById('edit-name-icon');

    // Восстанавливаем исходное состояние
    nameDisplay.style.display = 'inline';
    nameInput.style.display = 'none';
    innDisplay.style.display = 'inline';
    innInput.style.display = 'none';

    // Скрываем кнопки и возвращаем иконку редактирования
    saveButton.style.display = 'none';
    cancelButton.style.display = 'none';
    editIcon.style.display = 'inline';
}

// Функции для сохранения редактирования
function saveEditing() {
    var newName = document.getElementById('supplier-name-input').value.trim();
    var newInn = document.getElementById('supplier-inn-input').value.trim();
    var nameDisplay = document.getElementById('supplier-name-display');
    var innDisplay = document.getElementById('supplier-inn-display');
    var dealId = getDealIdFromUrl();  // Извлекаем ID сделки из URL

    // Проверка на пустое имя
    if (!newName) {
        alert('Введите корректное наименование поставщика.');
        return;
    }

    // Проверка длины ИНН
    if (newInn.length !== 10 && newInn.length !== 12) {
        alert('ИНН должен содержать 10 или 12 символов.');
        return;
    }

    // Проверка, что ИНН состоит только из цифр
    if (!/^\d+$/.test(newInn)) {
        alert('ИНН должен содержать только цифры.');
        return;
    }

    // Обновляем отображаемые значения
    nameDisplay.textContent = newName;
    innDisplay.textContent = newInn;

    // Скрываем поля ввода и кнопки, возвращаем текст и иконку
    cancelEditing();

    // AJAX-запрос для сохранения изменений на сервере
    $.ajax({
        url: '/crm/calculator/update-seller',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            title: newName,
            inn: newInn,
            deal_id: dealId
        }),
        success: function (response) {
            console.log(response.message); // Выводим сообщение об успешном обновлении
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при обновлении данных продавца:', xhr.responseText);
        }
    });
}


// Обработчик для клавиш ESC и Enter
function handleKeyEvents(event) {
    if (event.key === 'Escape') {
        cancelEditing();
    } else if (event.key === 'Enter') {
        saveEditing();
    }
}

function getDealIdFromUrl() {
    // Получаем путь URL
    var path = window.location.pathname;

    // Разбиваем путь на сегменты и возвращаем последний элемент (ID)
    var segments = path.split('/');
    return segments[segments.length - 1];  // Возвращает ID (в вашем случае 613)
}



