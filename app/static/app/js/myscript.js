$('#slider1, #slider2, #slider3').owlCarousel({
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
    var id =$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    //console.log(id)
    $.ajax({
        type : "GET",
         url : "/pluscart",
         data :{
             proud_id : id
         },
         success: function (data){
             eml.innerText = data.quantity
             document.getElementById("amount").innerText = data.amount
             document.getElementById("totalamount").innerText = data.totalamount
         }
    })
})

$('.minus-cart').click(function(){
    var id =$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    //console.log(id)
    $.ajax({
        type : "GET",
         url : "/minuscart",
         data :{
             proud_id : id
         },
         success: function (data){
             eml.innerText = data.quantity
             document.getElementById("amount").innerText = data.amount
             document.getElementById("totalamount").innerText = data.totalamount
         }
    })
})

$('.remove-cart').click(function(){
    var id =$(this).attr("pid").toString();
    var eml = this
    console.log(id)
    $.ajax({
        type : "GET",
         url : "/removecart",
         data :{
             proud_id : id
         },
         success: function (data){
             console.log("Delete")
             document.getElementById("amount").innerText = data.amount
             document.getElementById("totalamount").innerText = data.totalamount
             eml.parentNode.parentNode.parentNode.parentNode.remove()
         }
    })
})

$('.cancel-order').click(function(){
    var id =$(this).attr("pid").toString();
    var eml = this
    console.log(id)
    $.ajax({
        type : "GET",
         url : "/cancelorder",
         data :{
             op_id : id
         },
         success: function (data){
             console.log("Delete")
            eml.parentNode.parentNode.parentNode.remove()
         }
    })
})