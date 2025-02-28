const html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", { fps: 10, qrbox: 250 });

let isProcessing = false;

function onScanSuccess(token) {
    if (isProcessing) return; // Skip if already processing a token
    isProcessing = true;

    const resultDiv = document.getElementById('result');

    fetch('/verify_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token })
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.classList.remove('d-none', 'alert-success', 'alert-danger', 'alert-warning');
        if (data.valid) {
            if (data.already_redeemed) {
                resultDiv.classList.add('alert-warning');
                resultDiv.innerHTML = `Token already redeemed for ${data.user.name} (${data.user.email})`;
            } else {
                resultDiv.classList.add('alert-success');
                resultDiv.innerHTML = `Valid token for ${data.user.name} (${data.user.email})<br>Token ID: ${token}<br>Status: ${data.redeemed ? 'Redeemed' : 'Active'}`;
            }
        } else {
            resultDiv.classList.add('alert-danger');
            resultDiv.innerHTML = 'Invalid token';
        }

        // Reset processing flag after 2 seconds
        setTimeout(() => {
            isProcessing = false;
        }, 2000);
    })
    .catch(error => {
        resultDiv.classList.remove('d-none');
        resultDiv.classList.add('alert-danger');
        resultDiv.innerHTML = 'Error verifying token';

        setTimeout(() => {
            isProcessing = false;
        }, 2000);
    });
}

html5QrcodeScanner.render(onScanSuccess);