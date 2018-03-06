/*注册 -- start*/
var sms_code_flag = false;
var check_password_flag = false;
var check_exist = false;
var check_mobile = false; //号码格式

//验证码
function sendCodeReg() {
    check_mobile_register();
    if (!check_exist && check_mobile) {
        $('#user_mobile_verify_code_input').val('')
        doPostBack(); //发送短信接口
        invokeSettime(); //开启倒计时
        sms_code_flag = true;
    }
}
//验证手机号码是否注册
function check_mobile_register() {
    if(isPhoneNum()){
        var mobile = document.getElementById('user_mobile_phone_input').value;
        data = {};
        data['mobile'] = mobile;
        data['type'] = 'check_exist';
        $.ajax({
            type: 'POST',
            url: '/check_mobile_exist',
            data: data,
            dataType: 'json',
            success: function(data) {
                if (data['code'] == 1) {
                    check_exist = true
                    document.getElementById('msg').innerHTML = "手机号码已注册!";
                } else {
                    check_exist = false
                    document.getElementById('msg').value = "";
                }
            },
            error: function(xhr, type) {
                console.log('手机号码输入不正确!')
            }
        });
    }
    return false;
}
 //注册请求
function regist() {
     var mobile = document.getElementById("user_mobile_phone_input").value;
     var sms_code = document.getElementById("user_mobile_verify_code_input").value;
     var password = document.getElementById("user_password_input").value;
     var password_repeat = document.getElementById("user_password_input_repeat").value;
     check_mobile_register();
     if (!check_mobile || check_exist) {
         return false;
     }
     if (sms_code == "") {
         document.getElementById('msg').innerHTML="请输入短信验证码";
         return false;
     }
     if(!sms_code_flag){
        document.getElementById('msg').innerHTML="验证码不正确!";
         return false;
     }
     check_password_and_repeat();
     if(!check_password_flag){
        return false;
     }
     var data={};
     data['type']='create';
     data['mobile']=mobile;
     data['sms_code']=sms_code;
     data['password']=password;
     data['password_repeat']=password_repeat;
     $.ajax({
         type:'POST',
         url:'/regist',
         data:data,
         dataType:'json',
         success:function(data) {
            var code = data['code']
            var msg =''
            switch(code){
                case 0:
                    window.location.href="/index";
                    break;
                case 1:
                    msg ='请输入正确的手机号码!';
                    document.getElementById('msg').innerHTML=msg;
                    break;
                case 2:
                    msg ='手机号已注册!';
                    document.getElementById('msg').innerHTML=msg;
                    break;
                case 3:
                case 4:
                case 5:
                    msg ='验证码不正确!';
                    document.getElementById('msg').innerHTML=msg;
                    break;
                default:
                    console.log('注册失败!')
            }

         },
         error:function(xhr,type) {
             console.log('注册出错了')
         }
     });
     return false;
 }

/*找回密码 -- start*/

//校验手机号是否合法
function isPhoneNum() {
    var phonenum = $("#user_mobile_phone_input").val();
    var myreg = /^1(3|4|5|7|8)\d{9}$/;
    if (!myreg.test(phonenum)) {
        document.getElementById('msg').innerHTML = "请输入正确的手机号码!";
        check_mobile = false;
        return false;
    } else {
        check_mobile = true;
        return true;
    }
}

