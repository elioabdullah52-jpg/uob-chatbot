const chatBody = document.getElementById("chatBody");
const msg = document.getElementById("msg");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, who) {
  const row = document.createElement("div");
  row.className = "row " + who;

  const wrap = document.createElement("div");

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = (who === "user" ? "You" : "Bot") + " • " + timeNow();

  wrap.appendChild(bubble);
  wrap.appendChild(meta);
  row.appendChild(wrap);

  chatBody.appendChild(row);
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
  const question = msg.value.trim();
  if (!question) return;

  sendBtn.disabled = true;

  addMessage(question, "user");
  msg.value = "";

  addMessage("Typing...", "bot");
  const typingRow = chatBody.lastChild;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    typingRow.remove();

    addMessage(data.answer || "No answer received.", "bot");
  } catch (err) {
    typingRow.remove();
    addMessage("Network or server error.", "bot");
  } finally {
    sendBtn.disabled = false;
    msg.focus();
  }
}

async function clearChat() {
  chatBody.innerHTML = "";

  try {
    await fetch("/api/clear", { method: "POST" });
  } catch (err) {}

  addMessage("Hi! I’m the UoB Canvas Accessibility Bot. How can I help?", "bot");
}

sendBtn.onclick = sendMessage;

msg.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

clearBtn.onclick = clearChat;

document.getElementById("chips").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-q]");
  if (!b) return;
  msg.value = b.dataset.q;
  sendMessage();
});

addMessage("Hi! I’m the UoB Canvas Accessibility Bot. Ask me about reading help, formats, quizzes, focus, or support contacts.", "bot");
