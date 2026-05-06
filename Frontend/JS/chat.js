/**
 * ============================================
 * CARDKNOWLOGY — AI Chat Widget Controller
 * ============================================
 * 
 * Handles the floating chat interface logic.
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    // Toggle Chat Window
    chatToggle.addEventListener('click', () => {
        chatWindow.style.display = 'flex';
        chatToggle.style.display = 'none';
        chatInput.focus();
    });

    // Close Chat Window
    chatClose.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        chatToggle.style.display = 'flex';
    });

    // Send Message
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage(text, 'user');
        chatInput.value = '';

        // Add loading indicator
        const loadingId = addMessage('Thinking...', 'assistant loading');

        try {
            // Call AI Agent (via api.js)
            const response = await chat(text);
            
            // Remove loading and add response
            removeMessage(loadingId);
            addMessage(response.conversational_explanation || "I've processed your data.", 'assistant');
            
            // If the agent identified a disease, highlight it
            if (response.primary_disease && response.primary_disease !== "Undetermined") {
                addMessage(`🔍 Diagnostic Alert: ${response.primary_disease} (Confidence: ${(response.confidence_score * 100).toFixed(1)}%)`, 'assistant system-msg');
            }

        } catch (error) {
            removeMessage(loadingId);
            addMessage("Sorry, I'm having trouble connecting to the neural engine. Is the backend running?", 'assistant error');
            console.error(error);
        }
    }

    // Helper: Add message to UI
    function addMessage(text, type) {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = `message ${type}`;
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    // Helper: Remove message
    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Event Listeners
    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
