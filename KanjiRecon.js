window.onload = function(){
    var canvas = document.getElementById("kanjicanvas");
    //To transform canvas pixel size from default to intended size (same as CSS one)
    canvas.width=300;
    canvas.height=300;
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
        ctx.beginPath();
     }
     canvas.onmousemove=function(e){
         if(click){
             console.log(e.offsetX, e.offsetY);
             ctx.lineWidth=3;
             ctx.lineCap= "round";
             ctx.lineTo(e.offsetX, e.offsetY);
             ctx.stroke();
         }
     }
}
