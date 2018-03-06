//认证图片上传
$(function(){
	var delParent;
	var delElmentIndex;
	var defaults = {
		fileType         : ["jpg","png","bmp","jpeg","JPEG","JPG"],   // 上传文件的类型
		fileSize         : 1024 * 1024 * 10                  // 上传文件的大小 10M
	};
		/*点击图片的文本框*/
	$(".file").change(function(){
		var idFile = $(this).attr("id");
		var imgName = $(this).attr("name");
		var file = document.getElementById(idFile);
		var imgContainer = $(this).parents(".z_photo"); //存放图片的父亲元素
		var fileList = file.files; //获取的图片文件
		console.log(fileList+"======filelist=====");
		var input = $(this).parent();//文本框的父亲元素
		var imgArr = [];
		//遍历得到的图片文件
		var numUp = imgContainer.find(".up-section").length;
 		var totalNum = numUp + fileList.length;  //总的数量
		if(fileList.length >1){
			alert("一次只能上传一张图片");  //一次选择上传超过5个 或者是已经上传和这次上传的到的总数也不可以超过5个
		}
		 else if(numUp < 5){
			fileList = validateUp(fileList);
			for(var i = 0;i<fileList.length;i++){
			 var imgUrl = window.URL.createObjectURL(fileList[i]);
			     imgArr.push(imgUrl);
			var num =$(".z_file input").index(this);
			$('.z_file').eq(num).hide();
			 var $section = $("<section class='up-section loading'>");
			    // imgContainer.prepend($section);
			     $(".z_file").eq(num).after($section)
			     console.log(num);
			 var $span = $("<span class='up-span'>");
			     $span.appendTo($section);
			
		     var $img0 = $("<img class='close-upimg'>").on("click",function(event){
				    event.preventDefault();
					event.stopPropagation();
					$(".works-mask").show();
					delParent = $(this).parent();
				});   
				$img0.attr("src","images/a7.png").appendTo($section);
		     var $img = $("<img class='up-img up-opcity'>");
		         $img.attr("src",imgArr[i]);
		         $img.attr("name",imgName);
		         $img.appendTo($section);
		     var $p = $("<p class='img-name-p'>");
		         $p.html(fileList[i].name).appendTo($section);
			
		     var $input = $("<input id='taglocation' name='taglocation' value='"+idFile+"' type='hidden'>");
		         $input.appendTo($section);
		     var $input2 = $("<input id='tags' name='tags' value='' type='hidden'/>");
		         $input2.appendTo($section);
		      
		   }
	}
		setTimeout(function(){
             $(".up-section").removeClass("loading");
		 	 $(".up-img").removeClass("up-opcity");
		 },450);
		 numUp = imgContainer.find(".up-section").length;
		if(numUp >= 5){
			$(this).parent().hide();
		}
		//input内容清空
		$(this).val("");
	});
	
	
   
    $(".z_photo").delegate(".close-upimg","click",function(){
     	  $(".works-mask").show();
     	  delParent = $(this).parent();
	});
		
	$(".wsdel-ok").click(function(){
		$(".works-mask").hide();
		var numUp = delParent.siblings().length;
		console.log('numUp'+numUp)
		if(numUp < 6){
			var $input = delParent.find('input[name="taglocation"]')
			var charat = $input.val().length;
			var index = $input.val().charAt(charat-1)
			delParent.parent().find(".z_file").eq(index-1).show();
		}
		 delParent.remove();
	});
	
	$(".wsdel-no").click(function(){
		$(".works-mask").hide();
	});
		
		function validateUp(files){
			var arrFiles = [];//替换的文件数组
			for(var i = 0, file; file = files[i]; i++){
				//获取文件上传的后缀名
				var newStr = file.name.split("").reverse().join("");
				if(newStr.split(".")[0] != null){
						var type = newStr.split(".")[0].split("").reverse().join("");
						console.log(type+"===type===");
						if(jQuery.inArray(type, defaults.fileType) > -1){
							// 类型符合，可以上传
							if (file.size >= defaults.fileSize) {
								alert(file.size);
								alert('您上传的图片"'+ file.name +'"文件大小过大');
							} else {
								// 在这里需要判断当前所有文件中
								arrFiles.push(file);	
							}
						}else{
							alert('您上传的图片"'+file.name +'"类型不符合,请重新选择图片');
						}
					}else{
						alert('您上传的图片"'+ file.name +'"没有类型, 无法识别,请重新选择图片');
					}
			}
			return arrFiles;
		}
		

	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
})
