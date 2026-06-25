async function sendMessage() {

    const input = document.getElementById("user-input");

    const chatBox = document.getElementById("chat-box");

    const message = input.value;

    if(message === "")
        return;

    chatBox.innerHTML += `
<div class="user-message">
You: ${message}
</div>
`;

    const response = await fetch("/chat", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })
    });

    const data = await response.json();

    chatBox.innerHTML += `
<div class="bot-message">
Bot: ${data.response}
</div>
`;

    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";
}
document
.getElementById("user-input")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){
        sendMessage();
    }

});