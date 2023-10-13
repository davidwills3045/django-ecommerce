console.log("how fine");

$("#commentForm").submit(function(e){
    e.preventDefault(); 

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
            }
        }
    })
})