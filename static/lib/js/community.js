//初始化页面
var total = 0;
var page_no = 1;
var num_page = 10;
initData();

function initData(){
   load_commend_community();
   var callbackPage = function(page_no){
       loadCommunityPost(page_no)
   }
   callbackPage(1);
   $('#editor').html('');
   $('#post_title').val('');
   $("#page").initPage(num_page,total,page_no,callbackPage);
}

// 修改社区名称和描述
$('#update-community').click(function() {
    var name = $('input[name=community-name]').val()
    var desc = $('textarea[name=community-desc]').val()
    if ($.trim(name) == '') {
        sweetInfo({text:'请填写社区名!',type:'info'});
        return;
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
    var data = {}
    data['id'] = community_id;
    data['name'] = name;
    data['desc'] = desc;
    data['type'] = 'update'
    $.ajax({
        type: 'POST',
        url: '/update_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            if (data.result == 0) {
                $('h4.hname').find('span').text(name);
                $('.content').find('p.pdesc').html(desc);
                $('#modal-community').modal('toggle')
            } else {
                console.log('修改失败!')
            }
        },
        error: function(xhr, type) {
            console.log('修改失败!')
        }
    })
})

function remove_match() {
    $('.post-suggest-container').find('.match-post').empty();
    $('.post-suggest-container').addClass('hide')
    $('button#submmit-btn').removeAttr("disabled");
    $('div#editor').attr('contenteditable', 'true');
}
$('#post_title').keyup(function() {
     var title = $('#post_title').val();
     if(title.trim().length === 0){
        $(".suggest-container").addClass('hide');
        return;
     }
    find_match_post(title);
})
function find_match_post(title) {
    if(title.trim()!=''){
        if (title.trim()!=""){
            $.ajax({
              url:'/find_match_post',
              type:'get',
              dataType:'json',
              async:false,
              data:{
                name:title
              },
              timeout:5000,
              success:function(data){
                  var posts = data.post_list;
                  var match_post ='';
                  if (posts !=null && posts.length>0){
                      for(var i =0;i<posts.length;i++){
                        match_post =match_post +'<li><a href="/post?id='+posts[i].id+'&type=postInfo">'+posts[i].title+'</a></li>'
                      }
                      $('.match-post').html(match_post);
                      $('#submit').val('false');
                      $('.post-suggest-container').removeClass('hide')
                      $('button#submmit-btn').attr('disabled','true');
                      $('div#editor').removeAttr('contenteditable');
                  }else{
                    remove_match();
                  }
              }

            })
        }
    }
 }

$('button#submmit-btn').click(function() {
    //get title
    var title = $("input#post_title").val();
    //get content
    var content = $('#editor').html();
    if ($.trim(title) == "" || $.trim(title) == '标题') {
        sweetInfo({text:'标题不能为空!',type:'info'});
        return;
    }
    if ($.trim(content) == "" || content == null || content.length == 0) {
        sweetInfo({text:'内容不能为空!',type:'info'});
        return;
    }
    //post request for save post
    if (login_user_id > 0) {
        var token = $('#token').val();
        postRequest("/post_publish", { "type": "publish","token":token, "title": title, "content": content,"community_id": community_id});
    } else {
        sweetInfo({text:'登录后才能发帖哦!',type:'info'});
    }
})

function postRequest(URL, PARAMS) {
    var temp = document.createElement("form");
    temp.action = URL;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in PARAMS) {
        var opt = document.createElement("textarea");
        opt.name = x;
        opt.value = PARAMS[x];
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}

function load_commend_community() {
    var data = {}
    data['community_id'] = community_id;
    data['type'] = 'commend_community';
    $.ajax({
        type: 'get',
        url: '/get_commend_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async: false,
        success: function(data) {
            commend_list = data.commend_list
            if (commend_list != null && commend_list.length>0){
                var commend_wrap = '';
                for (var i = 0; i < commend_list.length; i++) {
                    community = commend_list[i]
                    commend_wrap = commend_wrap + '<div class="community-block">\
                                           <div class="img"><a title="'+community.name+'岛" alt="'+community.name+'岛" href="community?id=' + community.id + '&type=query"><img src="' + community.head_img_url + '"></a></div>\
                                           <div class="content">\
                                               <h4><a href="community?id=' + community.id + '&type=query">' + community.name + '岛</a></h4>\
                                               <p>' + community.describe + '</p>\
                                           </div>\
                                           <div class="blk-1x"></div>\
                                           <div class="divider solid"></div>\
                                           <div class="block-bar">\
                                                <div class="span"><em>帖子</em><b>' + community.post_num + '</b></div>\
                                                <div class="span"><em>成员</em><b>' + community.user_num + '</b></div>\
                                           </div>\
                                       </div>';
                }
                $('.side-container').append(commend_wrap);
            }
        },
        error: function(xhr, type) {
            console.log('数据加载失败!')
        }
    })
}

