// State
let currentUser = null;
let currentChatId = null;
let currentPersona = 'default';
let currentImageBase64 = null;

// Elements
const authOverlay = document.getElementById('auth-overlay');
const authForm = document.getElementById('auth-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const authError = document.getElementById('auth-error');
const userDisplay = document.getElementById('user-display');

const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const welcomeScreen = document.getElementById('welcome-screen');
const chatHistory = document.getElementById('chat-history');
const newChatBtn = document.getElementById('new-chat-btn');

const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');

const personaBtns = document.querySelectorAll('.persona-btn');

// --- Auth Logic ---
authForm.addEventListener('submit', (e) => e.preventDefault());

loginBtn.addEventListener('click', async () => {
    await handleAuth('/api/auth/login');
});

registerBtn.addEventListener('click', async () => {
    await handleAuth('/api/auth/register');
});

async function handleAuth(endpoint) {
    const username = usernameInput.value;
    const password = passwordInput.value;

    if (!username || !password) {
        showError("Please enter username and password");
        return;
    }

    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            if (endpoint.includes('register')) {
                // Auto login after register
                await handleAuth('/api/auth/login');
            } else {
                // Login Success
                currentUser = { id: data.user_id, username: data.username };
                userDisplay.textContent = currentUser.username;
                authOverlay.classList.add('hidden'); // Hide overlay
                loadChats();
            }
        } else {
            showError(data.detail);
        }
    } catch (e) {
        showError("Connection error");
    }
}

function showError(msg) {
    authError.textContent = msg;
    authError.classList.remove('hidden');
}

// --- Chat Logic ---
newChatBtn.addEventListener('click', async () => {
    if (!currentUser) return;
    try {
        const res = await fetch('/api/chats/new', {
            method: 'POST',
            headers: { 'user-id': currentUser.id }
        });
        const data = await res.json();
        currentChatId = data.chat_id;

        // Clear UI
        chatContainer.innerHTML = '';
        welcomeScreen.remove(); // Ensure welcome screen is gone

        // Refresh list
        loadChats();
    } catch (e) {
        console.error(e);
    }
});

async function loadChats() {
    if (!currentUser) return;
    const res = await fetch('/api/chats', {
        headers: { 'user-id': currentUser.id }
    });
    const chats = await res.json();

    chatHistory.innerHTML = '';
    chats.forEach(chat => {
        const btn = document.createElement('button');
        btn.className = 'w-full text-left px-4 py-3 rounded-2xl hover:bg-gray-700 text-sm text-gray-300 hover:text-white transition-all mb-2 border border-transparent hover:border-gray-600 truncate';
        btn.textContent = chat.title || 'New Chat';
        btn.onclick = () => loadChatHistory(chat.id);
        chatHistory.appendChild(btn);
    });
}

async function loadChatHistory(chatId) {
    currentChatId = chatId;
    const res = await fetch(`/api/chats/${chatId}/history`);
    const messages = await res.json();

    chatContainer.innerHTML = '';
    messages.forEach(msg => {
        addMessage(msg.content, msg.role, false, msg.image_data);
    });
    scrollToBottom();
}

// --- Messaging ---
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message && !currentImageBase64) return;

    if (welcomeScreen) welcomeScreen.remove();

    // Add User Message
    addMessage(message, 'user', false, currentImageBase64);

    const payload = {
        message: message || "Analyze this image",
        chat_id: currentChatId,
        model_name: document.getElementById('model-select').value,
        persona: currentPersona,
        image_data: currentImageBase64
    };

    // Clear Input
    userInput.value = '';
    clearImage();
    userInput.disabled = true;

    // Show Typing
    const typingId = addTypingIndicator();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'user-id': currentUser.id
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        removeMessage(typingId);

        if (res.ok) {
            addMessage(data.response, 'assistant');
            if (!currentChatId) {
                currentChatId = data.chat_id;
                loadChats(); // Refresh list to show new chat
            }
        } else {
            addMessage("Error: " + data.detail, 'assistant', true);
        }
    } catch (e) {
        removeMessage(typingId);
        addMessage("Network Error", 'assistant', true);
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
});

function addMessage(text, role, isError = false, image = null) {
    const div = document.createElement('div');
    div.className = `flex w-full ${role === 'user' ? 'justify-end' : 'justify-start'} message-enter mb-6`;

    const isUser = role === 'user';

    let imageHtml = '';
    if (image) {
        const src = image.startsWith('data:') ? image : `data:image/jpeg;base64,${image}`;
        imageHtml = `<img src="${src}" class="max-w-xs rounded-xl mb-2 border-2 border-white/10">`;
    }

    const content = `
        <div class="flex max-w-[85%] md:max-w-[75%] gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}">
            <div class="w-10 h-10 rounded-2xl flex-shrink-0 flex items-center justify-center shadow-lg transform hover:scale-110 transition-transform ${isUser ? 'bg-gray-700' : 'bg-gradient-to-br from-primary to-secondary'}">
                ${isUser ?
            '<span class="font-bold text-white">U</span>' :
            '<span class="text-xl">✨</span>'
        }
            </div>
            <div class="flex flex-col ${isUser ? 'items-end' : 'items-start'}">
                <div class="message-bubble px-6 py-4 rounded-3xl ${isUser ? 'bg-primary text-white rounded-tr-sm' : 'bg-gray-800 border border-gray-700 text-gray-100 rounded-tl-sm'} ${isError ? 'border-red-500 text-red-400' : ''} shadow-md">
                    ${imageHtml}
                    <p class="text-[15px] leading-relaxed whitespace-pre-wrap font-medium">${text}</p>
                </div>
                <span class="text-[10px] text-gray-500 mt-2 px-2 font-bold opacity-60 uppercase tracking-wider">Just now</span>
            </div>
        </div>
    `;

    div.innerHTML = content;
    chatContainer.appendChild(div);
    scrollToBottom();
}

// --- Image Handling ---
uploadBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            currentImageBase64 = e.target.result;
            previewImg.src = currentImageBase64;
            imagePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

removeImageBtn.addEventListener('click', clearImage);

function clearImage() {
    currentImageBase64 = null;
    fileInput.value = '';
    imagePreview.classList.add('hidden');
}

// --- Persona Handling ---
personaBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        personaBtns.forEach(b => {
            b.classList.remove('border-primary', 'active');
            b.classList.add('border-transparent');
        });
        btn.classList.add('border-primary', 'active');
        btn.classList.remove('border-transparent');
        currentPersona = btn.dataset.persona;
    });
});

// --- Utils ---
function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'flex w-full justify-start message-enter mb-6';
    div.innerHTML = `
        <div class="flex max-w-[80%] gap-4">
            <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex-shrink-0 flex items-center justify-center shadow-lg">
                <span class="text-xl">✨</span>
            </div>
            <div class="px-6 py-5 rounded-3xl bg-gray-800 border border-gray-700 rounded-tl-sm shadow-md flex items-center gap-2">
                <div class="w-2.5 h-2.5 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2.5 h-2.5 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2.5 h-2.5 bg-gray-400 rounded-full typing-dot"></div>
            </div>
        </div>
    `;
    chatContainer.appendChild(div);
    scrollToBottom();
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
