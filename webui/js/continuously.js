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
          var nexturl = '/'+ novelname + '/' + nextchapter;
          $.ajax({
            type:'post',
            dataType:'json',
            url: nexturl,
            beforeSend:function(){$(".footer").show();query_status =0},
            success:function(data){
                if (data.status == "404") {
                    $(".footer").hide();
                    query_status =1;
                    alert(data.message);
                    return false;}
                html+='<div class="well well-lg center-block" id="text">';
                html+='<h1 align="center">'+data.title+'</h1>';
                html+='<p>'+data.description+'</p>';
                html+='</div>';
                $("#resText").append($(html));
                nextchapter = nextchapter + 1;
                $(".footer").hide();
                query_status =1;
            },
            error:function(XMLResponse){alert(XMLResponse.responseText)}
          });//.ajax
      }
    })