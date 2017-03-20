$(document).ready(function(){
    var loading = 0;

    //当滚动条的位置处于距顶部600像素以下时，跳转链接出现，否则消失
    $(function () {
        $(window).scroll(function(){
            if ($(window).scrollTop()>400){
                $("#topper").fadeIn(300);
            }else{
                $("#topper").fadeOut(300);
            }
        });
        //当点击跳转链接后，回到页面顶部位置
        $("#topper").click(function(){
            $('body,html').animate({scrollTop:0},300);
            return false;
        });
    });

    if(loading <= 0){
        loading=0;
        $("#loading").hide();
    } else { 
        $("#loading").show();
    }
});
