document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
      setTimeout(() => {
        alert.classList.add("fade");
        alert.style.opacity = "0";
      }, 3000);
    });
  });
  