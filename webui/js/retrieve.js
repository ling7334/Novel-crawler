function Retrieve(id,novelname,restrict){
    if (query_status == 0){return false}
    if($("#bookmark").prop("checked")){bookmark=1}else{bookmark=0}
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/retrieve',
        data: {"bookmark": bookmark, "id": id , "novelname": novelname, "restrict":restrict},
        beforeSend:function(){$(".progress").show();query_status =0},
        complete:function(data){
            obj = data.responseText;
            if (obj=='SUCCESS'){
                query_status =1;
                location = "/" + novelname;
            }
            if (obj=='EXIST'){
                $('#rewrite').attr("onclick","Retrieve('"+id+"','"+novelname+"','1')");
                $('#myModal').modal();
                query_status =1;
            }
            // alert(obj);
            $(".progress").hide();
            query_status =1;
        },
        //error:function(XMLResponse){alert(XMLResponse.responseText);query_status =1;}
    });
}