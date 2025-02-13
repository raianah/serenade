function copyToClipboard() {
    var copyText = document.getElementById("inviteLink");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Successfully copied. Now go impress your date!");
}