$(document).ready(function () {
    $(".login100-form").on("submit", function (event) {
        event.preventDefault();  // Отключаем стандартное поведение формы

        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "active_session") {
                    // Показываем модальное окно, если сессия уже активна
                    $("#activeSessionModal").modal("show");

                    // Обработчик для подтверждения входа
                    $("#confirmLogin").one("click", function () {
                        $.ajax({
                            type: "POST",
                            url: "/crm/user/process-login?force=true",
                            data: $(".login100-form").serialize(),
                            success: function (res) {
                                if (res.status === "success") {
                                    window.location.href = res.redirect_url;
                                }
                            }
                        });
                    });
                } else if (response.status === "success") {
                    window.location.href = response.redirect_url;
                } else {
                    showError(response.message, "Ошибка");
                }
            }
        });
    });
});