// load post
function loadCommunityPost(page_no) {
    var data = {};
    data['type'] = 'getpost';
    data['community_id'] = community_id;
    data['page_no'] = page_no;
    data['num_perpage'] = num_page;
    $.ajax({
        type: 'get',
        url: '/get_community_post',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async: false,
        success: function(data) {
            post_list = data.post_list;
            if (post_list != null && post_list.length > 0){
                var post_wrap ='';
                for(var i=0;i<post_list.length;i++){
                    post=post_list[i];
                    user=post_list[i].user
                    var img_array=post_list[i].content.match(/<img[^>]+>/g);
                    var content = post_list[i].content.replace(/<[^>]+>/g,"");
                    if(content.length>100){
                        content = content.substring(0,100) + '...' ;
                    }
                    var imgs = ''
                    if(img_array!=null && img_array.length>0){
                        var count =0
                        for(var j=0;j<img_array.length && count<9;j++){
                            if(img_array[j].indexOf('images/img')<0){
                                imgs = imgs+'<li>'+img_array[j]+'</li>';
                                count++;
                            }
                        }
                        if(count>0){
                            imgs='<ul>'+imgs+'</ul>'
                        }

                    }
                    var approve_html='';
                    if(user.is_approve>0){
                        approve_html = '<span title="个人认证"  class="mark-i s v"><i class="icon-v"></i></span>';
                    }
                    post_wrap=post_wrap+ '<div class="item">\
                                            <div class="photo">\
                                                <a href="/user_info_post?type=1&user_id='+user.id+'">\
                                                    <img src="'+user.head_img_url+'"></a >\
                                            </div>\
                                            <div class="content">\
                                                <h4><a href="/post?id='+post.id+'&type=postInfo">'+post.title+'</a >\
                                                </h4>\
                                                <p>'+content+'</p >\
                                                '+imgs+'\
                                                <div class="block-bar">\
                                                    <span><a href="/user_info_post?type=1&user_id='+user.id+'">'+user.name+'</a ></span>\
                                                    '+approve_html+'\
                                                    <div class="control-right">\
                                                        <div class="row-1x">\
                                                            <div class="group-span-1x">\
                                                            <span><em>喜欢</em><b>'+post_list[i].like_num+'</b></span>\
                                                            <span><em>回复</em><b>'+post.floor_num+'</b></span>\
                                                            <span>'+post.create_time+'</span>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                </div>\
                                            </div>\
                                        </div>';
                }
                $('.post-list').html(post_wrap);
                total = data.total;
                page_no=page_no;
            }
        },
        error: function(xhr, type) {
            console.log('数据失败！')
        }
    })

}
// click left
$('#left').click(function() {
    var data = {};
    data['type'] = 'left';
    data['user_id'] = login_user_id;
    data['community_id'] = community_id;
    $.ajax({
        type: 'POST',
        url: '/user_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            $('.comm_user_num').text(data['user_num']);
            $('#left').addClass('hide');
            $('#join').removeClass('hide');
        },
        error: function(xhr, type) {
            console.log('操作失败!')
        }
    })

})
// click join
$('#join').click(function() {
    if (login_user_id > 0) {
        var data = {};
        data['type'] = 'join';
        data['user_id'] = login_user_id;
        data['community_id'] = community_id;
        $.ajax({
            type: 'POST',
            url: '/user_community',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                $('.comm_user_num').text(data['user_num']);
                $('#join').addClass('hide');
                $('#left').removeClass('hide');
            },
            error: function(xhr, type) {
                console.log('操作失败!')
            }
        })
    } else {
        sweetInfo({text:'登录后才能进岛哦!',type:'info'});
    }
})
 <!--模式框打开时,清理数据-->
$('#modal-community').on('hide.bs.modal', function () {
    $('input[name=community-name]').val($('h4.hname').find('span').text())
    $('textarea[name=community-desc]').val($('.content').find('p.pdesc').text())
})