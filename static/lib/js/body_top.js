<!--用户名点击-->
$("body").click(function(e){
    e = e || window.event;
    var obj =e.target || e.srcElement;
    if($(obj).closest(".search-group").length <=0){
        $(".suggest-container").addClass('hide');
    }
});
<!--信息提示-->
function  sweetInfo(options){
   /*type:info,error,warning,success*/
   type = options.type;
   text = options.text;
   title = options.title || '';
   switch(options.type){
        case "info":
            swal({
                title:title,
                text:text,
                type:'info',
                confirmButtonText:'确定',
                confirmButtonColor:'#B19270'
            });
            break;
        case "warning":
             swal({
                title:'',
                text:text,
                type:type,
                confirmButtonText:'确定',
                confirmButtonColor:'#B19270'
            });
            break;
        case "timer":
            swal({
                title:title,
                text:text,
                timer: 1000,
                showConfirmButton: false
            });
            break;
   }

}
$('#createCommunity').click(function(){
   var name=$("input[name='cummunityname']").val();
   var desc=$('textarea[name="communitydesc"]').val();
   if($.trim(desc)=="" || $.trim(desc)=="输入社区简介，提升人气" || desc.length==0){
      sweetInfo({title:'提示',text:'请输入社区简介!',type:'info'});
      return false;
   }
   console.log($.trim(name).length)
   console.log($.trim(desc).length)
   if($.trim(name).length>20){
        sweetInfo({title:'提示',text:'社区名称不能超过20个字符!',type:'info'});
        return false;
   }
    if($.trim(desc).length>100){
        sweetInfo({title:'提示',text:'社区简介不能超过100个字符!',type:'info'});
        return false;
   }
   var head_img_url = $('#modal_new').find('a[href="#photo"]').find('img').attr('src');
    var data={};
    data['name'] =name;
    data['describe'] = desc;
    data['head_img_url'] = head_img_url;
    data['type']='publish'
    $.ajax({
      type:'POST',
      url:'/community_create',
      data:data,
      dataType:'json',
      success:function(data){
        if (data['code']==0){
             $('button[data-dismiss="modal"]').trigger('click');
             community = data.community
             window.location.href='/community?id='+community.id+'&type=query';
        }else{
           console.log('创建失败!')
        }
        $("input[name='cummunityname']").val('');
        $('textarea[name="communitydesc"]').val('');
      },
      error:function(xhr,type) {
        console.log('创建失败!')
      }
    });
    return false;
})

function to_log_out() {
data={};
$.ajax({
  type:'POST',
  url:'/logout',
  data:data,
  dataType:'json',
  success:function(data){
    if (data['succ']==0){
        location.reload();
    }
  },
  error:function(xhr,type) {
  }
});
return false;
}

function toCreate(){
if(login_user_id>0){
    var name = $('#search_input_community_post_person').val()
    $("input[name='cummunityname']").val(name);
}else{
    sweetInfo({text:'登录后才能创建社区哦!',type:'info'});
    return false;
}
}

function to_log_in() {
 var cur_url=this.location.href;
 window.location.href="/login?next_url="+cur_url;
}
$('#search_input_community_post_person').focus(function(){
  var name = $('#search_input_community_post_person').val();
  if(name.trim()==''){
     $(".suggest-container").addClass('hide');
  }
})
$('#search_input_community_post_person').keyup(function(){
    var name = $('#search_input_community_post_person').val();
    if(name.trim().length === 0){
        $(".suggest-container").addClass('hide');
        return;
    }
   find_match_community(name);
})
function find_match_community(name){
   if(name.trim()!=""){
       $.ajax({
           url:'/search',
           type:'get',
           data:{
               name:name
               },
           dataType:'json',
           timeout:5000,
           success:function(data){
                $(".suggest>.item:first").nextAll().remove();
                post_list = data.post_list;
                user_list = data.user_list;
                adverse_list = data.adverse_list;
                var user_html ='';
                var post_html ='';
                if(user_list != null && user_list.length>0){
                    var each_user ='';
                    for(var k=0;k<user_list.length;k++){
                        each_user = each_user +'<div class="item">\
                                        <div class="img">\
                                            <a href="/user_info_post?type=1&user_id='+user_list[k].id+'"><img src="'+user_list[k].head_img_url+'"></a>\
                                        </div>\
                                        <div class="content">\
                                            <h4><a href="/user_info_post?type=1&user_id='+user_list[k].id+'">'+user_list[k].name+'</a></h4>\
                                        </div>\
                                    </div>';
                    }

                    user_html ='<div class="heading">用户</div>\
                                    <div class="body">\
                                        <div class="user-list user-list-basic">\
                                           '+each_user+'\
                                        </div>\
                                    </div>';
                }
                if(post_list != null && post_list.length>0){
                    var each_post ='';
                    for(var j = 0;j<post_list.length;j++ ){
                        each_post = each_post+'<li><a href="/post?id='+post_list[j].id+'&type=postInfo">'+post_list[j].title+'</a></li>';
                    }
                    post_html = '<div class="item">\
                                  <div class="heading">帖子<span style="position: absolute; right:30px"><a href="/search_result?name='+name+'">查看所有帖子</a></span></div>\
                                    <div class="body">\
                                        <ul class="list sm">\
                                            '+each_post+'\
                                        </ul>\
                                    </div>\
                                 </div>';
                }
                if(user_html != '' || post_html != '' ){
                    var user_post = '<div class="item">\
                                        '+user_html+post_html+'\
                                     </div>';
                    $('.suggest').append(user_post);
                }
               var drop_menu_html='';
               if(data.comm_list !=null && data.comm_list.length>0){
                 communities = data.comm_list;
                 for(var i =0;i<communities.length;i++){
                   drop_menu_html = drop_menu_html +'<li><a href="/community?type=query&id='+communities[i].id+'">'+communities[i].name+'</a></li>';
                 }
               } else {
                  if(login_user_id>0){
                    drop_menu_html='<li>目前还没有<span class="text-primary">'+name+'</span>岛,赶紧<span class="offset-1x"><a onclick="toCreate()"  href="#modal_new" data-toggle="modal"  class="btn btn-sm btn-default">去创建</a> 当岛主吧</span></li>';
                  }else{
                     drop_menu_html='<li>目前还没有<span class="text-primary">'+name+'</span>岛,赶紧<span class="offset-1x"><a onclick="toCreate()"  href="javascript:void(0)" data-toggle="modal"  class="btn btn-sm btn-default">去创建</a> 当岛主吧</span></li>';
                  }
               }
               $('ul.s-community').html(drop_menu_html);
               $('.suggest-container').removeClass('hide');

           }
       })
   }
}
$('#search').click(function(){
    var name = $('#search_input_community_post_person').val();
    if(name.trim()!=''){
        window.location.href='/search_result?name='+name;
    }
})