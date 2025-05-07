// Daniel Chung, dc3561

function calculateMortgage(principal, rate, years) {
    const monthlyRate = rate / 100 / 12;
    const n = years * 12;
    return (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -n));
}

document.getElementById('mortgageForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const downPayment = parseFloat(document.getElementById('downPayment').value);
    const propertyValue = parseFloat(document.getElementById('propertyValue').value);
    const rentAmount = parseFloat(document.getElementById('rentAmount').value);

    const loanAmount = propertyValue - downPayment;
    const years = 10;

    // Calculate monthly payments
    const fifteenMonthly = calculateMortgage(loanAmount, 6.25, 15);
    const thirtyMonthly = calculateMortgage(loanAmount, 6.75, 30);

    // Calculate yearly cumulative totals
    const rentTotals = [];
    const fifteenTotals = [];
    const thirtyTotals = [];

    let rentCumulative = 0;
    let fifteenCumulative = 0;
    let thirtyCumulative = 0;

    for (let i = 1; i <= years; i++) {
        rentCumulative += rentAmount * 12;
        fifteenCumulative += fifteenMonthly * 12;
        thirtyCumulative += thirtyMonthly * 12;

        rentTotals.push(rentCumulative);
        fifteenTotals.push(fifteenCumulative);
        thirtyTotals.push(thirtyCumulative);
    }

    // Update Monthly Payment in the table
    document.getElementById('monthlyRent').innerText = `$${rentAmount.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    document.getElementById('monthly15').innerText = `$${Math.round(fifteenMonthly).toLocaleString()}`;
    document.getElementById('monthly30').innerText = `$${Math.round(thirtyMonthly).toLocaleString()}`;    

    // Update the chart
    updateChart(rentTotals, fifteenTotals, thirtyTotals);
});

let chart;

function updateChart(rentData, fifteenData, thirtyData) {
    const ctx = document.getElementById('paymentChart').getContext('2d');
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 10 }, (_, i) => `Year ${i + 1}`),
            datasets: [
                {
                    label: 'Rent',
                    data: rentData,
                    borderColor: 'red',
                    fill: false,
                },
                {
                    label: '15-Year Fixed',
                    data: fifteenData,
                    borderColor: 'blue',
                    fill: false,
                },
                {
                    label: '30-Year Fixed',
                    data: thirtyData,
                    borderColor: 'green',
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                  position: 'top',
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      const value = Math.round(context.parsed.y);
                      return `$${value.toLocaleString()}`;
                    }
                  }
                }
              }              
        },        
    });
}