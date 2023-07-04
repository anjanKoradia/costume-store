// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("click", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

// access cookies
function getCookie(name) {
  const cookies = document.cookie.split(';');
  
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  
  return null;
}

// delete product
function delete_product(url) {
  flag =  confirm("Are you sure you want delete this product ?");

  if(flag){
    fetch(url,{
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
    }).then(() => {
      window.location.href = "/vendor"
    })
  }
}

let alertCloseBtn = document.getElementById("alert_message_close")
console.log(alertCloseBtn);
if(alertCloseBtn){
  setTimeout(() => {
    alertCloseBtn.click();
  }, 3000);
}