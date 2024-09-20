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
        const index = event.target.getAttribute('data-index');
        toggleEditMode(index, true);
    }
});

// Обработчик для кнопки "Сохранить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('save-supplier')) {
        const index = event.target.getAttribute('data-index');
        saveEditing(index);
    }
});

// Обработчик для кнопки "Отменить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('cancel-supplier')) {
        const index = event.target.getAttribute('data-index');
        toggleEditMode(index, false);
    }
});

// Функция переключения режима редактирования
function toggleEditMode(index, isEditing) {
    const nameDisplay = document.getElementById(`supplier-name-display-${index}`);
    const nameInput = document.getElementById(`supplier-name-input-${index}`);
    const innDisplay = document.getElementById(`supplier-inn-display-${index}`);
    const innInput = document.getElementById(`supplier-inn-input-${index}`);
    const addressDisplay = document.getElementById(`supplier-address-display-${index}`);
    const addressInput = document.getElementById(`supplier-address-input-${index}`);
    const phoneDisplay = document.getElementById(`supplier-phone-display-${index}`);
    const phoneInput = document.getElementById(`supplier-phone-input-${index}`);
    const emailDisplay = document.getElementById(`supplier-email-display-${index}`);
    const emailInput = document.getElementById(`supplier-email-input-${index}`);
    const signerDisplay = document.getElementById(`supplier-signer-display-${index}`);
    const signerInput = document.getElementById(`supplier-signer-input-${index}`);
    const basedDisplay = document.getElementById(`supplier-based-display-${index}`);
    const basedInput = document.getElementById(`supplier-based-input-${index}`);
    const bankDisplay = document.getElementById(`supplier-bank-display-${index}`);
    const bankInput = document.getElementById(`supplier-bank-input-${index}`);
    const currentDisplay = document.getElementById(`supplier-current-display-${index}`);
    const currentInput = document.getElementById(`supplier-current-input-${index}`);
    const saveButton = document.getElementById(`save-supplier-${index}`);
    const cancelButton = document.getElementById(`cancel-supplier-${index}`);
    const editIcon = document.getElementById(`edit-name-icon-${index}`);
    const deleteIcon = document.getElementById(`edit-delete-icon-${index}`);

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
        basedDisplay.style.display = 'none';
        basedInput.style.display = 'inline';
        bankDisplay.style.display = 'none';
        bankInput.style.display = 'inline';
        currentDisplay.style.display = 'none';
        currentInput.style.display = 'inline';
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
        basedDisplay.style.display = 'inline';
        basedInput.style.display = 'none';
        bankDisplay.style.display = 'inline';
        bankInput.style.display = 'none';
        currentDisplay.style.display = 'inline';
        currentInput.style.display = 'none';
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
    const newName = document.getElementById(`supplier-name-input-${index}`).value.trim();
    const newInn = document.getElementById(`supplier-inn-input-${index}`).value.trim();
    const newAddress = document.getElementById(`supplier-address-input-${index}`).value.trim();
    const newPhone = document.getElementById(`supplier-phone-input-${index}`).value.trim();
    const newEmail = document.getElementById(`supplier-email-input-${index}`).value.trim();
    const newSigner = document.getElementById(`supplier-signer-input-${index}`).value.trim();
    const newBased = document.getElementById(`supplier-based-input-${index}`).value.trim();
    const newBank = document.getElementById(`supplier-bank-input-${index}`).value.trim();
    const newCurrent = document.getElementById(`supplier-current-input-${index}`).value.trim();
    const nameDisplay = document.getElementById(`supplier-name-display-${index}`);
    const innDisplay = document.getElementById(`supplier-inn-display-${index}`);
    const addressDisplay = document.getElementById(`supplier-address-display-${index}`);
    const phoneDisplay = document.getElementById(`supplier-phone-display-${index}`);
    const emailDisplay = document.getElementById(`supplier-email-display-${index}`);
    const signerDisplay = document.getElementById(`supplier-signer-display-${index}`);
    const basedDisplay = document.getElementById(`supplier-based-display-${index}`);
    const bankDisplay = document.getElementById(`supplier-bank-display-${index}`);
    const currentDisplay = document.getElementById(`supplier-current-display-${index}`);
    const calcId = getCalcIdFromSection(index);

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
    basedDisplay.textContent = newBased;
    bankDisplay.textContent = newBank;
    currentDisplay.textContent = newCurrent;

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
            calc_id: calcId,
            based_on: newBased,
            bank: newBank,
            current: newCurrent
        }),
        success: function () {
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
            let deleteIcon = document.getElementById(`edit-delete-icon-${index}`);
            if (!deleteIcon) {
                // Создаем новую иконку удаления, если её нет
                deleteIcon = document.createElement('i');
                deleteIcon.classList.add('fa-solid', 'fa-xmark', 'edit-delete-icon');
                deleteIcon.id = `edit-delete-icon-${index}`;
                deleteIcon.setAttribute('data-index', index);

                // Добавляем иконку в нужное место в DOM
                let parentElement = document.getElementById(`edit-name-icon-${index}`).parentElement;
                if (parentElement) {
                    parentElement.appendChild(deleteIcon);
                }
            }
        },
        error: function () {
            // Обновляем значения полей, чтобы сделать их пустыми
            nameDisplay.textContent = '';
            innDisplay.textContent = '';
            addressDisplay.textContent = '';
            phoneDisplay.textContent = '';
            emailDisplay.textContent = '';
            signerDisplay.textContent = '';
            basedDisplay.textContent = '';
            bankDisplay.textContent = '';
            currentDisplay.textContent = '';

            document.getElementById(`supplier-address-input-${index}`).value = '';
            document.getElementById(`supplier-phone-input-${index}`).value = '';
            document.getElementById(`supplier-email-input-${index}`).value = '';
            document.getElementById(`supplier-signer-input-${index}`).value = '';
            document.getElementById(`supplier-based-input-${index}`).value = '';
            document.getElementById(`supplier-bank-input-${index}`).value = '';
            document.getElementById(`supplier-current-input-${index}`).value = '';

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


// Используем делегирование событий для иконки редактирования клиента
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('edit-client-icon')) {
        toggleEditModeClient(true);
    }
});

