public  {
    
}

// Dynamic greeting based on time
window.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header p');
    const hour = new Date().getHours();
    let greeting = "Welcome!";

    if (hour < 12) greeting = "Good morning!";
    else if (hour < 18) greeting = "Good afternoon!";
    else greeting = "Good evening!";

    const fullText = `${greeting} I'm Aditya Rajpoot, Web Developer | Designer | Programmer`;
    let i = 0;
    header.textContent = "";
    function typeWriter() {
        if (i < fullText.length) {
            header.textContent += fullText.charAt(i);
            i++;
            setTimeout(typeWriter, 40);
        }
    }
    typeWriter();
});

// Fade-in animation for sections
document.querySelectorAll('.section').forEach(section => {
    section.style.opacity = 0;
    section.style.transform = "translateY(40px)";
});
function revealSections() {
    document.querySelectorAll('.section').forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
            section.style.transition = "opacity 0.8s, transform 0.8s";
            section.style.opacity = 1;
            section.style.transform = "translateY(0)";
        }
    });
}
window.addEventListener('scroll', revealSections);
window.addEventListener('DOMContentLoaded', revealSections);

// Back to Top button
const backToTopBtn = document.createElement('button');
backToTopBtn.textContent = "↑ Top";
backToTopBtn.style.position = "fixed";
backToTopBtn.style.bottom = "32px";
backToTopBtn.style.right = "32px";
backToTopBtn.style.padding = "10px 18px";
backToTopBtn.style.fontSize = "1.1rem";
backToTopBtn.style.background = "#4e54c8";
backToTopBtn.style.color = "#fff";
backToTopBtn.style.border = "none";
backToTopBtn.style.borderRadius = "8px";
backToTopBtn.style.cursor = "pointer";
backToTopBtn.style.display = "none";
backToTopBtn.style.zIndex = "1000";
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTopBtn.style.display = "block";
    } else {
        backToTopBtn.style.display = "none";
    }
});

backToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Header color change on scroll
window.addEventListener('scroll', function() {
    const headerEl = document.querySelector('header');
    if (window.scrollY > 80) {
        headerEl.style.background = "#222";
        headerEl.style.transition = "background 0.3s";
    } else {
        headerEl.style.background = "linear-gradient(90deg, #333 60%, #4e54c8 100%)";
    }
});

// Firebase initialization
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.1.3/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.1.3/firebase-analytics.js";

const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
