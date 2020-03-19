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
    function grid(){
        //Drawing 原稿用紙 grid lines in lightgrey
        ctx.strokeStyle="lightgrey";
        ctx.lineWidth = 1;
        ctx.lineCap= "butt";
        ctx.beginPath();
        ctx.setLineDash([10,10]);
        //+5 to make lines symmetrical
        ctx.moveTo(0+5,canvas.width/2);
        ctx.lineTo(canvas.height,canvas.width/2);
        ctx.stroke();
        ctx.beginPath();
        ctx.setLineDash([10,10]);
        ctx.moveTo(canvas.width/2,0+5);
        ctx.lineTo(canvas.width/2,canvas.height);
        ctx.stroke();
        //Return to standard writing settings
        ctx.setLineDash([]);
        ctx.strokeStyle="black";
    }

    grid();
    
    canvas.onmousedown=function(e){
       click=true;
       ctx.beginPath();
    }
    canvas.addEventListener("touchstart", function (e){
       click=true;
       ctx.beginPath();
       e.preventDefault();
    }); 
    window.onmouseup=function(e){
       click=false;
       ctx.beginPath();
    }
    window.addEventListener("touchend", function (e){
       click=false;
       ctx.beginPath();
       e.preventDefault();
    }); 
    canvas.onmousemove=function(e){
       if(click){
           //getBoundingClientRect() returns the position of an element relative to the viewport
           //this function don't take into account an style applied to the canvas like border or padding 
           //Get the clientX/Y and subtract the canvas top left to get the correct position
           var rect = canvas.getBoundingClientRect();
           var clickX = e.clientX - rect.left;
           var clickY = e.clientY - rect.top;
           ctx.lineWidth = 3;
           ctx.lineCap= "round";
           ctx.lineTo(clickX, clickY);
           ctx.stroke();
       }
    }
    canvas.addEventListener("touchmove", function (e){
       if(click){
           var touch = e.touches[0];
           //pageX/Y returns the position relative to the top left corner of the whole page, scroll included
           //clientX/Y returns the position relative to the top left corner of the visible page in that moment
           //When using either clientX/Y or pageX/Y, we have to subtract the offset of the canvas to get
           //the correct position relative to its top left corner.  
           var touchX = touch.pageX - touch.target.offsetLeft;
           var touchY = touch.pageY - touch.target.offsetTop;
           ctx.lineWidth = 3;
           ctx.lineCap= "round";
           ctx.lineTo(touchX, touchY);
           ctx.stroke();
       }
       e.preventDefault();
    }); 
    document.getElementById("clean").onclick=function(){
       //The enternal battle against width hack 
       ctx.clearRect(0, 0, canvas.width, canvas.height);
       //Draw grid lines after clear
       grid();
    }
}
