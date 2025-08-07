// Example dynamic pricing logic
const basePrice = 1000;
const discountRate = 0.15; // 15% discount

function calculatePrice() {
  const currentHour = new Date().getHours();
  let finalPrice = basePrice;

  // Apply discount during off-peak hours
  if (currentHour >= 22 || currentHour <= 6) {
    finalPrice = basePrice * (1 - discountRate);
  }

  return finalPrice.toFixed(2);
}

// Simulate fetching product data from Shopify
const productData = {
  title: "Smartwatch Pro",
  image: "https://via.placeholder.com/300",
};

document.getElementById("product-title").textContent = productData.title;
document.getElementById("product-image").src = productData.image;
document.getElementById("product-price").textContent = `Price: ₹${calculatePrice()}`;

document.getElementById("buy-button").addEventListener("click", () => {
  alert("Redirecting to Shopify checkout...");
  // You would use Shopify's Buy SDK or redirect to the checkout URL here
});