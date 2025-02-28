function generateQR(token) {
    const qrContainer = document.getElementById('qrcode');
    qrContainer.innerHTML = '';

    new QRCode(qrContainer, {
        text: token,
        width: 256,
        height: 256,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
}