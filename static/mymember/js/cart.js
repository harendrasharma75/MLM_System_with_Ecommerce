
var userId = document.getElementById('userId').innerHTML
if(localStorage.getItem('cart')==null){
    var cart ={};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart)
    
}


$('.addpr').on('click', 'button.cart', function(){
    var idstr = this.id.toString();
    console.log(idstr)
    if(cart[idstr] != undefined){
        qty = cart[idstr][0] + 1;
        names = document.getElementById('name'+idstr).innerHTML;
        cart[idstr]=[qty,names];
    } else {
        qty=1;
        names = document.getElementById('name'+idstr).innerHTML;
        price = document.getElementById('price'+idstr).innerHTML;
        cart[idstr]=[qty, names, parseFloat(price)];
        
    }
    updateCart(cart)
    
});

$('#popcart').popover()
updatePopover(cart);

function updatePopover(cart){
    var popStr = "";
    popStr = popStr + "<h5>Cart for your item inside shopping</h5><div class='mx-2 my-2'>"
    var i = 1;
    for(var item in cart){
        popStr = popStr + "<b>"+ i + "</b>. ";
        popStr = popStr + document.getElementById('name'+item).innerHTML.slice(0,20) + " Qty : " + cart[item][0] + '<br>';
        i = i+1;
    }
    popStr = popStr + "</div><a href='/checkout'><button class='btn btn-primary' id='checkout'>Checkout</button></a><button class='btn btn-primary'onclick='clearCart()' id='clearCart'>ClearCart</button>"
    document.getElementById('popcart').setAttribute('data-content',popStr);
    $('#popcart').popover();
}

function clearCart(){
    cart = JSON.parse(localStorage.getItem('cart'));
    for(var item in cart){
        document.getElementById('add'+item).innerHTML='<button id="'+ item +'" class="btn btn-primary cart" style="width: auto;">Buy</button></span>'
    }
    localStorage.clear();
    cart={};
    updateCart(cart);
}

function updateCart(cart){
    var sum = 0;
    for(var item in cart){
        sum = sum + cart[item][0];
        if(cart[item][0]!=0){
            document.getElementById('add'+item).innerHTML = "<button id='minus"+ item +"' class='btn btn-primary minus' style='width:auto;'>-</button><span id='val"+item+"'>"+cart[item][0]+"</span><button id='plus"+item+"' class='btn btn-primary plus' style='width:auto;'>+</button>";

        }
    }
    localStorage.setItem('cart',JSON.stringify(cart));
    
    document.getElementById('cart').innerHTML=sum;
    updatePopover(cart);
    
}

$('.addpr').on("click", "button.minus", function(){
    a = this.id.slice(7, );
    cart['pr'+a][0]=cart['pr'+a][0]-1;
    cart['pr'+a][0] = Math.max(0,cart['pr'+a][0]);
    
    document.getElementById('valpr'+a).innerHTML=cart['pr'+a][0]
    
    if(cart['pr'+a][0]==0){ 
        document.getElementById('add'+'pr'+a).innerHTML='<button id="pr'+a+'" class="btn btn-primary cart" style="width: auto;">Buy</button></span>'    
        delete cart['pr'+a]
    }
    updateCart(cart)
});

$('.addpr').on("click", "button.plus", function(){
    a = this.id.slice(6, );
    cart['pr'+a][0]=cart['pr'+a][0]+1;
    document.getElementById('valpr'+a).innerHTML=cart['pr'+a][0]
    updateCart(cart)
});
