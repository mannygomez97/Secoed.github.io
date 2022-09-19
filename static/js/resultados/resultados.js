
function individual(x){

    var total = $("#tr"+x+' td:nth-child(13)').text();
    //alert(total);

    var auto =
       [
           ["Pedagógia",parseFloat($("#tr"+x+' td:nth-child(7)').text())],
           ["Tics",parseFloat($("#tr"+x+' td:nth-child(5)').text())],
           ["Didáctica",parseFloat($("#tr"+x+' td:nth-child(6)').text())]
       ]
   var coe =
       [
           ["Pedagógia" ,parseFloat($("#tr"+x+' td:nth-child(11)').text())],
           ["Tics",parseFloat($("#tr"+x+' td:nth-child(9)').text())],
           ["Didáctica",parseFloat($("#tr"+x+' td:nth-child(10)').text())]
       ];
   mostrarsemaforo(total,"global");
   var totalauto = parseFloat($("#tr"+x+' td:nth-child(8)').text());

   var totalcoe=parseFloat($("#tr"+x+' td:nth-child(12)').text());

   $("#nombreestadistica").html("de : "+$("#tr"+x+' td:nth-child(3)').text());

   $("#ModalGrafico").modal("show");

   graph_auto_evaluation(totalauto,auto);
   graph_co_evaluation(totalcoe,coe);
}

function mostrarsemaforo(total,divid){
    var n1 = $("#IND").text();
   var n2 = $("#RC").text();
   var n3 = $("#RCA").text();
   var n4 = $("#RCAI").text();
   var id = `#semaforo${divid}`;
   //alert(total);
   if(parseFloat(total)<=parseFloat(n1))
       {
          $(id).html("<img src='../../static/images/eva/rojo.png' style='width: 50%;'>");
       }
       else if(parseFloat(total)<=parseFloat(n2))
       {
          $(id).html("<img src='../../static/images/eva/amarillo.png' style='width: 50%;'>");
       }
       else if(parseFloat(total)<=parseFloat(n3))
       {
          $(id).html("<img src='../../static/images/eva/verde.png' style='width: 50%;'>");
       }
       else if(parseFloat(total)<=parseFloat(n4))
       {
          $(id).html("<img src='../../static/images/eva/azul.png' style='width: 50%;'>");
       }
       else
       {
          $(id).html("<img src='../../static/images/eva/azul.png' style='width: 50%;'>");
       }
}

function graph_auto_evaluation(subtitle, series) {
     Highcharts.chart('auto', {
         chart: {
             type: 'pie',
             options3d: {
                 enabled: true,
                 alpha: 45
             }
         },
         title: {
             text: 'La nota global de autoevaluación es de:'
         },
         subtitle: {
             text: subtitle + '/100'
         },
         plotOptions: {
             pie: {
                 innerSize: 100,
                 depth: 45
             }
         },
         series: [{
             name: 'Rendimiento por área',
             data: series
         }]
     });
 }

 function graph_co_evaluation(subtitle, series) {
     Highcharts.chart('coe', {
         chart: {
             type: 'pie',
             options3d: {
                 enabled: true,
                 alpha: 45
             }
         },
         title: {
             text: 'La nota global de co evaluación es de:'
         },
         subtitle: {
             text: subtitle + '/100'
         },
         plotOptions: {
             pie: {
                 innerSize: 100,
                 depth: 45
             }
         },
         series: [{
             name: 'Rendimiento por área',
             data: series
         }]
     });
 }

