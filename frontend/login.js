// login.js
async function initLogin() {
  $("btn-login").onclick = async () => {
    const msg = $("login-message");
    msg.textContent = "";
    try {
      const username = $("login-username").value.trim();
      const password = $("login-password").value;
      const data = await apiRequest("/login", "POST", { username, password });
      msg.textContent = data.message;
      window.location.href = "index.html";
    } catch (err) {
      msg.textContent = err.message;
      if (err.message.toLowerCase().includes("not found")) {
        msg.textContent += " Please register first.";
      }
    }
  };
}

document.addEventListener("DOMContentLoaded", initLogin);
