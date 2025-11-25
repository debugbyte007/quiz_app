// app.js
if (typeof $ === "undefined") {
  function $(id) {
    return document.getElementById(id);
  }
}

async function init() {
  const welcomeSection = $("welcome-section");
  const homeMessage = $("home-message");
  const loadingSection = $("loading-section");

  try {
    const me = await apiRequest("/me");
    if (me.authenticated) {
      welcomeSection.classList.remove("hidden");
      if (loadingSection) loadingSection.classList.add("hidden");
      $("welcome-text").textContent = `Welcome, ${me.username}`;

      const storedName = localStorage.getItem("quiz_display_name") || "";
      if (storedName && $("display-name")) {
        $("display-name").value = storedName;
      }
    } else {
      // Not logged in, send to login screen
      window.location.href = "login.html";
      return;
    }
  } catch (_) {
    // If /me fails, treat as not logged in
    window.location.href = "login.html";
    return;
  }

  if ($("btn-save-name")) {
    $("btn-save-name").onclick = () => {
      const name = $("display-name").value.trim();
      localStorage.setItem("quiz_display_name", name);
      homeMessage.textContent = "Name saved.";
    };
  }

  if ($("btn-host")) {
    $("btn-host").onclick = () => {
      window.location.href = "host.html";
    };
  }

  if ($("btn-join")) {
    $("btn-join").onclick = () => {
      window.location.href = "join.html";
    };
  }

  if ($("btn-history")) {
    $("btn-history").onclick = async () => {
      try {
        const data = await apiRequest("/history");
        alert(`You have participated in ${data.results.length} quizzes.`);
      } catch (err) {
        homeMessage.textContent = err.message;
      }
    };
  }

  if ($("btn-logout")) {
    $("btn-logout").onclick = async () => {
      try {
        await apiRequest("/logout", "POST");
      } catch (_) {
        // ignore errors on logout
      }
      window.location.reload();
    };
  }
}

document.addEventListener("DOMContentLoaded", init);
