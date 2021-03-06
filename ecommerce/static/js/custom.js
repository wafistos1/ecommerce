$(document).on('click', '.icon_icon span', function (event) {

    event.preventDefault();
    Element = $(this)

    $.ajax({
        url: $(this).parent().attr('href'),
        type: 'POST',
        data: {

            val: $(this).parent().attr('name'),
            pk: $(this).parent().attr('href'),

        },
        dataType: 'json',
        success: function (response) {
            if (response['etat'] == 1) {
                
                Element.toggleClass('icon_heart icon_heart_alt');
            }
            else {
                
                Element.toggleClass('icon_heart_alt icon_heart');
                
            }
        },
        error: function (rs, e) {
            console.log(rs);
        }
    });

});


$(document).on('click', '.cart-btn', function (event) {

    event.preventDefault();


    let id = $(this).attr('name');
    let url = $(this).attr('href');
    

    $.ajax({
        url: $(this).attr('href'),
        type: 'POST',
        data: {

            pk: id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (response) {
            
            var html = ' <p>Added item <strong>' + response.item_title + '</strong> to cart.</p>'
            $('.modal-body').html(html);
            $('.myModal').modal('show');
            // $( "div.tip" ).replaceWith( "<div class='tip'>" + response.count + "</div>" );
            
                
        },
        error: function (rs, e) {
            console.log(rs);
        }
    });




});

// $('#header__right__widget').mouseenter(function (event){
   

//     $.ajax({
//         url: '/cart_list/',
//         type: 'POST',
//         data: {
//             csrfmiddlewaretoken: window.CSRF_TOKEN,
//         },
//         dataType: 'json',
//         success: function (response) {
            
//             $( "div.tip" ).replaceWith( "<div class='tip'>" + response.count + "</div>" );
//         },
//         error: function (rs, e) {
//             // alert('error')
//         }
//     });

// });


$('.pro-qty span').click(function (event){
   
    var indent = $(this).parent().find(':nth-child(2)').attr('value');
    var id_product =$(this).parent().find(':nth-child(2)').attr('name');
    var action = 'toto';
    $( ".icon_loading" ).css( "display", "block" );
     
         action = $(this).attr('class')
    // alert(indent);
    // alert(id_product);
    // alert(action);
    $.ajax({
        url: '/update_item/',
        type: 'POST',
        data: {
            'indent': indent,
            'id': id_product,
            'action': action,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (response) {
            console.log(response.total, response.total_cart)
            $( ".icon_loading" ).css( "display", "none" );
            var html = '<input class="myclass" id="toto'+response.id + 'type="text" name='+ response.id +' value="'+ response.quantity + '">'
            var total = '<td class="cart__total" id="total'+response.id + '">$' + (response.total).toFixed(1) + '</td>';
            var total_cart = '<li class="total_cart">Subtotal <span>$ '+ (response.total_cart).toFixed(1) +'</span></li>';
            var total_final = '<li class="total_cart_final">Total <span>$'+ (response.total_cart).toFixed(1)+'</span></li>'
            $(':input[id="toto'+response.id +'"]').replaceWith(html); 
            $('#total'+response.id +'').replaceWith(total);
            $('.total_cart').replaceWith(total_cart);
            $('.total_cart_final').replaceWith(total_final);
            
        },
        error: function (rs, e) {
            alert('error');
        }
    });

});
