document.addEventListener('click', function (event) {
    if (event.target.classList.contains('remove-section-icon')) {
        var index = event.target.getAttribute('data-index');
        var calcId = event.target.getAttribute('data-id');
        var dlNumber = event.target.getAttribute('data-dl-number');

        Swal.fire({
            text: `Вы точно хотите отвязать договор` + ` № ${dlNumber} от сделки?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#67a2d5',
            cancelButtonColor: '#ad6c72',
            confirmButtonText: 'Да, удалить',
            cancelButtonText: 'Отменить'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById(`deal-section-${index}`).remove();

                $.ajax({
                    url: '/crm/deal/inside/delete-section',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({calc_id: calcId}),
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
                            title: "Договор успешно отвязан от сделки."
                        });
                    },
                    error: function (xhr, status, error) {
                        Swal.fire({
                            icon: 'error',
                            text: 'Ошибка при удалении секции',
                            confirmButtonColor: '#67a2d5',
                        });
                    }
                });
            }
        });
    }
});
