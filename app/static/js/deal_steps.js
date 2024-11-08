const socket = io({
    path: "/crm/socket.io"
});

socket.on('update_steps', function (response) {
    updateStepsStatus(response);
});

function approveStep(step) {
    socket.emit('approve_step', {'step': step});
}

function revokeStep(step) {
    socket.emit('revoke_step', {'step': step});
}

function updateStepsStatus(response) {
    document.getElementById('status-step1').innerText = response.step1.approved ? `Approved by ${response.step1.user} at ${response.step1.time}` : 'Not Approved';
    document.getElementById('status-step2').innerText = response.step2.approved ? `Approved by ${response.step2.user} at ${response.step2.time}` : 'Not Approved';
    document.getElementById('status-step3').innerText = response.step3.approved ? `Approved by ${response.step3.user} at ${response.step3.time}` : 'Not Approved';

    if (response.step3.approved) {
        var dealMessage = document.getElementById('deal-message');
        if (!dealMessage) {
            dealMessage = document.createElement('p');
            dealMessage.id = 'deal-message';
            dealMessage.innerText = 'The deal can be completed!';
            document.getElementById('deal-steps').appendChild(dealMessage);
        }
    } else {
        var dealMessage = document.getElementById('deal-message');
        if (dealMessage) {
            dealMessage.remove();
        }
    }
}