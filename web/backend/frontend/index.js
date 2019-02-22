$(document).scrollTop(0);
setTimeout(function() {$( '#logo' ).removeClass( 'bounceInLeft' ); $( '#logo' ).addClass( 'rubberBand' );}, 1000);

setTimeout(function() {$('#rul').css('display','block'); $('#rul').addClass('bounceInLeft');}, 2000);
setTimeout(function() {$('#rul2').css('display','block'); $('#rul2').addClass('bounceInDown');}, 2500);

setTimeout(function() {$( '#rul' ).removeClass( 'bounceInLeft' ); $( '#rul' ).addClass( 'bounceOutLeft' );}, 3500);
setTimeout(function() {$( '#rul2' ).removeClass( 'bounceInDown' ); $( '#rul2' ).addClass( 'bounceOutUp' );}, 3500);

setTimeout(function() {$('#rul').css('display','none');}, 4500);
setTimeout(function() {$('#rul2').css('display','none');}, 4500);
// setTimeout(function() {$('#sliper').css('opacity','1');}, 4500);

setTimeout(function() {let logo = document.getElementById('logo').style
    logo.top='1%';
    logo.width='7%';
    logo.left='47%'}, 4500);
// setTimeout(function(){document.getElementById('p1').style.backgroundColor='black';},4500);
setTimeout(function(){document.getElementsByClassName('text_1')[0].style.opacity='1';},4500);
var view=false;
function v(){
    if(view==false){
        view=true;
        document.getElementsByClassName('jello')[0].style.color='grey';
    }else{
        view=false;
        document.getElementsByClassName('jello')[0].style.color='black';
    }
}
setTimeout(function(){
    if(view==false){
        window.location.reload()
    }
}, 10000)
