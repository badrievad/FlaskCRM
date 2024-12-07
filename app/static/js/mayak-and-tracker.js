const termValueInput = document.getElementById('term-value')
const termRange = document.getElementById('term')

const oneTimeMayak = document.getElementById('one-time-mayak')
const monthlyMayak = document.getElementById('monthly-mayak')
const oneTimeTreker = document.getElementById('one-time-treker')
const monthlyTreker = document.getElementById('monthly-treker')

const mayakiPriceEl = document.getElementById('mayaki-price')
const trackeryPriceEl = document.getElementById('trackery-price')
const mayakiTrackeryPriceEl = document.getElementById('mayaki-trackery-price')

function formatPrice(value) {
	return value.toLocaleString('ru-RU') + ' руб.'
}

function calculatePrices() {
	const leaseTerm = parseInt(termValueInput.value, 10) || 36

	const mayakOneTime = parseFloat(oneTimeMayak.value) || 0
	const mayakMonthly = parseFloat(monthlyMayak.value) || 0
	const trekerOneTime = parseFloat(oneTimeTreker.value) || 0
	const trekerMonthly = parseFloat(monthlyTreker.value) || 0

	// Расчёт для каждого варианта
	const mayakiSum = mayakOneTime + mayakMonthly * leaseTerm
	const trackerySum = trekerOneTime + trekerMonthly * leaseTerm
	const mayakiTrackerySum = mayakiSum + trackerySum

	// Обновляем отображение цен в вариантах
	mayakiPriceEl.textContent = formatPrice(mayakiSum)
	trackeryPriceEl.textContent = formatPrice(trackerySum)
	mayakiTrackeryPriceEl.textContent = formatPrice(mayakiTrackerySum)
}

// События для пересчёта при изменениях
termValueInput.addEventListener('input', () => {
	if (parseInt(termValueInput.value) > 60) {
		termValueInput.value = 60
	}
	termRange.value = termValueInput.value
	calculatePrices()
})

termRange.addEventListener('input', () => {
	termValueInput.value = termRange.value
	calculatePrices()
})

oneTimeMayak.addEventListener('input', calculatePrices)
monthlyMayak.addEventListener('input', calculatePrices)
oneTimeTreker.addEventListener('input', calculatePrices)
monthlyTreker.addEventListener('input', calculatePrices)

// Инициализация при загрузке
calculatePrices()

const maxVal = 20000

const fields = [
	document.getElementById('one-time-mayak'),
	document.getElementById('monthly-mayak'),
	document.getElementById('one-time-treker'),
	document.getElementById('monthly-treker'),
]

fields.forEach(field => {
	field.addEventListener('input', () => {
		let val = parseInt(field.value, 10)
		if (val > maxVal) {
			field.value = maxVal
		}
	})
})
