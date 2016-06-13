function updated(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-success"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>更新成功！</strong></div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
}
function fail(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-danger"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>更新失败！</strong></div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
}
function noupdate(){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-info"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>没有更新。</strong></div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
}

var query_status = 1;

function update(){
    if (query_status == 0){return false}
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/'+$("title").html(),
        //data: { "id": $("#resource").html() , "novelname": $("title").html(), "restrict":"1" },
        beforeSend:function(){query_status =0},
        complete:function(data){
            obj = data.responseText;
            if (obj == 0){noupdate();query_status =1;return false}
            if (obj < 0){fail();query_status =1;return false}
            else{
                obj = JSON.parse(data.responseText);
                obj = obj.list;
                for (item in obj){
                    $('<a class="list-group-item col-lg-4" id="chapterlink" href=""></a>').attr("href","/"+ $("title").html()+'/'+obj[item].index).html(obj[item].name + '<span class="badge">新</span>').appendTo($(".list-group"));
                    }
                updated();
            }
            query_status =1;
        },
        error:function(XMLResponse){fail();query_status =1;}
    });
}

function del(){
    if (query_status == 0){return false}
    var title = $("title").text();
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/del',
        data: {"novelname": title},
        beforeSend:function(){query_status =0},
        complete:function(data){
            obj = data.responseText;
            if (obj == '0'){location = "/";}
            query_status =1;
        },
        error:function(XMLResponse){alert(XMLResponse.responseText);query_status =1}
    });
}

function change(){
    localStorage.novelname=$("title").text();
    location = "/search";
}