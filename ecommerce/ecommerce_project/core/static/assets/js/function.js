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
    $(".filter-checkbox").on("click",function() {
        console.log("a check box has been clicked");

        let filter_object = {}

        $(".filter-checkbox").each(function() {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log("filter value is:", filter_value);
            // console.log("filter value is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+  filter_key +']:checked')).map(function(element){
                return element.value
            })
        })
        console.log(filter_object);
        $.ajax({
            url:'/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("sending data....");
            },
            success: function(response) {
                console.log(response );
            }
        })
    })
}) 