// Plant Hub Main Interactions

document.addEventListener('DOMContentLoaded', () => {

    // Navbar Scroll Effect
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth Scrolling for Anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Fetch Plants from Backend
    const plantGrid = document.querySelector('#shop .grid');
    if (plantGrid) {
        fetch('http://localhost:5000/api/plants')
            .then(response => response.json())
            .then(plants => {
                plantGrid.innerHTML = ''; // Clear placeholders
                plants.forEach(plant => {
                    const card = document.createElement('div');
                    card.className = 'glass-panel plant-card fade-in';
                    card.innerHTML = `
                        <div class="card-img-container">
                            <img src="${plant.image_url}" alt="${plant.name}" class="card-img">
                        </div>
                        <div class="card-details">
                            <h3 class="card-title">${plant.name}</h3>
                            <div class="card-price">$${plant.price}</div>
                            <div class="card-actions">
                                <span class="difficulty-badge">${plant.difficulty}</span>
                                <button class="btn btn-primary" onclick="addToCart(${plant.id})">
                                    <i class="fa-solid fa-cart-shopping"></i>
                                </button>
                            </div>
                        </div>
                    `;
                    plantGrid.appendChild(card);
                });
            })
            .catch(err => {
                console.warn('Backend API not reachable. Showing static content.', err);
                // Keep the static placeholders if API fails
            });
    }

    // Add to Cart Animation Placeholder

    const addToCartBtns = document.querySelectorAll('.btn-primary i.fa-cart-shopping');

    addToCartBtns.forEach(icon => {
        icon.parentElement.addEventListener('click', function () {
            const btn = this;
            const originalHTML = btn.innerHTML;

            btn.innerHTML = '<i class="fa-solid fa-check"></i>';
            btn.style.background = 'var(--color-success)';
            btn.style.color = 'white';

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.style.background = '';
                btn.style.color = '';
            }, 2000);

            // In a real app, this would update cart state
            console.log('Item added to cart!');
        });
    });
});
