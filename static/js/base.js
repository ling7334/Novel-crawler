var flash_message = function (category, message) {
    // category为消息类别，可为info，success，danger
    // message为消息内容
    $("#message")
    .prepend('<div class="alert alert-dismissible alert-'+category+'"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>'+message+'</strong></div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
}

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
    // 当loading大于0时显示进度条
    if(loading <= 0){
        loading=0;
        $("#loading").hide();
    } else { 
        $("#loading").show();
    }
});
