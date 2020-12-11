var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

//if the broswer is chrome move labels to correct since it was developed on firefox
if(isChrome){


}else{

	$("#id_new_password1").css("margin-bottom","20px");
}