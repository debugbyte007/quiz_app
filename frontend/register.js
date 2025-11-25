// register.js
async function initRegister() {
  $("btn-register").onclick = async () => {
    const msg = $("reg-message");
    msg.textContent = "";
    try {
      const username = $("reg-username").value.trim();
      const password = $("reg-password").value;
      const data = await apiRequest("/register", "POST", { username, password });
      msg.textContent = data.message + " Redirecting to login...";
      setTimeout(() => {
        window.location.href = "login.html";
      }, 1000);
    } catch (err) {
      msg.textContent = err.message;
    }
  };
}

document.addEventListener("DOMContentLoaded", initRegister);
