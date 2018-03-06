var has_next = false;
function initData(){
    $('.friend-list li:first').addClass('active');

}

function makeMineHtml(message){
    var user = message.user;
    var user_html = '<li class="chat-mine">\
                        <div class="chat-user"><img src="'+user.head_img_url+'" /></div>\
                        <div class="chat-content">'+message.content+'\
                        </div>\
                    </li>';
    return user_html;
}
function makeChaterhtml(message){
    var chat_html ='<li>\
                        <div class="chat-user"><img src="'+message.user.head_img_url+'"/></div>\
                        <div class="chat-content">'+message.content+'\
                        </div>\
                    </li>';
    return chat_html;
}
$('#send').click(function(){
    var content =$('#smile-editor').html(); //$('#editor').html();
    if(content==''){
        sweetInfo({text:'发送内容不能为空!',type:'info'});
        return;
    }
    to_user_id = $('#chatWith').val()
    var data= {}
    data['type'] ='send';
    data['to_user_id'] = to_user_id;
    data['content'] = content;
    $.ajax({
        url:'/save_message',
        type:'POST',
        data:data,
        dataType: 'json',
        timeout: 5000,
        success:function(data){
            if(pageNo>1){
                scroll_bottom = true;
            }
            if(data.result.code==0){
                message=data.result.data;
                $("#containerScroll").append(makeMineHtml(message));
                $('#smile-editor').empty();
                $('#smile-editor').focus();
            }else{
                sweetInfo({title:'提示',text:'发送失败!',type:'timer'});
            }
        },
        error:function(data){
             console.log('发送失败!');
        }
    })
})

function getHistoryMessage(to_user_id){
    $('#chatWith').val(to_user_id);
    $('.friend-list>li#u_'+to_user_id).find('b.circle_sm').remove();
    var data = {}
    data['type']='history_message';
    data['to_user_id'] = to_user_id;
    data['page_no'] = pageNo;
    data['num_perpage'] = pageNum;
    $.ajax({
        url:'/get_history_message',
        type:'get',
        data:data,
        dataType: 'json',
        timeout: 5000,
        success:function(data){
            var new_message='';
            var mess_list= data.result;
            has_next = data.has_next;
            if(mess_list.length>0){
                for(var i =0;i<mess_list.length;i++){
                    if(mess_list[i].create_user_id==login_user_id){
                        new_message+=makeMineHtml(mess_list[i])
                    }else{
                        new_message+=makeChaterhtml(mess_list[i])
                    }
                }
                if(pageNo==1){
                    new_message+='<li class="msg-tip">历史消息</li>';
                    $('ul#containerScroll').empty().html(new_message);
                }else{
                    $('ul#containerScroll').prepend(new_message);
                }
            }else{
            console.log('暂无数据')
            }
        }
    })
}

(function longPolling() {
   to_user_id = $('#chatWith').val();
   var data= {}
   data['type'] = 'new_message'
   data['create_user_id'] = to_user_id
    $.ajax({
        url: "/get_new_message",
        data: data,
        dataType: "json",
        timeout: 5000,
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus == "timeout") { // 请求超时
                    console.log('请求超时')
                }
            },
        success: function (data) {
             message_list=data.result;
             var len = message_list.length
             if(len>0){
                var new_message='';
                for(var i =0;i<message_list.length;i++){
                    new_message+=makeChaterhtml(message_list[i])
                }
                $("#containerScroll").append(new_message);
                 // 这里必须用[] 否则返回undefined,调节内容的高度，有新消息时 滚动到最下
                // $("#containerScroll").scrollTop($("#containerScroll")[0].scrollHeight);
             }
            setTimeout(longPolling, 2000);//5000毫秒，自己定义延迟时间
        }
    });
})();