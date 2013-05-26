function buena() {
  var currentTime = new Date()
  var mes = currentTime.getMonth() + 1;
  var dia = currentTime.getDate();
  var año = currentTime.getFullYear();
  
  var horas    = currentTime.getHours()
  var minutos  = currentTime.getMinutes()
  var segundos = currentTime.getSeconds()

  $("#id_ingreso").val(dia+"/"+mes+"/"+año+" "+horas+":"+minutos+":"+segundos)
  $("#id_fecha").val(dia+"/"+mes+"/"+año+" "+horas+":"+minutos+":"+segundos)
}

$(document).ready( function() {
		$("#id_atencion").change(function () {
      var valor = $("#id_atencion").val()
      if (valor == 2) {
        document.calcularTriage.submit()
      }
    })

		$("#id_esperar").change(function () {
      var valor = $("#id_esperar").val()
      if (valor == 3) {
        document.calcularTriage.submit()
      }
    })

		$("#id_recursos").change(function () {
      var valor = $("#id_recursos").val()
      if (valor == 1) {
        document.calcularTriage.submit()
      } else if (valor == 2) {
        document.calcularTriage.submit()
      }
    })


});
