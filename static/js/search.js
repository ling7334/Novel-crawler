var listgroup = '<div class="list-group"></div>';

function Retrieve(id,novelname,restrict){
    if($("#bookmark").prop("checked")){bookmark=1}else{bookmark=0}
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/retrieve',
        data: {"bookmark": bookmark, "id": id , "novelname": novelname, "restrict":restrict},
        beforeSend:function(){loading +=1},
        complete:function(data){
            obj = data.responseText;
            if (obj=='SUCCESS'){
                loading -=1;
                location = "/" + novelname;
            }
            if (obj=='EXIST'){
                $('#rewrite').attr("onclick","Retrieve('"+id+"','"+novelname+"','1')");
                $('#myModal').modal();
                loading -=1;
            }
            // alert(obj);
        },
        //error:function(XMLResponse){alert(XMLResponse.responseText);query_status =1;}
    });
}

function getnovel(id){
    var html="";
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/search',
        data: { "id": idlist.id[i], "novelname": $("#search-novel").val() },
        beforeSend:function(){loading +=1},
        complete:function(data){
                obj = JSON.parse(data.responseText);
                if ('error' in obj){
                        flash_message('danger', obj.error);
                        loading -=1;
                        return false;
                }
            html+='<a class="list-group-item row" style="cursor: pointer;" onclick="Retrieve(\''+ obj.id+'\',\''+obj.title +'\',0)">';
            html+='<h4 class="list-group-item-heading">'+ obj.website + ' - ' + obj.title +'</h4>';
            html+='<span class="list-group-item-text col-md-4">最新章节：'+ obj.latest +'</span>';
            html+='<span class="list-group-item-text col-md-4">更新时间：'+ obj.update +'</span>';
            html+='<span class="list-group-item-text col-md-4">来源：'+ obj.homepage +'</span>';
            html+='</a>'
            $(".list-group").append($(html));
            loading -=1;
        },
        //error:function(XMLResponse){alert(XMLResponse.responseText);}
    })
}

function search(){
    if (loading > 0){return false};
    $.ajax({
    type:'post',
    dataType:'json',
    url:'/search',
    data: {"novelname": $("#search-novel").val()},
    beforeSend:function(){loading +=1},
    complete:function(id){
        idlist = JSON.parse(id.responseText);
        $(".list-group").remove();
        $(".container").append($(listgroup));
        for (i in idlist.id) {
            getnovel(idlist.id[i]);
        }
        loading -=1;
    },
    //success:
    error:function(XMLResponse){alert(XMLResponse.responseText)}
    });//.ajax
    
}

$(document).ready(function(){
    $("#search-novel").val(localStorage.novelname);
    localStorage.removeItem("novelname");
})
