// Modal View 
var $ = jQuery.noConflict();

function openModal(url, idModal) {
    console.log(idModal)
    $(idModal).load(url, function () {
        $(this).modal('show')
    });
}

//Delete
function deleteMenu(id) {
    Swal.fire({
        "title": "¿Está seguro?",
        "text": "Esta acción no se puede revertir",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "NO",
        "confirmButtonText": "SÍ",
        "cancelButtonColor": "#f46a6a",
        "confirmButtonColor": "#34c38f",
    })
        .then(function (result) {
            if (result.isConfirmed) {
                console.log(id)
                window.location.href = "deleteMenu/" + id
            }
        })
}


