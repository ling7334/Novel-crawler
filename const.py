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
                url:'http://api.flickr.com/services/feeds/photos_public.gne?tags=car&tagmode=any&format=json&jsoncallback=?',
                beforeSend:function(){$(".footer").show()},
                success:function(data)
                {
                              $.each(data.items,function(i,item)
                              {
                                    
                                    html+='<div class="well well-lg center-block">';
                                    html+='<h1 align="center">'+item.title+'</h1>';
                                    html+='<p>'+item.description+"</p>";
                                    html+='<div>'+item.tags+'</div>';
                                    html+='</div>';

                              });//.each
                              $("#resText").append($(html));
                },
                complete:function(){$(".footer").hide()}
                //error:
          });//.ajax
      }
    })
  </script>'''

script_pager='''<SCRIPT type="text/javascript">
  $(".progress").hide();
  document.onkeydown = pageEvent;
  var prevpage="#previous";
  var nextpage="#next";
  function pageEvent(evt){
    evt = evt ||window.event; 
    var key=evt.which||evt.keyCode;
    if (key == 37) location = prevpage;
    if (key == 39) location = nextpage;
  }; 
  </SCRIPT>'''