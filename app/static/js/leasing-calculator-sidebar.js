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
