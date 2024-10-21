let chatHistory = [];

document.addEventListener('DOMContentLoaded', function() {
  const chatForm = document.getElementById('chat-form');
  chatForm.addEventListener('submit', function(event) {
    event.preventDefault();
    sendMessage();
  });

  const inputElement = document.getElementById('user-input');
  inputElement.addEventListener('keypress', function(event) {
    // 13 is the key code for the Enter key
    if (event.keyCode === 13) {
      // Prevent the default Enter key action
      event.preventDefault();
      // Call the sendMessage function
      sendMessage();
    }
  });
});

function showTypingIndicator() {
  addToMessageList('Bot', 'Agent is typing...');
}

function sendMessage() {
  const inputElement = document.getElementById('user-input');
  const message = inputElement.value;
  inputElement.value = '';
  inputElement.focus();
  if (!message.trim()) return;
  addToMessageList('You', message);

  showTypingIndicator(); // Show the typing indicator
  fetch('/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question: message })
  })
  .then(response => response.json())
  .then(data => {
    removeTypingIndicator(); // Remove the typing indicator
    addToMessageList('Bot', data.answer);
    chatHistory.push({
        'user': message,
        'bot': data.answer
    });
  })
  .catch(error => {
    console.error('Error:', error);
    removeTypingIndicator(); // Also remove the typing indicator in case of an error
  });
}

function removeTypingIndicator() {
  const messagelistElement = document.getElementById('message-list');
  const typingIndicator = document.querySelector('.typing-indicator');
  if (typingIndicator) {
    messagelistElement.removeChild(typingIndicator);
  }
}

function addToMessageList(sender, message) {
  const messagelistElement = document.getElementById('message-list');

  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');

  if (sender === 'You') {
    messageDiv.classList.add('usermessage');
  } else if (sender === 'Bot') {
    if (message === 'Agent is typing...') {
      messageDiv.classList.add('typing-indicator'); // Use a special class for the typing indicator
    } else {
      messageDiv.classList.add('apimessage');
    }
  }

  const messageContent = document.createElement('div');
  messageContent.classList.add('message-content');
  messageContent.textContent = message;
  messageDiv.appendChild(messageContent);
  messagelistElement.appendChild(messageDiv);
  messagelistElement.scrollTop = messagelistElement.scrollHeight; // Scroll to the new message
}