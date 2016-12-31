var topper = '<div id="topcontrol" title="返回顶部" class="bg-primary" style="font-size: 30px; justify-content:center; align-items:center; display: -webkit-box; display: -moz-box; display: -ms-flexbox; display: -webkit-flex; display: flex; position: fixed; bottom: 30px; right: 30px; opacity: 1; cursor: pointer; width:50px; height:50px; border:0;"><span class="glyphicon glyphicon-chevron-up"></span></div>'

$(document).ready(function(){
    $("body").append($(topper));
    $("#topcontrol").hide();
    //当滚动条的位置处于距顶部600像素以下时，跳转链接出现，否则消失
    $(function () {
        $(window).scroll(function(){
            if ($(window).scrollTop()>400){
                $("#topcontrol").fadeIn(300);
            }else{
                $("#topcontrol").fadeOut(300);
            }
        });
        //当点击跳转链接后，回到页面顶部位置
        $("#topcontrol").click(function(){
            $('body,html').animate({scrollTop:0},300);
            return false;
        });
    });
});