// const staffOpenChatBtn = document.getElementById('staff-open-chat')
// async function activateChat() {
//     const response = await fetch('/chat/activate/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             'chat_id': chatId
//         })
//     })

//     const data = await response.json();
//     return data;
// }

// staffOpenChatBtn.onclick = async function(e) {
//     data = await activateChat();
//     console.log(data);
// }