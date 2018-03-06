//用户创建的社区
function get_user_create_community (pageNo){
    var data= {};
    data['user_id'] = view_user_info_id;
    data['no']=pageNo;
    data['size']=pageSize;
    $.ajax({
        type: 'POST',
        url: '/get_user_create_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            has_next = data.has_next;
            community_list = data.community_list;
            total_size =  data.total_size;
            if(total_size==0){
                if(login_user_id==view_user_info_id){
                    msg = '您还没有创建岛!'
                }else{
                     msg = view_user_info_name+'还没有创建过岛!'
                }
                community_html='<div class="empty">\
                  <span><img src="../images/empty-community.png"></span>\
                  <p>'+msg+'</p>\
                </div>'
                $('.community').html(community_html);
                return;
            }
            var community_html = '';
            for(var i=0;i<community_list.length;i++){
                var community = community_list[i]
                community_html= community_html+'<div class="item">\
                        <div class="img">\
                            <a href="/community?id='+community.id+'&type=query"><img src="'+community.head_img_url+'"></a>\
                        </div>\
                        <div class="content">\
                            <h4><a href="/community?id='+community.id+'&type=query">'+community.name+'岛</a></h4>\
                            <p>'+community.describe+'</p>\
                            <div class="block-bar">\
                                <div class="row-1x">\
                                    <div class="group-span-1x">\
                                        <span><em>帖子</em><b>'+community.post_num+'</b></span>\
                                        <span><em>成员</em><b>'+community.user_num+'</b></span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </div>';
            }
            $('.community').html(community_html);
        }
    });
}
//离开社区
function leftCommunity(community_id){
    var data = {};
    data['type'] = 'left';
    data['user_id'] = view_user_info_id;
    data['community_id'] = community_id;
    $.ajax({
        type: 'POST',
        url: '/user_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            $('.community').find('#c_'+community_id).remove();
            if( $('.community').html()=='' && pageNo>1){
                pageNo -=1;
                var url = "/user_info_community_join?user_id=" + user_id + "&no=" + pageNo + "&size=" + pageSize+"&type=joined";
                console.debug("pageurl:", url);
                window.location.href = url;

            }else if($('.community').html()=='' && pageNo==1){
                $('ul.pagination').empty();
            }
        },
        error: function(xhr, type) {
            console.log('操作失败!')
        }
    })

}
//用户加入的社区
function loadJoinedCommunity(pageno){
    var data = {};
    data['type'] = 'joined';
    data['user_id'] = view_user_id;
    data['no']=pageNo;
    data['size']=pageSize;
    $.ajax({
        type: 'get',
        url: '/community_joined',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            has_next = data.has_next;
            var community_list = data.community_list;
            var community_html = '';
            if(community_list.length==0){
                if(login_user_id==view_user_info_id){
                    msg = '您还没有加入岛!'
                }else{
                     msg = view_user_info_name+'还没有加入过岛!'
                }
                community_html='<div class="empty">\
                  <span><img src="../images/empty-community.png"></span>\
                  <p>'+msg+'</p>\
                </div>'
                $('.community').html(community_html);
                return;
            }
            for(var i=0;i<community_list.length;i++){
                community = community_list[i];
                var flag =login_user_id>0 && view_user_id==login_user_id && view_user_id!=community.owner_user_id ;
                var left_html =''
                if(flag){
                    left_html = '<div class="right-control"><a href="javascript:void(0)" onclick="leftCommunity('+community.id+')" class="btn btn-primary">离岛</a></div>';
                }

                community_html += '<div id="c_'+community.id+'" class="item">\
                            <div class="img">\
                                <a href="community?id='+community.id+'&type=query"><img src="'+community.head_img_url+'"></a>\
                           </div>\
                            <div class="content">\
                                <h4><a href="community?id='+community.id+'&type=query">'+community.name+'岛</a></h4>\
                                <p>'+community.describe+'</p>\
                                <div class="block-bar action">\
                                    <div class="row-1x">\
                                        <div class="group-span-1x">\
                                            <span><em>帖子</em><b>'+community.post_num+'</b></span>\
                                            <span><em>成员</em><b>'+community.user_num+'</b></span>\
                                        </div>\
                                    </div>\
                                    '+left_html+'\
                                </div>\
                            </div>\
                        </div>';
            }
            $('.community').append(community_html)
            pageNo = data['no'];
            pageSize = data['size']
            totalCount  = data['totalCount']
            totalPages = data['totalPages']
        },
        error: function(xhr, type) {
            console.log('社区加载失败!')
        }
    })

}
//删除帖子
function deletePost(postid) {
        swal({
          title: "你确定删除帖子吗?",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#B19270",
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          closeOnConfirm: false,
          closeOnCancel: true
        },
        function(isConfirm){
            if(isConfirm){
                var data = { 'post_id': postid }
                $.ajax({
                    url: '/delete_post',
                    type: 'POST',
                    data: data,
                    success: function(data) {
                        if (data.result == 0) {
                            window.location.reload();
                        } else {
                            console.log('删除失败!')
                        }
                    },
                    error: function(data) {
                        console.log('删除失败!')
                    }
                })
            }
    });
}
//用户发布的帖子
function loadUserPost(page_no) {
        var data = {};
        data['no'] = page_no;
        data['user_id'] = view_user_info_id
        data['size'] = num_perpage
        $.ajax({
            type: 'GET',
            url: '/get_user_post',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                var post_list = data.post_list;
                total = data.total_size;
                has_next = data.has_next;
                if(total==0){
                    if(login_user_id==view_user_info_id){
                        msg = '您还没有发过帖子!'
                    }else{
                         msg = view_user_info_name+'还没有发过帖子!'
                    }
                   user_post_wrap='<div class="empty">\
                      <span><img src="../images/empty-post.png"></span>\
                      <p>'+msg+'</p>\
                    </div>'
                    $('.my-list').html(user_post_wrap);
                    return;
                }
                if (post_list.length > 0) {
                    var user_post_wrap = '';
                    for (var i = 0; i < post_list.length; i++) {
                        var user = post_list[i].user;
                        var community = post_list[i].community;
                        var img_array = post_list[i].content.match(/<img[^>]+>/g);
                        var content = post_list[i].content.replace(/<[^>]+>/g, "");
                        if (content.length > 100) {
                            content = content.substring(0, 100) + '...';
                        }
                        var like_num = '';
                        var imgs = '';
                        if (img_array != null && img_array.length > 0) {
                            imgs = '<ul>';
                            var count = 0;
                            for (var j = 0; j < img_array.length && count < 9; j++) {
                                if (img_array[j].indexOf('images/img') < 0) {
                                    imgs = imgs + '<li>' + img_array[j] + '</li>';
                                    count++;
                                }
                            }
                            imgs = imgs + '</ul>'
                        }
                        like_num = '<span><em>喜欢</em><b>' + post_list[i].like_num + '</b></span>';
                        var approve_html = '';
                        if(user.is_approve>0){
                            approve_html = '<span title="个人认证"  class="mark-i s v"><i class="icon-v"></i></span>';
                        }
                        user_post_wrap += '<div class="item">\
                            <div class="photo">\
                                <a href="/user_info_post?type=1&user_id=' + user.id + '"><img src="' + user.head_img_url + '"></a>\
                            </div>\
                            <div class="content">\
                            <div class="block-bar">\
                                <span><a href="/user_info_post?type=1&user_id=' + user.id + '">' + user.name + '</a></span>\
                                '+approve_html+'\
                                <span>' + post_list[i].create_time + '</span>\
                            </div>\
                                <h4><a href="post?id=' + post_list[i].id + '&type=postInfo">' + post_list[i].title + '</a></h4>\
                                <p>' + content + '</p>\
                                ' + imgs + '\
                                <div class="block-bar">\
                                 ' + like_num + '\
                                   <span><em>评论</em><b>' + post_list[i].floor_num + '</b></span>\
                                    <div class="control-right">\
                                        <div class="row-1x">\
                                            <div class="group-span-1x">\
                                            <span>来自：<a href="/community?id=' + community.id + '&type=query">' + community.name + '岛</a></span>\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>';

                    }
                $('.my-list').append(user_post_wrap);
                }
            },
            error: function(xhr, type) {
                console.log('加载失败!')
            }
        })
}
//好友
function get_user_friend(pageNo){
    var data = {};
    data['user_id'] = view_user_info_id;
    data['no']=pageNo;
    data['size']=pageSize;
    $.ajax({
        type: 'POST',
        url: '/get_user_friend',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            has_next = data.has_next;
            friend_list = data.friend_list;
            total_size = data.total_size;
            if(total_size==0){
                if(login_user_id==view_user_info_id){
                    msg = '您还没有好友!'
                }else{
                     msg = view_user_info_name+'还没有好友!'
                }
                friend_html='<div class="empty">\
                  <span><img src="../images/empty-friend.png"></span>\
                  <p>'+msg+'</p>\
                </div>';
                $('.user-list').html(friend_html);
                return;
            }
            var friend_html = '';
            for(var k=0;k<friend_list.length;k++){
                var friend = friend_list[k];
                var friend_is_approve ='';
                if(friend.user.is_approve>0){
                   friend_is_approve ='<span class="mark-i s2 s v"><i class="icon-v"></i></span>';
                }
                friend_html= friend_html+'<div class="item">\
                            <div class="img">\
                                <a href="user_info_post?user_id='+friend.user.id+'"><img src="'+friend.user.head_img_url+'"></a>\
                            </div>\
                            <div class="content">\
                                <h4><a href="user_info_post?user_id='+friend.user.id+'">'+friend.user.name+'</a></h4>\
                                '+friend_is_approve+'\
                                <p>'+friend.user.label+'</p>\
                                <div class="block-bar action">\
                                    <div class="row-1x">\
                                        <div class="group-span-1x">\
                                            <span><em>帖子数</em><b>'+friend.user.post_num+'</b></span>\
                                            <span><em>粉丝数</em><b>'+friend.user.by_attention_num+'</b></span>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>';
            }
            $('.user-list').append(friend_html);
        }
    });
}
