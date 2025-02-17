document.addEventListener("DOMContentLoaded", function () {
    const layoutSelect = document.getElementById("layout-select");
    const metricSelect = document.getElementById("metric-select");
    const timeButtons = document.querySelectorAll(".time-options button");
    const colorSelect = document.getElementById("color-select");
    const imageContainer = document.getElementById("generated-image-container");
    const generatedImage = document.getElementById("generated-image");

    const downloadBtn = document.getElementById("download-btn");

    let selectedPeriod = "short_term";
    let selectedColor = "default";

    function updateLayout() {
        let layout = layoutSelect.value;
        let metric = metricSelect.value;

        let newSrc = `/generate_recap/?layout=${layout}&metric=${metric}&period=${selectedPeriod}&color=${selectedColor}`;
        
        generatedImage.onload = function () {
            if (layout === "list") {
                imageContainer.classList.add("list-view");
                generatedImage.style.width = "auto";
                generatedImage.style.aspectRatio = "auto";
            } else {
                imageContainer.classList.remove("list-view");
                generatedImage.style.width = "60%";
                generatedImage.style.aspectRatio = "9 / 16";
            }
        };

        colorSelect.addEventListener("change", function () {
            selectedColor = this.value;
            updateLayout();
        });

        generatedImage.src = newSrc;
    }

    downloadBtn.addEventListener("click", function () {
        const imageUrl = generatedImage.src;
        const fileName = "serenade_music_recap.png";

        fetch(imageUrl)
            .then(response => response.blob())
            .then(blob => {
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => console.error("Error downloading image:", error));
    });

    timeButtons.forEach(button => {
        button.addEventListener("click", function () {
            timeButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            selectedPeriod = this.getAttribute("data-period");
            updateLayout();
        });
    });

    layoutSelect.addEventListener("change", updateLayout);
    metricSelect.addEventListener("change", updateLayout);

    updateLayout();
});

