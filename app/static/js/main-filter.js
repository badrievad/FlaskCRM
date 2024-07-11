// Показать или скрыть строку фильтрации
const filterHeader = document.getElementById('filter-header');
const filterSearch = document.getElementById('filter-search');
const filterSearchArchived = document.getElementById('filter-search-archived');
const filterHeaderArchived = document.getElementById('filter-header-archived');
const filterRow = document.getElementById('filter-row');
const filterRowArchived = document.getElementById('filter-row-archived');
filterHeader.addEventListener('click', () => {
    filterRow.classList.toggle('hidden');
    filterRow.classList.toggle('show');
});
filterHeaderArchived.addEventListener('click', () => {
    filterRowArchived.classList.toggle('hidden');
    filterRowArchived.classList.toggle('show');
});

filterSearch.addEventListener('click', () => {
    filterRow.classList.toggle('hidden');
    filterRow.classList.toggle('show');
});
filterSearchArchived.addEventListener('click', () => {
    filterRowArchived.classList.toggle('hidden');
    filterRowArchived.classList.toggle('show');
});


// Фильтрация сделок по ДЛ
const filterInputDl = document.getElementById('filter-input-dl');
const filterInputDlArchived = document.getElementById('filter-input-dl-archived');

// Фильтрация сделок по Лизингополучателю
const filterInput = document.getElementById('filter-input');
const filterInputArchived = document.getElementById('filter-input-archived');

// Фильтрация сделок по продукту
const filterInputProduct = document.getElementById('filter-input-product');
const filterInputProductArchived = document.getElementById('filter-input-product-archived');

// Фильтрация сделок по менеджеру
const filterInputManager = document.getElementById('filter-input-manager');
const filterInputManagerArchived = document.getElementById('filter-input-manager-archived');

// Фильтрация сделок по созданию
const filterInputCreated = document.getElementById('filter-input-created');
const filterInputCreatedArchived = document.getElementById('filter-input-created-archived');

// Фильтрация сделок по дате архивации
const filterInputArchivedDateArchived = document.getElementById('filter-input-to-archive-archived');


filterInput.addEventListener('input', function () {
    const filterValue = filterInput.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows tr');
    dealRows.forEach(row => {
        const title = row.querySelector('.deal-title').textContent.toLowerCase();
        if (title.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});
filterInputArchived.addEventListener('input', function () {
    const filterValue = filterInputArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const title = row.querySelector('.deal-title').textContent.toLowerCase();
        if (title.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

filterInputProduct.addEventListener('input', function () {
    const filterValue = filterInputProduct.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows tr');
    dealRows.forEach(row => {
        const product = row.querySelector('.deal-product').textContent.toLowerCase();
        if (product.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});
filterInputProductArchived.addEventListener('input', function () {
    const filterValue = filterInputProductArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const product = row.querySelector('.deal-product').textContent.toLowerCase();
        if (product.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
})

filterInputManager.addEventListener('input', function () {
    const filterValue = filterInputManager.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows tr');
    dealRows.forEach(row => {
        const manager = row.querySelector('.deal-manager').textContent.toLowerCase();
        if (manager.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});
filterInputManagerArchived.addEventListener('input', function () {
    const filterValue = filterInputManagerArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const manager = row.querySelector('.deal-manager').textContent.toLowerCase();
        if (manager.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
})

filterInputCreated.addEventListener('input', function () {
    const filterValue = filterInputCreated.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows tr');
    dealRows.forEach(row => {
        const created = row.querySelector('.deal-created').textContent.toLowerCase();
        if (created.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});
filterInputCreatedArchived.addEventListener('input', function () {
    const filterValue = filterInputCreatedArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const created = row.querySelector('.deal-created').textContent.toLowerCase();
        if (created.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
})

filterInputArchivedDateArchived.addEventListener('input', function () {
    const filterValue = filterInputArchivedDateArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const archived = row.querySelector('.deal-archived').textContent.toLowerCase();
        if (archived.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

filterInputDl.addEventListener('input', function () {
    const filterValue = filterInputDl.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows tr');
    dealRows.forEach(row => {
        const dl = row.querySelector('.deal-dl').textContent.toLowerCase();
        if (dl.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});
filterInputDlArchived.addEventListener('input', function () {
    const filterValue = filterInputDlArchived.value.toLowerCase();
    const dealRows = document.querySelectorAll('#deal-rows-archived tr');
    dealRows.forEach(row => {
        const dl = row.querySelector('.deal-dl').textContent.toLowerCase();
        if (dl.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});