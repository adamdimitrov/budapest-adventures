/* ==========================================
   BUDAPEST PROSECCO CRUISE INTERACTIVE LOGIC
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Dynamic Filtering Logic
    const filterButtons = document.querySelectorAll(".filter-btn");
    const cruiseCards = document.querySelectorAll(".cruise-card");

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove("active"));
            
            // Add active class to clicked button
            button.classList.add("active");

            const filterValue = button.getAttribute("data-filter");

            cruiseCards.forEach(card => {
                const cardCategory = card.getAttribute("data-category");

                if (filterValue === "all" || cardCategory === filterValue) {
                    // Show card with fade effect
                    card.style.display = "flex";
                    setTimeout(() => {
                        card.style.opacity = "1";
                        card.style.transform = "translateY(0)";
                    }, 50);
                } else {
                    // Hide card
                    card.style.opacity = "0";
                    card.style.transform = "translateY(15px)";
                    setTimeout(() => {
                        card.style.display = "none";
                    }, 300);
                }
            });
        });
    });

    // 2. Comparison Table Highlight Logic
    const tableRows = document.querySelectorAll(".comparison-table tbody tr");

    tableRows.forEach(row => {
        row.addEventListener("click", () => {
            row.classList.toggle("highlighted");
        });
    });

    // 3. Simple scroll reveal effect for tips
    const tipCards = document.querySelectorAll(".tip-card");
    const revealOnScroll = () => {
        const triggerBottom = window.innerHeight * 0.9;
        
        tipCards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            
            if (cardTop < triggerBottom) {
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
            }
        });
    };

    // Set initial state for tip animation
    tipCards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";
        card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    });

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll(); // run once on load
});
