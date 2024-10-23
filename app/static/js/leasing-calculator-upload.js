// Получаем элементы
const fileUploadContainer = document.getElementById('file-upload-container');
const fileInput = document.getElementById('file-upload-input');
const fileNameDisplay = document.getElementById('file-name');
const errorMessage = document.getElementById('error-message');
const uploadButton = document.getElementById('upload-button');

// Обработчик выбора файла через input
fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        // Проверяем формат файла
        if (!file.name.endsWith('.xlsm')) {
            fileNameDisplay.textContent = 'Файл не выбран';
            errorMessage.style.display = 'block'; // Показываем ошибку
            uploadButton.style.display = 'none'; // Скрываем кнопку загрузки
        } else {
            fileNameDisplay.textContent = file.name;
            errorMessage.style.display = 'none'; // Скрываем ошибку
            uploadButton.style.display = 'inline-block'; // Показываем кнопку загрузки
        }
    } else {
        fileNameDisplay.textContent = 'Файл не выбран';
        errorMessage.style.display = 'none';
        uploadButton.style.display = 'none';
    }
});

// Обработка событий drag and drop
fileUploadContainer.addEventListener('dragover', function (e) {
    e.preventDefault();
    fileUploadContainer.classList.add('dragover');
});

fileUploadContainer.addEventListener('dragleave', function () {
    fileUploadContainer.classList.remove('dragover');
});

fileUploadContainer.addEventListener('drop', function (e) {
    e.preventDefault();
    fileUploadContainer.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        fileInput.files = e.dataTransfer.files; // Помещаем файл в input
        // Проверяем формат файла
        if (!file.name.endsWith('.xlsm')) {
            fileNameDisplay.textContent = 'Файл не выбран';
            errorMessage.style.display = 'block'; // Показываем ошибку
            uploadButton.style.display = 'none'; // Скрываем кнопку загрузки
        } else {
            fileNameDisplay.textContent = file.name;
            errorMessage.style.display = 'none'; // Скрываем ошибку
            uploadButton.style.display = 'inline-block'; // Показываем кнопку загрузки
        }
    }
});

// Обработчик клика по контейнеру для открытия выбора файла
fileUploadContainer.addEventListener('click', function (e) {
    if (e.target.classList.contains('file-upload-label')) {
        return; // Прерываем событие, если клик был по label
    }
    fileInput.click(); // Открываем диалог выбора файла
});

// Обработчик для отправки файла
uploadButton.addEventListener('click', function () {
    const file = fileInput.files[0];

    if (file) {
        // Окно подтверждения перед загрузкой файла
        Swal.fire({
            text: 'Вы точно хотите отправить файл?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#5789b9',
            cancelButtonColor: '#ad6c72',
            confirmButtonText: 'Да',
            cancelButtonText: 'Отменить'
        }).then((result) => {
            if (result.isConfirmed) {
                // Блокируем кнопку
                uploadButton.disabled = true;
                uploadButton.style.cursor = 'not-allowed';
                uploadButton.style.opacity = '0.6';

                // Создаем форму для отправки файла
                const formData = new FormData();
                formData.append('file', file);

                // Отправляем файл на сервер через fetch
                fetch('/crm/calculator/upload-file', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.file_name) {
                            Swal.fire({
                                icon: 'success',
                                text: 'Файл успешно загружен!',
                                showConfirmButton: false,
                                timer: 1500
                            }).then(() => {
                                // Обновляем страницу после успешной загрузки
                                window.location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                text: 'Ошибка при загрузке файла: ' + data.error,
                            });
                        }
                    })
                    .catch(error => {
                        Swal.fire({
                            icon: 'error',
                            title: 'Ошибка',
                            text: 'Ошибка при отправке файла',
                        });
                    })
                    .finally(() => {
                        // Разблокируем кнопку после завершения
                        uploadButton.disabled = false;
                        uploadButton.style.cursor = 'pointer';
                        uploadButton.style.opacity = '1';
                    });
            }
        });
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Ошибка',
            text: 'Вы не выбрали файл для загрузки!',
        });
    }
});
