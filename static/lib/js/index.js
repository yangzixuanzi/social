//初始化页面
var page_no = 1;
var num_perpage = 20;
var total = 0;
var has_next = false;
var callbackPage = function(page_no){
   loadHotPost(page_no)
}
function initData(){
    callbackPage(1)
    loadHotCommunity();
}
initData();
//加载热帖
function loadHotPost(page_no){
    var data = {};
    data['type'] = 'hot';
    data['page_no'] = page_no;
    data['num_perpage'] = num_perpage;
    $.ajax({
        type: 'GET',
        url: '/get_hot_post',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            var post_list = data.post_list;
            total = data.total;
            has_next = data.has_next
            if(post_list.length>0){
                var hot_post_wrap ='';
                for(var i =0 ; i<post_list.length;i++){
                    var user = post_list[i].user;
                    var community = post_list[i].community;
                    var img_array=post_list[i].content.match(/<img[^>]+>/g);
                    var content = post_list[i].content.replace(/<[^>]+>/g,"");
                    if(content.length>100){
                        content = content.substring(0,100) + '...' ;
                    }
                    var imgs = ''
                    var like_num = '';
                    var approve_html = ''
                    if(img_array!=null && img_array.length>0){
                        imgs='<ul>';
                        var count =0
                        for(var j=0;j<img_array.length && count<9;j++){
                            if(img_array[j].indexOf('images/img')<0){
                                imgs = imgs+'<li>'+img_array[j]+'</li>';
                                count++;
                            }
                        }
                        imgs=imgs+'</ul>'
                    }
                    if(user.is_approve>0){
                        approve_html = '<span title="个人认证"  class="mark-i s v"><i class="icon-v"></i></span>';
                    }
                    like_num = '<span><em>喜欢</em><b>'+post_list[i].like_num+'</b></span>'
                    hot_post_wrap+='<div class="item">\
                            <div class="photo">\
                                <a href="/user_info_post?type=1&user_id='+user.id+'"><img src="'+user.head_img_url+'"></a>\
                            </div>\
                            <div class="content">\
                                <div class="block-bar">\
                                        <span><a href="/user_info_post?type=1&user_id='+user.id+'">'+user.name+'</a ></span>\
                                        '+approve_html+'\
                                        <span>'+post_list[i].create_time+'</span>\
                                </div>\
                                <h4><a href="post?id='+post_list[i].id+'&type=postInfo">'+post_list[i].title+'</a></h4>\
                                <p>'+content+'</p>\
                                '+imgs+'\
                                <div class="block-bar">\
                                    '+like_num+'\
                                     <span><em>回复</em><b>'+post_list[i].floor_num+'</b></span>\
                                     <div class="control-right">\
                                        <div class="row-1x">\
                                            <div class="group-span-1x">\
                                            <span>来自：<a href="/community?id='+community.id+'&type=query">'+community.name+'岛</a></span>\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>';

                }
                $('.post-list').append(hot_post_wrap);
                if(!data.has_next){
                    $('.info').html('没有更多了')
                }
                //$("#page").initPage(num_perpage,total,page_no,callbackPage);
            }
        },
        error: function(xhr, type) {
            console.log('加载失败!')
        }
    })
}
//加载热门社区
function loadHotCommunity(){
    var data = {}
    data['type'] = 'commend_community';
    $.ajax({
        type: 'get',
        url: '/get_hot_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async:false,
        success: function(data) {
            commend_list = data.commend_list;
            var commend_wrap ='';
            for(var i=0;i<commend_list.length;i++){
                community = commend_list[i]
                commend_wrap =commend_wrap+'<div class="community-block">\
                                       <div class="img"><a href="community?id='+community.id+'&type=query"><img title="'+community.name+'岛" alt="'+community.name+'岛" src="'+community.head_img_url+'"></a></div>\
                                       <div class="content">\
                                           <h4><a href="community?id='+community.id+'&type=query">'+community.name+'岛</a></h4>\
                                           <p>'+community.describe+'</p>\
                                       </div>\
                                       <div class="blk-1x"></div>\
                                       <div class="divider solid"></div>\
                                       <div class="block-bar">\
                                            <div class="span"><em>帖子</em><b>'+community.post_num+'</b></div>\
                                            <div class="span"><em>成员</em><b>'+community.user_num+'</b></div>\
                                       </div>\
                                   </div>';

            }
            $('.side-container').append(commend_wrap);
        },
        error: function(xhr, type) {
            console.log('加载失败!')
        }
    })
}
$(document).endlessScroll({
    bottomPixels: 450,
    fireDelay: 10,
    callback: function(p){
        if(has_next){
            page_no++;
            loadHotPost(page_no)
        }else{
            console.log('到底了')
        }
    }
});

