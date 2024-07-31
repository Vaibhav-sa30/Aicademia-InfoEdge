// Select the video element
const video = document.getElementById('video-bg');

// Listen for scroll events on the webpage
window.addEventListener('scroll', function() {
    // Calculate the blur or whitening effect based on scroll position
    const scrollPosition = window.scrollY;
    const blurAmount = scrollPosition / 50; // Adjust as needed for desired blur effect

    // Apply CSS changes to the video element
    video.style.filter = `blur(${blurAmount}px)`;
});


// Select the navbar element
const navbar = document.getElementById('navbar');

// Listen for scroll events on the window
window.addEventListener('scroll', function() {
    // Get the current scroll position
    const scrollPosition = window.scrollY;

    // Determine the threshold scroll position for adding the opaque class
    const threshold = 100; // Adjust as needed

    // Check if the scroll position exceeds the threshold
    if (scrollPosition > threshold) {
        // Add the opaque class to the navbar
        navbar.classList.add('opaque');
    } else {
        // Remove the opaque class from the navbar
        navbar.classList.remove('opaque');
    }
});

window.addEventListener('scroll', function() {
    var scrollButton = document.getElementById('scroll-button');
    if (window.pageYOffset > 100) { // Adjust the scroll threshold as needed
        scrollButton.style.display = 'block'; // Show the button when scrolling down
    } else {
        scrollButton.style.display = 'none'; // Hide the button when scrolling back to top
    }
});


