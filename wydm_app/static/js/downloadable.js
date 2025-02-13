function downloadAsImage() {
    let captureArea = document.getElementById("capture-area");
    
    document.querySelector(".link-box").style.display = "none";
    document.querySelector(".button-group").style.display = "none";
    document.querySelector(".share-text").style.display = "none";

    html2canvas(captureArea, {
        backgroundColor: null,
        scale: 2
    }).then(canvas => {
        let link = document.createElement("a");
        link.href = canvas.toDataURL("image/png");
        link.download = "date_response.png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        document.querySelector(".link-box").style.display = "flex";
        document.querySelector(".button-group").style.display = "flex";
        document.querySelector(".share-text").style.display = "block";
    });
}