// Обработчик для кнопки "Сохранить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('save-client')) {
        saveEditingClient();
    }
});

// Обработчик для кнопки "Отменить"
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('cancel-client')) {
        toggleEditModeClient(false);
    }
});

// Функция переключения режима редактирования клиента
function toggleEditModeClient(isEditing) {
    const nameDisplayClient = document.getElementById(`client-name-display`);
    const nameInputClient = document.getElementById(`client-name-input`);
    const innDisplayClient = document.getElementById(`client-inn-display`);
    const innInputClient = document.getElementById(`client-inn-input`);
    const addressDisplayClient = document.getElementById(`client-address-display`);
    const addressInputClient = document.getElementById(`client-address-input`);
    const phoneDisplayClient = document.getElementById(`client-phone-display`);
    const phoneInputClient = document.getElementById(`client-phone-input`);
    const emailDisplayClient = document.getElementById(`client-email-display`);
    const emailInputClient = document.getElementById(`client-email-input`);
    const signerDisplayClient = document.getElementById(`client-signer-display`);
    const signerInputClient = document.getElementById(`client-signer-input`);
    const basedDisplayClient = document.getElementById(`client-based-display`);
    const basedInputClient = document.getElementById(`client-based-input`);
    const bankDisplayClient = document.getElementById(`client-bank-display`);
    const bankInputClient = document.getElementById(`client-bank-input`);
    const currentDisplayClient = document.getElementById(`client-current-display`);
    const currentInputClient = document.getElementById(`client-current-input`);
    const saveButtonClient = document.getElementById(`save-client`);
    const cancelButtonClient = document.getElementById(`cancel-client`);
    const editIconClient = document.getElementById(`edit-client-icon`);

    if (isEditing) {
        // Включаем режим редактирования
        nameDisplayClient.style.display = 'none';
        nameInputClient.style.display = 'inline';
        innDisplayClient.style.display = 'none';
        innInputClient.style.display = 'inline';
        addressDisplayClient.style.display = 'none';
        addressInputClient.style.display = 'inline';
        phoneDisplayClient.style.display = 'none';
        phoneInputClient.style.display = 'inline';
        emailDisplayClient.style.display = 'none';
        emailInputClient.style.display = 'inline';
        signerDisplayClient.style.display = 'none';
        signerInputClient.style.display = 'inline';
        basedDisplayClient.style.display = 'none';
        basedInputClient.style.display = 'inline';
        bankDisplayClient.style.display = 'none';
        bankInputClient.style.display = 'inline';
        currentDisplayClient.style.display = 'none';
        currentInputClient.style.display = 'inline';
        editIconClient.style.display = 'none';
        saveButtonClient.style.display = 'inline-block';
        cancelButtonClient.style.display = 'inline-block';
        nameInputClient.focus();
    } else {
        // Выключаем режим редактирования
        nameDisplayClient.style.display = 'inline';
        nameInputClient.style.display = 'none';
        innDisplayClient.style.display = 'inline';
        innInputClient.style.display = 'none';
        addressDisplayClient.style.display = 'inline';
        addressInputClient.style.display = 'none';
        phoneDisplayClient.style.display = 'inline';
        phoneInputClient.style.display = 'none';
        emailDisplayClient.style.display = 'inline';
        emailInputClient.style.display = 'none';
        signerDisplayClient.style.display = 'inline';
        signerInputClient.style.display = 'none';
        basedDisplayClient.style.display = 'inline';
        basedInputClient.style.display = 'none';
        bankDisplayClient.style.display = 'inline';
        bankInputClient.style.display = 'none';
        currentDisplayClient.style.display = 'inline';
        currentInputClient.style.display = 'none';
        editIconClient.style.display = 'inline';
        saveButtonClient.style.display = 'none';
        cancelButtonClient.style.display = 'none';
    }
}

