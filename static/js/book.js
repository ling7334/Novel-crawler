function update(){
    if (loading >= 0){return false}
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/'+$("title").html(),
        //data: { "id": $("#resource").html() , "novelname": $("title").html(), "restrict":"1" },
        beforeSend:function(){loading+=1},
        complete:function(data){
            obj = data.responseText;
            if (obj == 0){flash_message('info', '没有更新！');query_status =1;return false}
            if (obj < 0){flash_message('danger', '更新失败！');query_status =1;return false}
            else{
                obj = JSON.parse(data.responseText);
                obj = obj.list;
                for (item in obj){
                    $('<a class="list-group-item col-lg-4" id="chapterlink" href=""></a>').attr("href","/"+ $("title").html()+'/'+obj[item].index).html(obj[item].name + '<span class="badge">新</span>').appendTo($(".list-group"));
                    }
                flash_message('success', '更新成功！');
            }
            loading-=1;
        },
        error:function(XMLResponse){alert(XMLResponse.responseText);loading-=1;}
    });
}

function del(){
    if (loading>=0){return false}
    var title = $("title").text();
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/del',
        data: {"novelname": title},
        beforeSend:function(){loading+=1},
        complete:function(data){
            obj = data.responseText;
            if (obj == '0'){location = "/";}
            loading-=1;
        },
        error:function(XMLResponse){alert(XMLResponse.responseText);loading-=1;}
    });
}

function change(){
    localStorage.novelname=$("title").text();
    location = "/search";
}