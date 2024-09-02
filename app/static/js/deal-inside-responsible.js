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

    // Отправка AJAX-запроса на сервер для получения пользователей
    $.ajax({
        url: './get-managers-and-admins',
        method: 'GET',
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

                // Уведомление об успешном обновлении
                showInfo("Ответственный успешно обновлен");
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
        timeOut: "4000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    };
    toastr.info(message, title);
}