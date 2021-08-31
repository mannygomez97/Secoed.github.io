let $ = jQuery.noConflict();

/******************* Create Modals ******************/
function openModal(url, opModal) {
    $('#'+ opModal).load(url, function () {
        $(this).modal('show');
    });
}

function closeModal(opModal) {
    $('#' + opModal).modal('hide');
    let url = $('input[name="url_list"]').val();
    window.setTimeout(function() {
            window.location.href = url;
    },1500);
    return true;
}

function activeButton(button) {
    if ($('#' + button).prop('disabled')) {
        $('#' + button).prop('disabled',false);
    }else{
        $('#' + button).prop('disabled',true);
    }
}

function ajaxRequest(form, error_tag, button) {
    activeButton(button);
    let param = $('#' + form).serialize()
    let method = $('#' + form).attr('method')
    let action  = $('#' + form).attr('action')
    console.log(param + '\n'+ method + '\n' + action);
    $.ajax({
        data:$('#' + form).serialize(),
        url: $('#' + form).attr('action'),
        type:$('#' + form).attr('method'),
        dataType: 'JSON',
        success:function(response){
            notification('Excelente!', response.message, 'success');
            closeModal();
        },
        error:function(error){
            notification('Oops...!', error.responseJSON.message, 'error');
            errorAlerts(error_tag, error);
            activeButton(button);
        }
    });
}

function errorAlerts(error_tag, errors) {
    $('#'+ error_tag).html('');
    let error= '';
    for (let item in errors.responseJSON.error) {
        error += '' +
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
            +   '<strong>'+ errors.responseJSON.error[item] + '</strong>' +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'+
            '</div>';
    }
    $('#'+ error_tag).append(error)
}

function notification(title, message, icon) {
    Swal.fire({
        title: title,
        text: message,
        icon: icon,
        showConfirmButton: false,
        timer:3000
    });
}

function confirmDelete(url) {
    let token = {csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()};
    Swal.fire({
      title: '¿Estas seguro?',
      text: "¡No podrás revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si, eliminar!',
    }).then(function(result){
      if (result.isConfirmed) {
         $.ajax({
            data: token,
            url: url,
            type:'post',
            success:function(response){
                notification('Excelente!', response.message, 'success');
                closeModal();
            },
            error:function(error){
                notification('Oops!', error.responseJSON.message, 'error');
            }
        });
      }
    });
}