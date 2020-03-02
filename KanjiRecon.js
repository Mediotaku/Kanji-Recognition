window.onload = function(){
    var canvas = document.getElementById("kanjicanvas");
    var ctx = canvas.getContext("2d");
        iniciar(canvas, ctx);
}

function iniciar(canvas, ctx){
    var click=false;
     canvas.onmousedown=function(e){
        click=true;
     }
     canvas.onmouseup=function(e){
        click=false;
     }
     canvas.onmousemove=function(e){
         if(click){
             console.log("si");
             
         }
     }
}
