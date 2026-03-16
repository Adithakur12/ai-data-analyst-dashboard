/* Smooth transition for all interactive elements */
.destination-card,
.filter-btn,
.add-favorite,
.book-now,
#ai-recommend-btn,
#search-btn,
#chatbot,
#send-chat {
    transition: all 0.3s ease;
}

/* Destination card hover: elevate with shadow and scale */
.destination-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

/* Filter buttons: active and hover states */
.filter-btn:hover:not(.bg-green-600) {
    background-color: #34d399; /* Tailwind emerald-400 */
    color: white;
    cursor: pointer;
}

.filter-btn.bg-green-600 {
    box-shadow: 0 0 8px #34d399;
}

/* Add favorite button: toggle heart color and scale */
.add-favorite {
    cursor: pointer;
}
.add-favorite:hover {
    transform: scale(1.2);
}

/* Book now buttons: subtle shadow and scale on hover */
.book-now:hover {
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.5);
    transform: scale(1.05);
}

/* AI Recommendation button: pulse animation on hover */
#ai-recommend-btn:hover {
    animation: pulse 1.5s infinite;
    box-shadow: 0 0 15px #fbbf24;
}

/* Pulse keyframes */
@keyframes pulse {
    0%, 100% {
        box-shadow: 0 0 15px #fbbf24;
    }
    50% {
        box-shadow: 0 0 30px #fbbf24;
    }
}

/* Search input focus */
#search-input:focus {
    outline: none;
    box-shadow: 0 0 8px #10b981;
    border-color: #10b981;
}

/* Chatbot button: subtle bounce animation on hover */
#chatbot:hover {
    animation: bounce 0.6s ease-in-out;
    box-shadow: 0 0 12px #059669;
}

/* Bounce keyframes */
@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-6px);
    }
}

/* Chat window scrollbar styling */
#chat-messages::-webkit-scrollbar {
    width: 6px;
}
#chat-messages::-webkit-scrollbar-thumb {
    background-color: #10b981;
    border-radius: 3px;
}

/* Map points: add subtle shadow and smooth transform */
.map-point {
    box-shadow: 0 0 5px rgba(220, 38, 38, 0.7);
    transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}

.map-point:hover {
    box-shadow: 0 0 12px rgba(234, 88, 12, 0.9);
}

/* Header nav links: underline on hover */
nav ul li a:hover {
    text-decoration: underline;
}

/* Footer social icons: scale and color transition */
footer a {
    transition: color 0.3s ease, transform 0.3s ease;
}
footer a:hover {
    color: #bbf7d0; /* Tailwind emerald-200 */
    transform: scale(1.2);
}

/* Form inputs and textarea: smooth focus ring */
input:focus, textarea:focus {
    outline: none;
    box-shadow: 0 0 6px #059669;
    border-color: #059669;
}

/* Smooth fade-in for search results */
#search-results {
    animation: fadeIn 0.4s ease forwards;
}

/* FadeIn keyframes */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}