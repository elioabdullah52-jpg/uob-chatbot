const chatBody = document.getElementById("chatBody");
const msg = document.getElementById("msg");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

function addMessage(text, who){
    const row = document.createElement("div");
    row.className = "row " + who;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    row.appendChild(bubble);
    chatBody.appendChild(row);

    chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage(){
    const question = msg.value.trim();
    if(!question) return;

    addMessage(question, "user");
    msg.value = "";

    addMessage("Typing...", "bot");
    const typing = chatBody.lastChild;

    try{
        const res = await fetch("/api/chat", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({question})
        });

        const data = await res.json();
        typing.remove();

        addMessage(data.answer, "bot");

    }catch(err){
        typing.remove();
        addMessage("Server error.", "bot");
    }
}

sendBtn.onclick = sendMessage;

msg.addEventListener("keydown", function(e){
    if(e.key === "Enter" && !e.shiftKey){
        e.preventDefault();
        sendMessage();
    }
});

clearBtn.onclick = async function(){
    chatBody.innerHTML = "";
    await fetch("/api/clear", {method:"POST"});
};
