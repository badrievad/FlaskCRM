function showTab(tabId) {
    var tabs = document.getElementsByClassName('tab-content');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }
    document.getElementById(tabId).classList.add('active');

    var tabButtons = document.getElementsByClassName('tab');
    for (var i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    event.target.classList.add('active');
}

function toggleSubmenu(id) {
    var submenu = document.getElementById(id);
    if (submenu.classList.contains('show')) {
        submenu.classList.remove('show');
    } else {
        submenu.classList.add('show');
    }
}

function showForm(formId) {
    document.querySelectorAll('.deal-content .card').forEach(card => {
        card.classList.add('hidden');
    });
    document.getElementById(formId).classList.remove('hidden');
}

window.onload = function () {
    document.getElementById("sidebar").classList.add("open");
    document.getElementById("main-content").classList.remove("shrink");

}