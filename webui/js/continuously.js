$(function(){
      $(window).bind('scroll',function(){show()});
      $(".footer").hide();
      $(".pager").hide();
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
        //   $.getJSON('/json/'+ novelname + '/' + nextchapter, function(data) {
        //             obj = JSON.parse(data.responseText)
        //             html+='<div class="well well-lg center-block">';
        //             html+='<h1 align="center">'+obj.title+'</h1>';
        //             html+='<p id="text">'+obj.description+'</p>';
        //             html+='</div>';
        //             $("#resText").append($(html));
        //             nextchapter = nextchapter + 1
        //             $(".footer").hide();
        //             }
        //         );
          $.ajax({
            //type:'get',
            //dataType:'json',
            url:'/json/'+ novelname + '/' + nextchapter,
            beforeSend:function(){$(".footer").show()},
            complete:function(data){
                obj = JSON.parse(data.responseText)
                html+='<div class="well well-lg center-block">';
                html+='<h1 align="center">'+obj.title+'</h1>';
                html+='<p id="text">'+obj.description+'</p>';
                html+='</div>';
                $("#resText").append($(html));
                nextchapter = nextchapter + 1
                $(".footer").hide();
            },
            //complete:function(){$(".footer").hide();},
            error:function(XMLResponse){alert(XMLResponse.responseText)}
          });//.ajax
      }
    })