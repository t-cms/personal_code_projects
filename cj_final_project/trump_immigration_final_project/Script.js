 // Change background when scrolling past a certain point
  window.addEventListener('scroll', function() {
    const scrollPos = window.scrollY;

    if(scrollPos < window.innerHeight) {
      // First section (red/blue)
      document.body.style.background = "linear-gradient(to right, #ff4d4d 50%, #4d79ff 50%)";
    } else {
      // After scrolling down, show muted image
      document.body.style.background = "url('muted_background.jpg')";
      document.body.style.backgroundSize = "cover";
      document.body.style.backgroundPosition = "center";
    }
  });