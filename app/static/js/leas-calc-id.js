function createCommercialOffer(scheduleType, leasCalculatorId) {
    // Создаем форму для отправки POST-запроса
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/crm/calculator/${leasCalculatorId}/create-commercial-offer`;

    // Создаем скрытое поле для передачи типа графика
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'type_of_schedule';
    input.value = scheduleType;

    // Добавляем скрытое поле в форму
    form.appendChild(input);

    // Отправляем форму
    document.body.appendChild(form);
    form.submit();
}