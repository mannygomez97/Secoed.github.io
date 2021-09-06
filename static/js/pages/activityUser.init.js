function solicitar(){
    const csrftoken = getCookie('csrftoken');
    var url=window.location.href.replace('authentication/perfil','jsnCountLogin');
    $.ajax({
        url: url,
        dataType:"json",
        type:'POST',
        headers:{"X-CSRFToken": csrftoken },
        success:function (data){
            alert("todo bien "+data['la']);
        },error:function(xhr, status, error) {
            var err = + xhr.responseText ;
            alert("error"+err);
        }
    })
    return data=[10, 30, 20, 40, 50,70,80]
}
var options = {
    series: [{
        name: "Login",
        data: solicitar()
    }],
    chart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight'
    },
    title: {
        text: 'Inicio de sesión por mes',
        align: 'left'
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'],
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'],
    }
};
var chart = new ApexCharts(document.querySelector("#activity-user"), options);
chart.render();


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}