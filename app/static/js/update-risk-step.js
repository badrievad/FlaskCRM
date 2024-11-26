function updateStepper(decision) {
    const riskStep = document.getElementById('step-risk');

    if (decision === "approve") {
		console.log('Risk step completed');
		console.log(decision);
        riskStep.classList.add('completed');
    } else {
		console.log('Risk step not completed');
        riskStep.classList.remove('completed');
    }
}
