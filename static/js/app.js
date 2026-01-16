// Add to Cart button functionality
document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".book button");

    buttons.forEach(btn => {
        btn.addEventListener("click", function() {
            alert("Added to cart!");
        });
    });
});
const buttons = document.querySelectorAll('button');

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        alert('Book added to cart!');
    });
});
