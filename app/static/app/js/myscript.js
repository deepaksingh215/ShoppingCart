 $('#slider1, #slider2, #slider3,#slider4,#slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    console.log("plus Clicked")
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log(id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success: function(data) {
            console.log(data)
            console.log("success")
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.minus-cart').click(function(){
    console.log('minus clicked')
    var id = $(this).attr('pid').toString();
    var emk = this.parentNode.children[2];
    console.log(id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success: function(data){
            console.log(data)
            console.log("Succesfully")
            emk.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }
    })
})