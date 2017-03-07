function readok(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-success"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>成功！</strong>清空缓存以更新。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#readsubmit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#readsubmit").addClass('btn-success');
}
function readfail(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-danger"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>失败！</strong>哪里出错了。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#readsubmit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#readsubmit").addClass('btn-danger');
}
function searchok(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-success"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>成功！</strong>清空缓存以更新。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#searchsubmit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#searchsubmit").addClass('btn-success');
}
function searchfail(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-danger"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>失败！</strong>哪里出错了。</div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
    $("#searchsubmit").removeClass('btn-primary').removeClass('btn-success').removeClass('btn-danger');
    $("#searchsubmit").addClass('btn-danger');
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
                    localStorage.config = obj.config;
                }
                else{
                    localStorage.continuously = true;
                    localStorage.bold = false;
                    localStorage.fontcolor = "black";
                    localStorage.bkcolor = "#8FBC8F";
                    localStorage.fontfamily = "黑体";
                    localStorage.fontsize = "30px";
                    localStorage.config = "";
                }
                readreset();
                searchreset();
                query_status =1;
            },
            error:function(data){alert(data.responseText);query_status =1;}
          })//.ajax
}

function readsave(){
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
                    readok();
                }
                else{readfail();}
                query_status =1;
            },
            error:function(data){alert(data.responseText);query_status =1;}
          })//.ajax
}

function readreset(){
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

    $("#bkcolor").val(localStorage.bkcolor);
    $("#bkcolor-display").css("background",localStorage.bkcolor);

    $("#fontcolor").val(localStorage.fontcolor);
    $("#fontcolor-display").css("background",localStorage.fontcolor);

    $("#fontfamily").val(localStorage.fontfamily);
    $("#fontfamily").css("font-family",localStorage.fontfamily);

    $("#fontsize").val(localStorage.fontsize);
    $("#fontsize").css("font-Size",localStorage.fontsize);
}

function searchsave(){
    $.ajax({
            type:'post',
            dataType:'json',
            url:'/config',
            beforeSend:function(){query_status =0},
            data: {
                 "access"       : "saveconfig",
                 "config"       : $("#searchconfig").val()
            },
            complete:function(data){
                obj = JSON.parse(data.responseText);
                if (obj == '0'){
                    localStorage.config = $("#searchconfig").val();
                    searchok();
                }
                else{searchfail();}
                query_status =1;
            },
            error:function(data){alert(data.responseText);query_status =1;}
          })//.ajax
}

function searchreset(){
    $("#searchconfig").val(localStorage.config);
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