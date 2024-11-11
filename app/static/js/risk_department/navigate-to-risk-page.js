function navigateToRiskDepartment(url) {
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', function () {
	var clickableItems = document.querySelectorAll('.sidebar ul li.clickable')

	clickableItems.forEach(function (item) {
		item.addEventListener('click', function () {
			var link = item.querySelector('a.nav-link')
			if (link) {
				window.location.href = link.href
			}
		})
	})
})
