let current = 0;
const slides = document.querySelectorAll(".slide");
const progress = document.querySelector(".progress");

function showSlide(index) {
  slides.forEach(s => s.classList.remove("active"));
  slides[index].classList.add("active");

  progress.style.width = ((index + 1) / slides.length) * 100 + "%";
}

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight") next();
  if (e.key === "ArrowLeft") prev();
});

function next() {
  if (current < slides.length - 1) {
    current++;
    showSlide(current);
  }
}

function prev() {
  if (current > 0) {
    current--;
    showSlide(current);
  }
}

showSlide(current);