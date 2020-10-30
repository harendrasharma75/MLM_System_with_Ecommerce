var set=setInterval(function(){
    
  var currentT = new Date();
  var days = currentT.getDate();
  var hours = currentT.getHours();
  var mins = currentT.getMinutes();
  var secs = currentT.getSeconds();

  if(hours == 07 && mins==0 && secs>2){hours = hours+1;}
  if(hours<= 07){hours = 07;mins=0;secs=0;}
  if(hours >= 07){days = days+1; hours =07;mins=0;secs=0;}
  
  currentT.setDate(days);
  currentT.setHours(hours);
  currentT.setMinutes(mins);
  currentT.setSeconds(secs);

  document.getElementById('referece').innerHTML=currentT.toLocaleTimeString();

  var now = new Date().getTime();
  var diff = currentT - now;

  var d = Math.floor((diff / (1000 * 60 * 60 * 24)));
  var h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  var s = Math.floor((diff % (1000 * 60)) / 1000);

    var formattedTime = h + ' : ' + m + ' : ' + s + " Hours";
    document.getElementById("validity").innerHTML = formattedTime;

    if(diff<=0){
      window.location = "/myAdmin/updating...";
    }


  },1000);