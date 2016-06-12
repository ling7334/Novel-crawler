function okkey(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-success"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>成功！</strong>清空缓存以更新。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#submit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#submit").addClass('btn-success');
}
function fkey(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-danger"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>失败！</strong>哪里出错了。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#submit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#submit").addClass('btn-danger');
}

function init(){
    var query_status =1;
    $.ajax({
            type:'post',
            dataType:'json',
            url:'/config',
            beforeSend:function(){query_status =0},
            data: {"access": "getsetting"},
            complete:function(data){
                obj = JSON.parse(data.responseText);
                if (obj){
                    localStorage.continuously = obj.continuously;
                    localStorage.bold = obj.bold;
                    localStorage.fontcolor = obj.fontcolor;
                    localStorage.bkcolor = obj.bkcolor;
                    localStorage.fontsize = obj.fontsize;
                    var div = document.createElement('div');
                    div.innerHTML = obj.fontfamily;
                    localStorage.fontfamily =  div.innerText;
                }
                else{
                    localStorage.continuously = true;
                    localStorage.bold = false;
                    localStorage.fontcolor = "black";
                    localStorage.bkcolor = "#8FBC8F";
                    localStorage.fontfamily = "黑体";
                    localStorage.fontsize = "30px";
                }
                reset();
                query_status =1;
            },
            error:function(){query_status =1;}
          });//.ajax
}

function save(){
    $.ajax({
            type:'post',
            dataType:'json',
            url:'/config',
            beforeSend:function(){query_status =0},
            data: {
                 "access"       : "savesetting",
                 "continuously" : document.getElementById("continuously").checked,
                 "bold"         : document.getElementById("bold").checked,
                 "fontcolor"    : $("#fontcolor").val(),
                 "bkcolor"      : $("#bkcolor").val(),
                 "fontfamily"   : $("#fontfamily").val(),
                 "fontsize"     : $("#fontsize").val(),
            },
            complete:function(data){
                obj = JSON.parse(data.responseText);
                if (obj == '0'){
                    localStorage.continuously = document.getElementById("continuously").checked;
                    localStorage.bold = document.getElementById("bold").checked;
                    localStorage.fontcolor = $("#fontcolor").val();
                    localStorage.bkcolor = $("#bkcolor").val();
                    localStorage.fontfamily = $("#fontfamily").val();
                    localStorage.fontsize = $("#fontsize").val();
                    okkey();
                }
                else{fkey();}
                query_status =1;
            },
            error:function(){fkey();query_status =1;}
          });//.ajax
}

function reset(){
    if (localStorage.continuously == 'true'){
        $('#continuously').bootstrapSwitch('state', true);
    }
    else{
        $('#continuously').bootstrapSwitch('state', false);
    }
    if (localStorage.bold == 'true'){
        $('#bold').bootstrapSwitch('state', true);
    }
    else{
        $('#bold').bootstrapSwitch('state', false);
    }


    //$("#bkcolor").attr("value",localStorage.bkcolor);
    $("#bkcolor").val(localStorage.bkcolor);
    $("#bkcolor-display").css("background",localStorage.bkcolor);

    //$("#fontcolor").attr("value",localStorage.fontcolor);
    $("#fontcolor").val(localStorage.fontcolor);
    $("#fontcolor-display").css("background",localStorage.fontcolor);

    //$("#fontfamily").attr("value",localStorage.fontfamily);
    $("#fontfamily").val(localStorage.fontfamily);
    $("#fontfamily").css("font-family",localStorage.fontfamily);

    //$("#fontsize").attr("value",localStorage.fontsize);
    $("#fontsize").val(localStorage.fontsize);
    $("#fontsize").css("font-Size",localStorage.fontsize);
}

$(document).ready(function(){
    init();

    $("#fontcolor").change(function(){ 
        $("#fontcolor-display").css("background",$(this).val());
        });

    $("#bkcolor").change(function(){ 
        $("#bkcolor-display").css("background",$(this).val());
        });
        
    $("#fontsize").change(function(){
        $(this).css("font-Size", $(this).val()); 
        });
    $("#fontfamily").change(function(){
        $(this).css("font-family", $(this).val()); 
        });
})