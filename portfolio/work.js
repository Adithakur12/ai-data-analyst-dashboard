// Project data
const projects = [
    {
        title: "Project 1",
        description: "A web application built with React and Node.js.",
        image: "https://via.placeholder.com/300x200",
        liveLink: "#",
        codeLink: "#"
    },
    {
        title: "Project 2",
        description: "An e-commerce site using HTML, CSS, and JavaScript.",
        image: "https://via.placeholder.com/300x200",
        liveLink: "#",
        codeLink: "#"
    },
    {
        title: "Project 3",
        description: "A portfolio website with modern design.",
        image: "https://via.placeholder.com/300x200",
        liveLink: "#",
        codeLink: "#"
    }
];

// Function to create project cards
function createProjectCards() {
    const projectsGrid = document.getElementById('projects-grid');

    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';

        projectCard.innerHTML = `
            <div class="project-image">
                <img src="${project.image}" alt="${project.title}">
            </div>
            <div class="project-content">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="project-links">
                    <a href="${project.liveLink}" class="btn" target="_blank">Live Demo</a>
                    <a href="${project.codeLink}" class="btn" target="_blank">View Code</a>
                </div>
            </div>
        `;

        projectsGrid.appendChild(projectCard);
    });
}

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    createProjectCards();
});
