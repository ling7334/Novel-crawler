$(".progress").hide();
var listgroup = '<div class="list-group"></div>';
var query_status = 1;

function getnovel(i,id){
    if (id[i] == null){return false}
    var html="";
    if (query_status==i){
                $.ajax({
                    type:'post',
                    dataType:'json',
                    url:'/search',
                    data: { "id": idlist.id[i], "novelname": $("#search-novel").val() },
                    beforeSend:function(){$(".progress").show();query_status =i},
                    complete:function(data){
                        obj = JSON.parse(data.responseText);
                        html+='<a class="list-group-item row" style="cursor: pointer;" onclick="Retrieve(\''+ obj.id+'\',\''+obj.title +'\',0)">';
                        html+='<h4 class="list-group-item-heading">'+ obj.website + ' - ' + obj.title +'</h4>';
                        html+='<span class="list-group-item-text col-md-4">最新章节：'+ obj.latest +'</span>';
                        html+='<span class="list-group-item-text col-md-4">更新时间：'+ obj.update +'</span>';
                        html+='<span class="list-group-item-text col-md-4">来源：'+ obj.homepage +'</span>';
                        html+='</a>'
                        $(".list-group").append($(html));
                        $(".progress").hide();
                        query_status = i+1;
                        i=i+1;
                        getnovel(i,id);
                    },
                    error:function(XMLResponse){alert(XMLResponse.responseText);}
                })
            }
}

function search(){
    if (query_status == 0){return false};
    $.ajax({
    type:'post',
    dataType:'json',
    url:'/search',
    data: {"novelname": $("#search-novel").val()},
    beforeSend:function(){$(".progress").show();query_status =0},
    complete:function(id){
        idlist = JSON.parse(id.responseText);
        $(".list-group").remove();
        $(".container").append($(listgroup));
        getnovel(0,idlist.id);
        //query_status =1;
    },
    //success:
    error:function(XMLResponse){alert(XMLResponse.responseText)}
    });//.ajax
    
}

$(document).ready(function(){
    $("#search-novel").val(localStorage.novelname);
    localStorage.removeItem("novelname");
})