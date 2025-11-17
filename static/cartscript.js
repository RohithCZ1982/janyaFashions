let popupItem = {};
let cart = JSON.parse(localStorage.getItem('jf_cart')) || [];

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
  cart = JSON.parse(localStorage.getItem('jf_cart')) || [];
  document.getElementById("floatingCartCount").innerText = cart.length;

  const cartBox = document.getElementById("cartItems");
  cartBox.innerHTML = "";

  let total = 0; // ✅ to calculate total amount

  cart.forEach((item, i) => {
    total += item.price; // ✅ add item price to total

    cartBox.innerHTML += `
      <div class="cart-item">
      <img src="${item.image}" alt="${item.name}" />
        <b>${item.name}</b> <br>
        💰 ₹${item.price} <br>
        <button class="remove-btn" onclick="removeFromCart(${i})">Remove</button>
      </div>
    `;
  });

  // ✅ show total amount in cart
  cartBox.innerHTML += `
    <div style="margin-top:10px; padding:8px; font-weight:bold; background:#ffe6f0; border-radius:6px;">
      Total Amount: ₹${total}
    </div>
  `;
}