//验证手机号是否存在
function check_mobile_exist() {
    if(isPhoneNum()){
        var mobile = document.getElementById('user_mobile_phone_input').value;
        data = {};
        data['mobile'] = mobile;
        data['type'] = 'check_exist';
        $.ajax({
            type: 'POST',
            url: '/check_mobile_exist',
            data: data,
            dataType: 'json',
            success: function(data) {
                if (data['code'] == 0) {
                    document.getElementById('msg').innerHTML = "手机号码尚未注册!";
                    check_exist = false
                } else {
                    check_exist = true
                    document.getElementById('msg').value = "";
                }
            },
            error: function(xhr, type) {
                console.log('手机号码输入不正确!')
            }
        });
    }
    return false;
}
//修改密码
function modify_password() {
    var mobile = document.getElementById("user_mobile_phone_input").value;
    var sms_code = document.getElementById("user_mobile_verify_code_input").value;
    var password = document.getElementById("user_password_input").value;
    var password_repeat = document.getElementById("user_password_input_repeat").value;
    if (mobile == "") {
        document.getElementById('msg').innerHTML = "请输入手机号!";
        return false;
    }
    check_mobile_exist();

    if(!check_mobile || !check_exist){
        return false;
    }
    if (sms_code == "") {
        document.getElementById('msg').innerHTML = "请输入手机验证码!";
        return false;
    }
    if (!sms_code_flag) {
        document.getElementById('msg').innerHTML = "验证码不正确!";
        return false;
    }
    if (password == "") {
        document.getElementById('msg').innerHTML = "请输入新密码";
        return false;
    }
    if (password_repeat == "") {
        document.getElementById('msg').innerHTML = "请重复输入新密码!";
        return false;
    }
    check_password_and_repeat();
    if (!check_password_flag) {
        return false;
    }
    var data = {};
    data['type'] = 'modify_password';
    data['mobile'] = mobile;
    data['sms_code'] = sms_code;
    data['password'] = password;
    data['password_repeat'] = password_repeat;
    $.ajax({
        type: 'POST',
        url: '/modify_user',
        data: data,
        dataType: 'json',
        success: function(data) {
            if (data['code'] == 1) {
                document.getElementById('msg').innerHTML = "用户不存在";
            } else if (data['code'] > 1) {
                document.getElementById('msg').innerHTML = "验证码不正确";
            } else if (data['code'] == 0) {
                window.location.href = "/index";
            }
        },
        error: function(xhr, type) {
            console.log('手机号或者验证码不正确!');
        }
    });
    return false;
}

//登录
$('#login-btn').click(function(){
            var name = $('#name').val();
            var password=$('#password').val();
            var data={};
            data['name']=name;
            data['password']=password;
            $.ajax({
                type:'POST',
                url:'/login',
                data:data,
                dataType:'json',
                timeout:5000,
                 success:function(data){
                    if(data.code==0){
                        if(data.next_url==''){
                            data.next_url='/index';
                        }
                        window.location=data.next_url
                    }else{
                        document.getElementById('msg').innerHTML = '用户名或密码错误!';
                    }
                },
                error:function(){
                    document.getElementById('msg').innerHTML = '登录失败!';
                }
            })
})

/* common */

//输入,清空提示
function onInput() {
    document.getElementById('msg').innerHTML = "";
}

//验证码
function sendCodeFindPass() {
    check_mobile_exist();
    if (check_exist && check_mobile) {
        $('#user_mobile_verify_code_input').val('')
        doPostBack(); //发送短信接口
        invokeSettime(); //开启倒计时
        sms_code_flag = true;
    }
}

//检查密码
function check_password_and_repeat() {
    var password = document.getElementById('user_password_input').value;
    var password_repeat = document.getElementById('user_password_input_repeat').value;
    if (password_repeat == '') {
        document.getElementById('msg').innerHTML = "请输入密码";
        check_password_flag = false;
    } else if (password.length < 6) {
        document.getElementById('msg').innerHTML = "密码长度不少于6位"
        check_password_flag = false;
    } else if (password_repeat != password) {
        document.getElementById('msg').innerHTML = "两次输入密码不一致";
        document.getElementById('user_password_input').value = "";
        document.getElementById('user_password_input_repeat').value = "";
        check_password_flag = false;
    } else {
        document.getElementById('msg').innerHTML = "";
        check_password_flag = true;
    }
    return false;
}

//触发倒计时
function invokeSettime() {
    var countdown = 60;
    var obj = $('#button_send_sms_code');
    settime(obj);
    function settime(obj) {
        if (countdown == 0) {
            obj.attr("disabled", false);
            obj.html("获取验证码");
            countdown = 60;
            return;
        } else {
            obj.attr("disabled", true);
            obj.html( + countdown + "s后可重新获取");
            countdown--;
        }
        setTimeout(function() {
            settime(obj)
        },
        1000)
    }
}
function doPostBack(url, backFunc, queryParam) {
    var mobile = $("#user_mobile_phone_input").val();
    var data = {};
    data['mobile'] = mobile;
    $.ajax({
        async: false,
        cache: false,
        type: 'post',
        url: '/send_sms_code',
        // 请求的action路径
        data: data,
        error: function() { // 请求失败处理函数
            console.log('发送手机验证码出错!')
        },
        success: function(data) {
            if (data.code == 0) {
                console.log('验证码发送成功!')
            } else {
                console.log('验证码发送失败!')
            }
        }
    });
}
