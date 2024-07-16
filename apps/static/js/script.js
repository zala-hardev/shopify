document.addEventListener('DOMContentLoaded', function () {
  const menuButton = document.querySelector('#mobile-menu-button');
  const mobileMenu = document.querySelector('#mobile-menu');

  menuButton.addEventListener('click', function () {
    mobileMenu.classList.toggle('hidden');
  });

  /* Logout */

  /* endof Logout */


  /* Category - All,Mobile,Laptops,Headphone,Smartwatch */
  const categoryBtn = document.getElementById("categoryBtn");
  const categoryDropdown = document.getElementById("categoryDropdown");

  // Hide dropdown initially
  categoryDropdown.classList.add("hidden");

  // Toggle dropdown on button click
  categoryBtn.addEventListener("click", function () {
    categoryDropdown.classList.toggle("hidden");
  });
  /* End of Category Menu */

  /* Orders - All,Present Orders,Past Orders 
  const ordersBtn = document.getElementById("ordersBtn");
  const ordersDropdown = document.getElementById("ordersDropdown");

  // Hide dropdown initially
  ordersDropdown.classList.add("hidden");

  // Toggle dropdown on button click
  ordersBtn.addEventListener("click", function () {
    ordersDropdown.classList.toggle("hidden");
  });
  /* End of Category Menu */

  /* Hide dropdown when clicking outside of it */
  document.addEventListener("click", function (event) {
    if (!categoryBtn.contains(event.target) && !categoryDropdown.contains(event.target)) {
      categoryDropdown.classList.add("hidden");
    }
  });

  /* WishList */

  /* EndOf WishList */

  /* To increarse and decrease the quantity of cart's product */


})