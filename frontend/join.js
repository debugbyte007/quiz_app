// join.js
async function checkQuizStart(code) {
  try {
    const data = await apiRequest(`/quizzes/${code}`);
    if (data.status === "started") {
      window.location.href = `play.html?code=${code}`;
    }
  } catch (_) {
    // ignore polling errors
  }
}

async function initJoin() {
  const message = $("join-message");

  $("btn-join-quiz").onclick = async () => {
    message.textContent = "";
    const code = $("quiz-code-input").value.trim();
    if (code.length !== 5) {
      message.textContent = "Please enter a 5-digit code.";
      return;
    }
    try {
      await apiRequest(`/quizzes/${code}/join`, "POST", {});
      const quiz = await apiRequest(`/quizzes/${code}`);
      $("waiting-section").classList.remove("hidden");
      $("waiting-quiz-title").textContent = quiz.title;
      $("waiting-quiz-host").textContent = quiz.host;

      setInterval(() => checkQuizStart(code), 2000);
    } catch (err) {
      message.textContent = err.message;
    }
  };
}

document.addEventListener("DOMContentLoaded", initJoin);
