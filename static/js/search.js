var listgroup = '<div class="list-group"></div>';
var query_status = 1;
function status_inc() { 
        query_status = query_status + 1;
        if(query_status > 0){$(".progress").hide();}
        else{$(".progress").show();}
} 
function status_des() { 
        query_status = query_status - 1;
        if(query_status > 0){$(".progress").hide();}
        else{$(".progress").show();}
} 
function fail(str){
    $("#aldiv")
    .prepend('<div class="alert alert-dismissible alert-danger"><button class="close" type="button" data-dismiss="alert">&times;</button><strong>'+str+'</strong></div>')
    .children(':first')
    .delay(5000)
    .fadeOut(1000);
}

function Retrieve(id,novelname,restrict){
    if($("#bookmark").prop("checked")){bookmark=1}else{bookmark=0}
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/retrieve',
        data: {"bookmark": bookmark, "id": id , "novelname": novelname, "restrict":restrict},
        beforeSend:function(){status_des()},
        complete:function(data){
            obj = data.responseText;
            if (obj=='SUCCESS'){
                status_inc();
                location = "/" + novelname;
            }
            if (obj=='EXIST'){
                $('#rewrite').attr("onclick","Retrieve('"+id+"','"+novelname+"','1')");
                $('#myModal').modal();
                status_inc();
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
        beforeSend:function(){status_des()},
        complete:function(data){
                obj = JSON.parse(data.responseText);
                if ('error' in obj){
                        fail(obj.error);
                        status_inc();
                        return false;
                }
            html+='<a class="list-group-item row" style="cursor: pointer;" onclick="Retrieve(\''+ obj.id+'\',\''+obj.title +'\',0)">';
            html+='<h4 class="list-group-item-heading">'+ obj.website + ' - ' + obj.title +'</h4>';
            html+='<span class="list-group-item-text col-md-4">最新章节：'+ obj.latest +'</span>';
            html+='<span class="list-group-item-text col-md-4">更新时间：'+ obj.update +'</span>';
            html+='<span class="list-group-item-text col-md-4">来源：'+ obj.homepage +'</span>';
            html+='</a>'
            $(".list-group").append($(html));
            status_inc();
        },
        //error:function(XMLResponse){alert(XMLResponse.responseText);}
    })
}

function search(){
    if (query_status == 0){return false};
    $.ajax({
    type:'post',
    dataType:'json',
    url:'/search',
    data: {"novelname": $("#search-novel").val()},
    beforeSend:function(){status_des()},
    complete:function(id){
        idlist = JSON.parse(id.responseText);
        $(".list-group").remove();
        $(".container").append($(listgroup));
        for (i in idlist.id) {
            getnovel(idlist.id[i]);
        }
        status_inc();
    },
    //success:
    error:function(XMLResponse){alert(XMLResponse.responseText)}
    });//.ajax
    
}

$(document).ready(function(){
    $("#search-novel").val(localStorage.novelname);
    localStorage.removeItem("novelname");
    if(query_status > 0){
    $(".progress").hide();
    }
    else{$(".progress").show();}
})
