$(".progress").hide();
  document.onkeydown = pageEvent;
  function pageEvent(evt){
    evt = evt ||window.event; 
    var key=evt.which||evt.keyCode;
    if (key == 37) location = prevpage;
    if (key == 39) location = nextpage;
    if (key == 13) location = novelpage;
  }; 