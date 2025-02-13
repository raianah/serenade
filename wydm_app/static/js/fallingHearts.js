document.addEventListener("DOMContentLoaded", function() {
    function createHeart() {
        const heart = document.createElement("div");
        heart.classList.add("heart");
        heart.innerHTML = "💖";
        heart.style.left = Math.random() * 100 + "vw";
        heart.style.animationDuration = Math.random() * 3 + 2 + "s"; 
        document.querySelector(".hearts-container").appendChild(heart);
        setTimeout(() => { heart.remove(); }, 5000);
    }
    setInterval(createHeart, 300);
});

function declineInvite() {
    let declineButton = document.querySelector(".decline-btn");
    declineButton.innerText = "💔 Invitation Declined";
    declineButton.style.background = "#b0b0b0";
    declineButton.style.cursor = "not-allowed"; 
    declineButton.disabled = true;
    setTimeout(() => {
        declineButton.style.opacity = "0";
        declineButton.style.transform = "scale(0.8)";
    }, 500);
}