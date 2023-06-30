let csrfToken = $.cookie("csrftoken");

/*-------------------
	Cart Item Quantity
	--------------------- */
$("[id='cart_item_quantity']").click(function () {
  let element = $(this);
  let url = element.data("url");
  let operation = element.data("operation");
  let id = element.data("id");

  $.ajax({
    url: url,
    method: "PATCH",
    data: JSON.stringify({
      operation: operation,
      id: id,
    }),
    contentType: "application/json",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    success: function (response) {
      let { quantity, item_price, total_price, cart_count } = response;

      if (cart_count == 0) {
        window.location.reload();
        return;
      }

      if (operation == "delete" || quantity == 0) {
        element.parent().parent().remove();
        new Noty({
          theme: "metroui",
          type: "success",
          text: "Item removed successfully",
          timeout: 1000,
        }).show();
      }

      element.siblings("#item_quantity").val(quantity);
      element
        .parent()
        .parent()
        .siblings("#item_total_price")
        .text("₹ " + item_price * quantity);
      $("#cart_subtotal").text("₹ " + total_price);
      $("#cart_total").text("₹ " + total_price);
      $("#cart_count").text(cart_count);
    },
    error: function (xhr, status, error) {
      new Noty({
        theme: "metroui",
        type: "error",
        text: error,
        timeout: 1000,
      }).show();
    },
  });
});

/*-------------------
	Handel Add to Cart Operation
	--------------------- */
$("#add_to_cart").submit(function (e) {
  e.preventDefault();
  let url = $(this).attr("action");
  let data = $(this).serialize();

  $.ajax({
    url: url,
    method: "POST",
    data: data,
    success: function (response) {
      let { message, redirect_url } = response;
      new Noty({
        theme: "metroui",
        type: "success",
        text: message,
        timeout: 1000,
      }).show();

      setTimeout(function () {
        window.location.href = redirect_url;
      }, 1000);
    },
    error: function (xhr, status, error) {
      let message = xhr.responseJSON[0];
      new Noty({
        theme: "metroui",
        type: "error",
        text: message,
        timeout: 1000,
      }).show();
    },
  });
});

/*-------------------
	Handel Add/Remove to Wishlist
	--------------------- */
$("[id='wishlist_btn']").click(function () {
  let btn = $(this);
  let url = btn.data("url");
  let operation = btn.data("operation");
  let id = btn.data("id");

  $.ajax({
    url: url,
    method: "POST",
    data: JSON.stringify({
      operation: operation,
      id: id,
    }),
    contentType: "application/json",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    success: function (response) {
      if (
        response.items_count == 0 &&
        window.location.href.includes("wishlist")
      ) {
        window.location.reload();
        return;
      }

      if (operation == "add") {
        btn.html('<i class="fa fa-heart" aria-hidden="true"></i>');
        btn.data("operation", "remove");
        new Noty({
          theme: "metroui",
          type: "success",
          text: response.message,
          timeout: 1000,
        }).show();
        return;
      }

      if (operation == "remove" && btn.hasClass("wishlist_item_remove_btn")) {
        btn.parent().parent().remove();
        new Noty({
          theme: "metroui",
          type: "error",
          text: response.message,
          timeout: 1000,
        }).show();
        return;
      }

      if (operation == "remove") {
        btn.html('<i class="fa fa-heart-o" aria-hidden="true"></i>');
        btn.data("operation", "add");
        new Noty({
          theme: "metroui",
          type: "error",
          text: response.message,
          timeout: 1000,
        }).show();
        return;
      }
    },
  });
});


// $(".product_price_range").on("input", function(e){
//   let price = $(this).val();
//   let url = window.location.href
//   $.ajax({
//     url: url,
//     method: "GET",
//     data: {
//       price: price,
//     },
//     contentType: "application/json",
//     headers: {
//       "X-CSRFToken": csrfToken,
//     },
//     success: function (response) {
//       console.log(response);
//     }
//   })
// })