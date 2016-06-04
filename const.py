pager='''<ul class="pager">
        <li class="previous"><a href="#previous">&larr; 上一章</a></li>
        <li class="next"><a href="#next">下一章 &rarr;</a></li>
      </ul>
    </div>
'''

script_continuously='''<script type="text/javascript">
    $(function(){
      $(window).bind('scroll',function(){show()});
      $(".footer").hide();
      var chapter = #chapter;
      function show()
      {

          if($(window).scrollTop()+$(window).height()>=$(document).height())
          {
              ajaxReadText();
          }
      }
      
      function ajaxReadText()
      {

          var html="";
          $.ajax({
                type:'get',
                dataType:'jsonp',
                url:'/json/#novelname/' + chapter,
                beforeSend:function(){$(".footer").show()},
                complete:function(data){
                  obj = JSON.parse(data.responseText)
                  html+='<div class="well well-lg center-block">';
                  html+='<h1 align="center">'+obj.title+'</h1>';
                  html+='<p id="text">'+obj.description+'</p>';
                  html+='</div>';
                  $("#resText").append($(html));
                  chapter= chapter + 1
                  $(".footer").hide()}
                //error:function(){$(".progress").hide();}
          });//.ajax
      }
    })
  </script>'''

script_pager='''<SCRIPT type="text/javascript">
  $(".progress").hide();
  document.onkeydown = pageEvent;
  var prevpage="#previous";
  var nextpage="#next";
  var novelpage="#novelpage";
  function pageEvent(evt){
    evt = evt ||window.event; 
    var key=evt.which||evt.keyCode;
    if (key == 37) location = prevpage;
    if (key == 39) location = nextpage;
    if (key == 13) location = novelpage;
  }; 
  </SCRIPT>'''