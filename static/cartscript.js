let popupItem = {};
let cart = [];

updateCartUI();

function openPreview(name, price, image) {
  popupItem = { name, price, image };

  document.getElementById("popupImage").src = image;
  document.getElementById("popupName").innerText = name;
  document.getElementById("popupPrice").innerText = "₹" + price;

  document.getElementById("previewPopup").style.display = "flex";
}

function closePreview() {
  document.getElementById("previewPopup").style.display = "none";
}

function addPopupToCart() {
  addToCart(popupItem.name, popupItem.price, popupItem.image);
  closePreview();
}

function addToCart(name, price, image) {
  cart.push({name, price, image});
  localStorage.setItem('jf_cart', JSON.stringify(cart));
  updateCartUI();
}

function removeFromCart(index) {
  cart.splice(index, 1);
  localStorage.setItem('jf_cart', JSON.stringify(cart));
  updateCartUI();
}

function emptyCart() {
  if (confirm("Clear your entire cart?")) {
    cart = [];
    localStorage.removeItem("jf_cart");   // ✅ delete from browser storage
    updateCartUI();                       // refresh UI
  }
}

function updateCartUI() {
  const container = document.getElementById("cartItems");
  container.innerHTML = "";

  cart.forEach((item, index) => {
    const div = document.createElement("div");
    div.classList.add("cart-item");

    div.innerHTML = `
      <img src="${item.image}" alt="">
      <div class="cart-item-info">
        <strong>${item.name}</strong><br>
        💰₹${item.price}
      </div>
      <div class="cart-item-remove" onclick="removeFromCart(${index})">×</div>
    `;

    container.appendChild(div);
  });
 
  document.getElementById("floatingCartCount").innerText = cart.length;
 
}

