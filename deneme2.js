const lines = document.querySelectorAll(".line h1");

lines.forEach((h1, index) => {
  setTimeout(() => {
    h1.style.transition = "transform 0.7s ease, opacity 0.7s ease";
    h1.style.transform = "translateY(0)";
    h1.style.opacity = "1";
  }, index * 350);
});
