function toggleMenu() {
  document.getElementById("smallMenu").classList.toggle("open");
}

  // Close image popup on ESC key press
document.addEventListener("keydown", function(event) {
    if (event.key == "Escape") {
       closePreview();
  }
});

function openWhatsApp(){
  const phone = "918792507355";
  const message = encodeURIComponent("Hi Janya Fashions!");
  const appURL = `whatsapp://send?phone=${phone}&text=${message}`;
  const webFallback = `https://wa.me/${phone}?text=${message}`;
  
  window.location.href = appURL;
  
  setTimeout(() => {
    window.open(appURL, "_blank", "noopener");
  }, 1000);
}

function toggleCart() {
  document.getElementById("cartSidebar").classList.toggle("open");
}

function closeCart() {
  document.getElementById("cartSidebar").classList.remove("open");
}


function scrollLeftDiv(id) {
  document.getElementById(id).scrollBy({ left: -260, behavior: "smooth" });
}

function scrollRightDiv(id) {
  document.getElementById(id).scrollBy({ left: 260, behavior: "smooth" });
}

let message = "Hi, I want to order:\n\n";
  cart.forEach(c => {
    message += `🛍 ${c.name}\n₹${c.price}  |  ${c.code}\n\n`;
  });

  function checkoutWhatsApp() {
  if(cart.length === 0) {
    alert("Cart is empty!");
    return;
  }

  let message = "Hi, I want to order:\n\n";
  let total = 0;

  cart.forEach(c => {
    message += `🛍 ${c.name}\n💰 ₹${c.price}\n🏷 ${c.code}\n\n`;
    total += c.price;
  });

  message += `✅ Total Amount: ₹${total}\n\nPlease confirm the order.`;

  let phone = "919876543210"; // ✅ replace with your number
  let url = `https://wa.me/${phone}?text=` + encodeURIComponent(message);
  window.open(url, "_blank");
}


// Close cart when clicking outside it
document.addEventListener("click", function (event) {
  const cartSidebar = document.getElementById("cartSidebar");
  const cartBtn = document.querySelector(".cart-btn");

  // if sidebar is open, and click is NOT inside it or on the cart button
  if (
    cartSidebar.classList.contains("open") &&
    !cartSidebar.contains(event.target) &&
    !cartBtn.contains(event.target)
  ) {
    cartSidebar.classList.remove("open");
  }
});

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}

function loadWomenImages(womenImages) {
  const track = document.getElementById("womenTrack");
  if (!track || !Array.isArray(womenImages)){
    alert("no track");
    return;
  } 
 
  womenImages.forEach((filename, idx) => {
    const name = filename.split('.').shift();  
    const parts = name.split('-');   
    const amount = parseInt(parts.pop(), 10); 
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
       <img src="/static/images/women/${filename}" alt="${filename}"  class="product-img" onclick="openPreview('Women Dress ${idx + 1}', ${amount}, this.src)">
    `;
    track.appendChild(card);
  });
}

function loadKidsImages(kidsImages) {
  const track = document.getElementById("kidsTrack");
  if (!track || !Array.isArray(kidsImages)){
    alert("no track");
    return;
  } 
  
    kidsImages.forEach((filename, idx) => {
    const name = filename.split('.').shift();  
    const parts = name.split('-');                 // ["dress", "2500"]
    const amount = parseInt(parts.pop(), 10); 
  
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
       <img src="/static/images/kids/${filename}" alt="${filename}"  class="product-img" onclick="openPreview('Kids Dress ${idx + 1}', ${amount} , this.src)">
    `;
    track.appendChild(card);
  });
}


