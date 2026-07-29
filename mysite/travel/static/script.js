function navigateTo(feature) {
    alert(`Navigate to ${feature} section.`);
    // Add logic here to redirect or load components dynamically
}
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('splitForm');
    form?.addEventListener('submit', function (e) {
        e.preventDefault();

        const amount = parseFloat(document.getElementById('amount').value);
        const names = document.getElementById('participants').value.split(',').map(n => n.trim());
        const share = (amount / names.length).toFixed(2);
        let output = `<p>Total: ₹${amount}</p><ul>`;

        names.forEach(name => {
            output += `<li>${name} owes ₹${share}</li>`;
        });

        output += '</ul>';
        document.getElementById('result').innerHTML = output;
    });
});
