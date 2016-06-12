$(function(){
      $(window).bind('scroll',function(){show()});
      $(".footer").hide();
      $(".pager").remove();
      var query_status = 1;
      function show()
      {

          if($(window).scrollTop()+$(window).height()>=$(document).height())
          {
              ajaxReadText();
          }
      }
      
      function ajaxReadText()
      {
          if (query_status == 0){return false}
          var html="";

          $.ajax({
            type:'post',
            dataType:'json',
            url:'/'+ novelname + '/' + nextchapter,
            beforeSend:function(){$(".footer").show();query_status =0},
            complete:function(data){
                obj = JSON.parse(data.responseText)
                html+='<div class="well well-lg center-block" id="text">';
                html+='<h1 align="center">'+obj.title+'</h1>';
                html+='<p>'+obj.description+'</p>';
                html+='</div>';
                $("#resText").append($(html));
                nextchapter = nextchapter + 1;
                $(".footer").hide();
                query_status =1;
            },
            //complete:function(){$(".footer").hide();},
            error:function(XMLResponse){alert(XMLResponse.responseText)}
          });//.ajax
      }
    })