// Функция сохранения изменений
function saveEditingClient() {
    const newNameClient = document.getElementById(`client-name-input`).value.trim();
    const newInnClient = document.getElementById(`client-inn-input`).value.trim();
    const newAddressClient = document.getElementById(`client-address-input`).value.trim();
    const newPhoneClient = document.getElementById(`client-phone-input`).value.trim();
    const newEmailClient = document.getElementById(`client-email-input`).value.trim();
    const newSignerClient = document.getElementById(`client-signer-input`).value.trim();
    const newBasedClient = document.getElementById(`client-based-input`).value.trim();
    const newBankClient = document.getElementById(`client-bank-input`).value.trim();
    const newCurrentClient = document.getElementById(`client-current-input`).value.trim();
    const nameDisplayClient = document.getElementById(`client-name-display`);
    const innDisplayClient = document.getElementById(`client-inn-display`);
    const addressDisplayClient = document.getElementById(`client-address-display`);
    const phoneDisplayClient = document.getElementById(`client-phone-display`);
    const emailDisplayClient = document.getElementById(`client-email-display`);
    const signerDisplayClient = document.getElementById(`client-signer-display`);
    const basedDisplayClient = document.getElementById(`client-based-display`);
    const bankDisplayClient = document.getElementById(`client-bank-display`);
    const currentDisplayClient = document.getElementById(`client-current-display`);
    const saveClientButton = document.getElementById('save-client');
    const dealId = saveClientButton.getAttribute('deal-id');

    // Валидация данных
    if (!newNameClient) {
        Swal.fire({
            icon: 'warning',
            title: 'Ошибка!',
            text: 'Введите корректное наименование поставщика.',
            confirmButtonColor: '#67a2d5',
        });
        return;
    }

    if (newInnClient.length !== 10 && newInnClient.length !== 12 || !/^\d+$/.test(newInnClient)) {
        Swal.fire({
            icon: 'warning',
            title: 'Ошибка!',
            text: 'ИНН должен содержать 10 или 12 цифр.',
            confirmButtonColor: '#67a2d5',
        });
        return;
    }

    // Обновляем отображаемые значения
    nameDisplayClient.textContent = newNameClient;
    innDisplayClient.textContent = newInnClient;
    addressDisplayClient.textContent = newAddressClient;
    phoneDisplayClient.textContent = newPhoneClient;
    emailDisplayClient.textContent = newEmailClient;
    signerDisplayClient.textContent = newSignerClient;
    basedDisplayClient.textContent = newBasedClient;
    bankDisplayClient.textContent = newBankClient;
    currentDisplayClient.textContent = newCurrentClient;

    // Выключаем режим редактирования
    toggleEditModeClient(false);

    // Отправляем данные на сервер
    $.ajax({
        url: '/crm/deal/inside/update-client',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            deal_id: dealId,
            address: newAddressClient,
            phone: newPhoneClient,
            email: newEmailClient,
            signer: newSignerClient,
            based_on: newBasedClient,
            bank: newBankClient,
            current: newCurrentClient
        }),
        success: function () {
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
                title: "Данные клиента обновлены."
            });
        },
        error: function () {
            // Обновляем значения полей, чтобы сделать их пустыми
            phoneDisplayClient.textContent = '';
            emailDisplayClient.textContent = '';

            document.getElementById(`client-phone-input`).value = '';
            document.getElementById(`client-email-input`).value = '';

            // Выводим сообщение об ошибке
            Swal.fire({
                icon: 'error',
                text: 'Ошибка при обновлении данных клиента.',
                confirmButtonColor: '#67a2d5',
            });
        }
    });
}