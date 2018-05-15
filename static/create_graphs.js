function makegraph(years, revenue) {
    var ctx = document.getElementById("chart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: years,
            datasets: [{
                label: 'Revenue',
                data: revenue
            }]
    }
});
}

