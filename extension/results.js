document.addEventListener('DOMContentLoaded', function () {
    var randomPercentage = Math.floor(Math.random() * 101);
    displayResults(randomPercentage);
});

function displayResults(percentage) {
    var percentageElement = document.getElementById('percentage');
    var percentageBar = document.getElementById('percentage-bar');

    percentageElement.textContent = 'Random Percentage: ' + percentage + '%';

    if (percentage < 30) {
        percentageBar.style.backgroundColor = 'red';
    } else if (percentage >= 30 && percentage < 70) {
        percentageBar.style.backgroundColor = 'yellow';
    } else {
        percentageBar.style.backgroundColor = 'green';
    }

    percentageBar.style.width = percentage + '%';
}
