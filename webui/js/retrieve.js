function Retrieve(id,novelname){
    $.ajax({
        type:'post',
        dataType:'json',
        url:'/retrieve',
        data: { "id": id , "novelname": novelname },
        beforeSend:function(){$(".progress").show()},
        complete:function(data){
            obj = data.responseText;
            if (obj==0){
                location = "/" + novelname;
            }
            // alert(obj);
            $(".progress").hide();
        }
    });
}