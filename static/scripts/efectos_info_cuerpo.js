$(document).ready(function () {
  /* botones de los div que eliminan los div*/
  /*se elimna caja1*/
  $('#boton1').click(function(){
    $('#cajon1, #cajon2, #cajon3').slideUp();
  });
  /*se elimina caja2*/
  $('#boton2').click(function(){
    $('#cajon2, #cajon3').slideUp();
    $("#cuerpou").scrollLeft(365); 
  });
  /*se elimina caja3*/
  $('#boton3').click(function(){
    $('#cajon3').slideUp();
    $("#cuerpou").scrollLeft(525); 
  });

  /*Asociaciones de los botones*/
  $('area').click(function(){
    $('#cajon1').slideDown();
    $("#cuerpou").scrollLeft(365); 
    var parte = $(this).attr("id");
    $('.pc').each(function(i,valor) {
      if ($(valor).attr("zona") == parte){
        $(valor).show();                
      }else{
        $(valor).hide();
      }
    });
  });

  $('.pc').click(function(){
    $('#cajon2').slideDown(); 
    $("#cuerpou").scrollLeft(525);
    var proble = $(this).attr("id");
    $('.causa').each(function(i,valor) {
      if ($(valor).attr("problem") == proble){
        $(valor).show();                
      }else{
        $(valor).hide();
      }
    });
  });

  $('.causa').click(function(){
    $('#cajon3').slideDown();
    $("#cuerpou").scrollLeft(685); 
    var causa = $(this).attr("id");
    $('.pres').each(function(i,valor) {
      if ($(valor).attr("causa") == causa){
        $(valor).show();                
      }else{
        $(valor).hide();
      }
    });
  });
});
