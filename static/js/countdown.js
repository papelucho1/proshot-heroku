
console.log("timesss !");

const countdownEl = document.getElementById('countdown');

console.log(document.getElementById('countdown'));
var x = document.getElementById('tiempo').value;
console.log(typeof parseInt(x))

console.log("timesss 2!");

const startingMinutes = parseInt(x);
let time = startingMinutes*60;


setInterval(UpdateCountdown, 1000);

function UpdateCountdown(){
    const minutes = Math.floor(time/60);
    let seconds = time % 60;


    seconds = seconds < 10 ? '0' + seconds : seconds;

    countdownEl.innerHTML = `${minutes} : ${seconds}`;
    time--;
    time = time < 0 ? 0 : time; 
    if(time<=0){

        document.getElementById('submit').click();
            
    }
    if (time<=30){
        document.getElementById('countdown').className ='animacion';
    }
}
