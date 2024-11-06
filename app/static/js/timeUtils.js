// timeUtils.js

function getPlural(number, forms) {
    number = Math.abs(number) % 100;
    const n1 = number % 10;
    if (number > 10 && number < 20) return forms[2];
    if (n1 > 1 && n1 < 5) return forms[1];
    if (n1 === 1) return forms[0];
    return forms[2];
}

function formatTimeAgo(dateString) {
    let createdAtStr = dateString.split('.')[0];
    createdAtStr = createdAtStr.replace(' ', 'T');
    const dealCreatedAt = new Date(createdAtStr);

    const now = new Date();
    const diffInSeconds = Math.floor((now - dealCreatedAt) / 1000);

    let timeAgo = '';
    if (diffInSeconds < 60) {
        timeAgo = 'только что';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        timeAgo = `${minutes} ${getPlural(minutes, ['минута', 'минуты', 'минут'])} назад`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        timeAgo = `${hours} ${getPlural(hours, ['час', 'часа', 'часов'])} назад`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        timeAgo = `${days} ${getPlural(days, ['день', 'дня', 'дней'])} назад`;
    }

    return timeAgo;
}
