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

// Используем делегирование событий для иконки редактирования
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('edit-name-icon')) {
        var index = event.target.getAttribute('data-index');
        toggleEditMode(index, true);
    }
});

// Обработчик для кнопки "Сохранить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('save-supplier')) {
        var index = event.target.getAttribute('data-index');
        saveEditing(index);
    }
});

// Обработчик для кнопки "Отменить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('cancel-supplier')) {
        var index = event.target.getAttribute('data-index');
        toggleEditMode(index, false);
    }
});

// Функция переключения режима редактирования
function toggleEditMode(index, isEditing) {
    var nameDisplay = document.getElementById(`supplier-name-display-${index}`);
    var nameInput = document.getElementById(`supplier-name-input-${index}`);
    var innDisplay = document.getElementById(`supplier-inn-display-${index}`);
    var innInput = document.getElementById(`supplier-inn-input-${index}`);
    var addressDisplay = document.getElementById(`supplier-address-display-${index}`);
    var addressInput = document.getElementById(`supplier-address-input-${index}`);
    var phoneDisplay = document.getElementById(`supplier-phone-display-${index}`);
    var phoneInput = document.getElementById(`supplier-phone-input-${index}`);
    var emailDisplay = document.getElementById(`supplier-email-display-${index}`);
    var emailInput = document.getElementById(`supplier-email-input-${index}`);
    var signerDisplay = document.getElementById(`supplier-signer-display-${index}`);
    var signerInput = document.getElementById(`supplier-signer-input-${index}`);
    var saveButton = document.getElementById(`save-supplier-${index}`);
    var cancelButton = document.getElementById(`cancel-supplier-${index}`);
    var editIcon = document.getElementById(`edit-name-icon-${index}`);
    var deleteIcon = document.getElementById(`edit-delete-icon-${index}`);

    if (isEditing) {
        // Включаем режим редактирования
        nameDisplay.style.display = 'none';
        nameInput.style.display = 'inline';
        innDisplay.style.display = 'none';
        innInput.style.display = 'inline';
        addressDisplay.style.display = 'none';
        addressInput.style.display = 'inline';
        phoneDisplay.style.display = 'none';
        phoneInput.style.display = 'inline';
        emailDisplay.style.display = 'none';
        emailInput.style.display = 'inline';
        signerDisplay.style.display = 'none';
        signerInput.style.display = 'inline';
        editIcon.style.display = 'none';
        if (deleteIcon) {  // Проверяем, существует ли элемент
            deleteIcon.style.display = 'none';  // Скрыть
        }
        saveButton.style.display = 'inline-block';
        cancelButton.style.display = 'inline-block';
        nameInput.focus();
    } else {
        // Выключаем режим редактирования
        nameDisplay.style.display = 'inline';
        nameInput.style.display = 'none';
        innDisplay.style.display = 'inline';
        innInput.style.display = 'none';
        addressDisplay.style.display = 'inline';
        addressInput.style.display = 'none';
        phoneDisplay.style.display = 'inline';
        phoneInput.style.display = 'none';
        emailDisplay.style.display = 'inline';
        emailInput.style.display = 'none';
        signerDisplay.style.display = 'inline';
        signerInput.style.display = 'none';
        editIcon.style.display = 'inline';
        if (deleteIcon) {  // Проверяем, существует ли элемент
            deleteIcon.style.display = 'inline';  // Скрыть
        }
        saveButton.style.display = 'none';
        cancelButton.style.display = 'none';
    }
}

// Функция сохранения изменений
function saveEditing(index) {
    var newName = document.getElementById(`supplier-name-input-${index}`).value.trim();
    var newInn = document.getElementById(`supplier-inn-input-${index}`).value.trim();
    var newAddress = document.getElementById(`supplier-address-input-${index}`).value.trim();
    var newPhone = document.getElementById(`supplier-phone-input-${index}`).value.trim();
    var newEmail = document.getElementById(`supplier-email-input-${index}`).value.trim();
    var newSigner = document.getElementById(`supplier-signer-input-${index}`).value.trim();
    var nameDisplay = document.getElementById(`supplier-name-display-${index}`);
    var innDisplay = document.getElementById(`supplier-inn-display-${index}`);
    var addressDisplay = document.getElementById(`supplier-address-display-${index}`);
    var phoneDisplay = document.getElementById(`supplier-phone-display-${index}`);
    var emailDisplay = document.getElementById(`supplier-email-display-${index}`);
    var signerDisplay = document.getElementById(`supplier-signer-display-${index}`);
    var calcId = getCalcIdFromSection(index);

    // Валидация данных
    if (!newName) {
        Swal.fire({
            icon: 'warning',
            title: 'Ошибка!',
            text: 'Введите корректное наименование поставщика.',
            confirmButtonColor: '#67a2d5',
        });
        return;
    }

    if (newInn.length !== 10 && newInn.length !== 12 || !/^\d+$/.test(newInn)) {
        Swal.fire({
            icon: 'warning',
            title: 'Ошибка!',
            text: 'ИНН должен содержать 10 или 12 цифр.',
            confirmButtonColor: '#67a2d5',
        });
        return;
    }

    // Обновляем отображаемые значения
    nameDisplay.textContent = newName;
    innDisplay.textContent = newInn;
    addressDisplay.textContent = newAddress;
    phoneDisplay.textContent = newPhone;
    emailDisplay.textContent = newEmail;
    signerDisplay.textContent = newSigner;

    // Выключаем режим редактирования
    toggleEditMode(index, false);

    // Отправляем данные на сервер
    $.ajax({
        url: '/crm/calculator/update-seller',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            title: newName,
            inn: newInn,
            address: newAddress,
            phone: newPhone,
            email: newEmail,
            signer: newSigner,
            calc_id: calcId
        }),
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
                title: "Данные продавца обновлены."
            });

            // Проверяем, существует ли иконка удаления
            var deleteIcon = document.getElementById(`edit-delete-icon-${index}`);
            if (!deleteIcon) {
                // Создаем новую иконку удаления, если её нет
                deleteIcon = document.createElement('i');
                deleteIcon.classList.add('fa-solid', 'fa-xmark', 'edit-delete-icon');
                deleteIcon.id = `edit-delete-icon-${index}`;
                deleteIcon.setAttribute('data-index', index);

                // Добавляем иконку в нужное место в DOM
                var parentElement = document.getElementById(`edit-name-icon-${index}`).parentElement;
                if (parentElement) {
                    parentElement.appendChild(deleteIcon);
                }
            }
        },
        error: function (xhr, status, error) {
            // Обновляем значения полей, чтобы сделать их пустыми
            nameDisplay.textContent = '';
            innDisplay.textContent = '';
            addressDisplay.textContent = '';
            phoneDisplay.textContent = '';
            emailDisplay.textContent = '';
            signerDisplay.textContent = '';

            document.getElementById(`supplier-address-input-${index}`).value = '';
            document.getElementById(`supplier-phone-input-${index}`).value = '';
            document.getElementById(`supplier-email-input-${index}`).value = '';
            document.getElementById(`supplier-signer-input-${index}`).value = '';

            // Выводим сообщение об ошибке
            Swal.fire({
                icon: 'error',
                text: 'Ошибка при обновлении данных продавца.',
                confirmButtonColor: '#67a2d5',
            });
        }
    });
}

function getCalcIdFromSection(index) {
    // Получаем секцию по ID
    const section = document.getElementById(`deal-section-${index}`);

    // Если секция найдена, получаем значение data-id
    if (section) {
        return section.dataset.id;
    } else {
        console.error(`Section with index ${index} not found`);
        return null;
    }
}
