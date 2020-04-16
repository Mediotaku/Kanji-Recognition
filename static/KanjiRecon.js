window.onload = function(){
    var canvas = document.getElementById("kanjicanvas");
    //To transform canvas pixel size from default to intended size (same as CSS one)
    canvas.width=300;
    canvas.height=300;
    var ctx = canvas.getContext("2d");
    iniciar(canvas, ctx);
}

//To transform the canvas content into binary data
function canvastoimg(){
   var canvas = document.getElementById("kanjicanvas");
   document.getElementById('imgcanvas').value = canvas.toDataURL();
}

function iniciar(canvas, ctx){
    var click=false;
    console.log(window.initialData);
    
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
//Language management module
    function language(){
       var lang =sessionStorage.getItem("language");
       if(lang!='ja' && lang!='en'){
         sessionStorage.setItem("language", document.getElementsByTagName("html")[0].getAttribute("lang"));
         lang =sessionStorage.getItem("language");
       } 
       document.getElementsByTagName("html")[0].setAttribute("lang", lang);
       var aux = document.getElementById("sentence2").innerHTML;
       var mychar = aux.substring(aux.lastIndexOf("「") + 1, aux.lastIndexOf("」"));
       if(lang=='ja'){
         document.getElementById("changelang").checked=true;
         var pelements=document.querySelectorAll("p");
         for (var i = 0; i < pelements.length; i++) {
            pelements[i].style['font-family']="'Noto Serif JP', serif";
            pelements[i].style['font-size']="1em";
         }
         document.querySelectorAll("form")[0].style['font-family']="'Noto Serif JP', serif";
         document.querySelectorAll("form")[0].style['font-size']="1em";
         document.getElementById("sentence1").innerHTML="ようこそ！これは日本語の文字を認識の研究プロジェクトです。自分の1文字を送ることで貢献できます。";
         document.getElementById("sentence2").innerHTML="グレー の箱に「"+mychar+"」の文字を記入してください。その後、以下の3つの質問に答えて[送信]をクリックしてください。";
         document.getElementById("question1").innerHTML="出身はどちらですか?";
         document.getElementById("question2").innerHTML="あなたの日本語レベルはどのくらいですか？";
         document.getElementById("question3").innerHTML="文字を書くのに何を使いましたか？";
         document.getElementById("country1").innerHTML="日本";
         document.getElementById("country2").innerHTML="他の国";
         document.getElementById("language1").innerHTML="母語";
         document.getElementById("language2").innerHTML="第二言語";
         document.getElementById("language3").innerHTML="勉強中";
         document.getElementById("input1").innerHTML="マウス";
         document.getElementById("input2").innerHTML="指";
         document.getElementById("input3").innerHTML="タッチペン";
         var languageele=document.getElementsByName("language");
         var inputele=document.getElementsByName("input");
         for (var i = 0; i < languageele.length; i++){
            languageele[i].style['margin-left']="25px";
            inputele[i].style['margin-left']="27px";
         } 
         document.getElementById("clean").innerHTML="消す";
         document.getElementById("clean").style['font-family']="'Noto Serif JP', serif";
         document.getElementById("submit").value="送信";
         document.getElementById("submit").style['margin-left']='41%';
         document.getElementById("submit").style['font-family']="'Noto Serif JP', serif";
       }
       if(lang=='en'){
         document.getElementById("changelang").checked=false;
         var pelements=document.querySelectorAll("p");
         for (var i = 0; i < pelements.length; i++) {
            pelements[i].style['font-family']="'Nunito', sans-serif";
            pelements[i].style['font-size']="1em";
         }
         document.querySelectorAll("form")[0].style['font-family']="'Nunito', sans-serif";
         document.querySelectorAll("form")[0].style['font-size']="1em";
         document.getElementById("sentence1").innerHTML="Welcome! This is a research project for the recognition of Japanese characters. You can contribute by sending one character of your own.";     
         document.getElementById("sentence2").innerHTML="Please write the character「"+mychar+"」in the grey box. After that, answer the three questions below and press 'Submit'.";
         document.getElementById("question1").innerHTML="Where are you from?";
         document.getElementById("question2").innerHTML="What is your level of Japanese language?";
         document.getElementById("question3").innerHTML="What have you used to write the character?";
         document.getElementById("country1").innerHTML="Japan";
         document.getElementById("country2").innerHTML="Other";
         document.getElementById("language1").innerHTML="Native";
         document.getElementById("language2").innerHTML="Second language";
         document.getElementById("language3").innerHTML="Learner";
         document.getElementById("input1").innerHTML="Mouse";
         document.getElementById("input2").innerHTML="Finger";
         document.getElementById("input3").innerHTML="Stylus pen";
         var languageele=document.getElementsByName("language");
         var inputele=document.getElementsByName("input");
         for (var i = 0; i < languageele.length; i++){
            languageele[i].style['margin-left']="4px";
            inputele[i].style['margin-left']="20px";
         }
         document.getElementById("clean").innerHTML="Clean";
         document.getElementById("clean").style['font-family']="'Nunito', sans-serif"; 
         document.getElementById("submit").value="Submit";
         document.getElementById("submit").style['margin-left']='39%';
         document.getElementById("submit").style['font-family']="'Nunito', sans-serif"; 
      }
    }
    document.getElementById("changelang").onchange=function(){
      var lang=document.getElementsByTagName("html")[0].getAttribute("lang");
      if(lang=='ja'){
         document.getElementsByTagName("html")[0].setAttribute("lang","en");
         sessionStorage.setItem("language", "en");
         language();
      }
      if(lang=='en'){
         document.getElementsByTagName("html")[0].setAttribute("lang","ja");
         sessionStorage.setItem("language", "ja");
         language();
      }
    }
    language();
}
