$(function(){
        let parameters = {};
        let url = '';
        let method = '';
        let answers = {
            user: '',
            cycle: '',
            questions: [],
        };

        $('#btnGuardar').on('click', function () {
            //e.preventDefault();
            url = $('#form_auto_evaluation').attr('action');
            method = $('#form_auto_evaluation').attr('method');
            console.log(url + '\n' + method);
            //confirmarEnvio();
        });

        function getData() {
            answers.user = $('input:hidden[name=user_id]').val();
            answers.cycle = $('input:hidden[name=cycle_id]').val();
            $('#preguntas tbody tr.parent td > input[type="radio"]:checked').each(function (index, input) {
                let item = {};
                item.question = $(input).parent().parent().find('input:hidden[name=pregunta]').val();
                item.parameter = $(input).val();
                answers.questions.push(item);
            });
        }

        function confirmarEnvio() {
            Swal.fire({
              title: 'Notificación',
              text: '¿Desea enviar su evaluación ahora?',
              icon: 'question',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Si, proseguir!'
            }).then(function(result){
              if (result.isConfirmed) {
                  getData();
                  parameters = new FormData();
                  parameters.append('action', $('input[name="action"]').val());
                  parameters.append('answers', JSON.stringify(answers));
                  console.log(answers +parameters +'\n' + url);
                  //alert('Confirmed');
                  //saveEvaluation(url, redirection)
                  sendRequest(url, parameters, method, redirection);
              }
            });
        }

        function sendRequest(url, parameters, redirection) {
            $.ajax({
                url: url,
                data: parameters,
                type: 'POST',
                dataType: 'json',
                processData: false,
                contentType: false,
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    window.setTimeout(function () {
                        window.location.href = redirection;
                    }, 1500);
                    return true;
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ' ' + errorThrown);
            }).always(function (data) {

            });
        }

        function confirmAction(title, content, icon, url, redirection) {
            Swal.fire({
              title: title,
              text: content,
              icon: icon,
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Si, proseguir!'
            }).then(function(result){
              if (result.isConfirmed) {
                  //alert('Confirmed'+ url + redirection);
                  //saveEvaluation(url, redirection)
                  sendRequest(url, parameters, method, redirection);
              }
            });
        }

        function saveEvaluation(url, redirection) {
            /*
            getData();
            answers.user = $('input:hidden[name=user_id]').val();
            answers.ciclo = $('input:hidden[name=cycle_id]').val();
            parameters = new FormData();
            parameters.append('action', $('input[name="actions"]').val());
            parameters.append('answers', JSON.stringify(answers));
            console.log(parameters +'\n' + url);
            sendRequest(url, parameters, redirection);*/
        }

});