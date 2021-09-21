
function message_error(obj){
    var html = '</ul>'
    $.each(obj, function(key, value){
        console.log(value)
        console.log(typeof(value))

        html += '<li>' + key + ': ' + value + '</li>' ;   
        /**/
    });

    html += '</ul>'
    Swal.fire({
        title: 'Error!',
        html : html,
        icon: 'error',
      })
};




function message_error_question(obj){
    
    $('#preguntasAlert')      
        .append(`<div class="alert alert-warning" role="alert" id = "errorRadiosIngresados">
        <span class="alert-inner--text">Debes ingresar almenos un encabezado en texto o imagen.</span>
        </div>`);

};



function validarForm(document){
    const preguntasAlert = document.getElementById('preguntasAlert');
    var error = true
    if (!document.getElementById('id_question_text').value && !document.getElementById('inputImagen').files[0] && !document.getElementById('id_question_url').value){
        console.log("nada in  questionsstatus error1:"+ error)
        if (error){
            preguntasAlert.innerHTML = `<div class="alert alert-warning" role="alert">
                    <span class="alert-inner--text">Debes ingresar al menos un texto o una imagen de encabezado.</span>
                    </div>` ;
            error = false;
            console.log("nada in status error1:"+ error)
            return false
        /*}else{
            error1 = true;
            console.log("error ya ignresado error1:"+ error1)*/
        }
    }else{
        preguntasAlert.innerHTML = ``;    
        error1 = true;
        console.log("hay algo ingresado "+ error);
    }
   
    const alternativasAlert = document.getElementById('alternativasAlert');
     var radiosIngresados = document.getElementsByName("alternativa").length;
      console.log("radios " + radiosIngresados);
      if (radiosIngresados<4){
          if (error){
              alternativasAlert.innerHTML = `<div class="alert alert-warning" role="alert" id = "errorRadiosIngresados">
              <span class="alert-inner--text">Debes ingresar al menos 4 respuestas , te faltan ingresar ${ (4 - radiosIngresados)}.</span>
              </div>` ;
              error = false;
              console.log("nada in radios status error1:"+ error)
              return false
          /*}else{
              error1 = true;
              console.log("error ya ignresado error1:"+ error1)*/
          }
      }else{

          alternativasAlert.innerHTML = ``;  
          error = true;
      }
      /* mostrar que se debe ingrear almenos alguna pregunta*/

      if(!document.querySelector('input[type=radio]:checked')) {     
            if (error){
                alternativasAlert.innerHTML = `<div class="alert alert-warning" role="alert">
                <span class="alert-inner--text">Debes seleccionar una respuesta correcta.</span>
                </div>` ;
                error = false;
                console.log("nada in radios status error1:"+ error)
                return false
            /*}else{
                error1 = true;
                console.log("error ya ignresado error1:"+ error1)*/
            }
        }else{

            alternativasAlert.innerHTML = ``;  
            error = true;
        }
         
         
}