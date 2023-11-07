console.log("how fine");

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
  "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault(); 

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("comment saved to DB.....");

            if (res.bool == true) {
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

               let _html =  '<div class="single-comment justify-content-between d-flex mb-30">'
                   _html += '<div class="user justify-content-between d-flex">'
                   _html += '<div class="thumb text-center">'
                   _html += '<img src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg" alt="" />'
                   _html += '<a href="#" class="font-heading text-brand">'+ res.context.user+'</a>'
                   _html += '</div>'

                   _html += '<div class="desc">'
                   _html += '<div class="d-flex justify-content-between mb-10">'
                   _html += '<div class="d-flex align-items-center">'
                   _html += '<span class="font-xs text-muted">'+ time +'</span>'
                   _html += '</div>'

                   for (let i=1; i<=res.context.rating ; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>'
                   }

                   _html += '</div>'
                   _html += '<p class="mb-10">'+ res.context.review +'</p>'

                   _html += '</div>'
                   _html += '</div>'
                   _html += '</div>'
                
                   $(".comment-list").prepend(_html) 
            }

        }
    })
})


$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click",function() {
        console.log("a check box has been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min") 
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $(".filter-checkbox").each(function() {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log(filter_value,filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+  filter_key +']:checked')).map(function(element){
                return element.value
            })
        })      
        console.log(filter_object);
        $.ajax({
            url:'http://127.0.0.1:8000/filter-product/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("sending data....");
            },
            success: function(response) {
                console.log(response);
                $("#filtered-product").html(response.data)
            }
        })
    })
    $("#max_price").on("blur", function() {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            min_Price = Math.round(min_price * 100) / 100
            max_Price = Math.round(max_price * 100) / 100
            alert("price must be between $"+min_Price+ " and $"+ max_Price)
            $(this).val(min_Price)
            $("#range").val(min)

            $(this).focus()
            return false
        }

    })

    // Add to cart functionality 
    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
        

        console.log("quantity:",quantity);
        console.log("product_title:",product_title);
        console.log("product_id:",product_id);
        console.log("product_pid:",product_pid);
        console.log("product_image:",product_image);
        console.log("product_index:",index);
        console.log("product_price:",product_price);
        console.log("Current Element:",this_val);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'pid': product_pid,
                'image': product_image,
                
            },
            dataType:'json',
            beforeSend: function () {
                console.log("Adding Product to Cart....");
            },
            success: function (response) {
                this_val.html("✓")
                console.log("Added Product to Cart!");
                $('.cart-items-count').text(response.totalcartitems)
            }
    })  })

    $(".delete-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("id: ",product_id);
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':product_id
            },
            dataType:'json',
            beforeSend:function () {
                this_val.hide()
            },
            success:function (response) {
                console.log(response);
                this_val.show()
                $('.cart-items-count').text(response.totalcartitems)
                $("#cartList").html(response.data)
    
    
            }
        })
    })

    $(".update-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_qty = $(".product-qty-"+product_id).val()
    
        console.log("id: ",product_id);
        console.log("qty: ",product_qty);
        $.ajax({
            url:'/update-cart',
            data:{
                'id':product_id,
                'qty':product_qty
            },
            dataType:'json',
            beforeSend:function () {
                this_val.hide()
            },
            success:function (response) {
                // console.log(response);
                this_val.show()
                $('.cart-items-count').text(response.totalcartitems)
                $("#cart-list").html(response.data)
    
    
            }
        })
    })

})






