$(document).ready(function(){
    $("#topcontrol").hide();
    //当滚动条的位置处于距顶部600像素以下时，跳转链接出现，否则消失
    $(function () {
        $(window).scroll(function(){
            if ($(window).scrollTop()>600){
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