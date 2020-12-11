

function shareClose(){
	$("#share-popup").css("display","none");
}
function shareFolderClose(){
  $("#sharefolder-popup").css("display","none");
  $(".imgcover").css("display","none");
}

$( "#sharefolder" ).click(function() {
  $("#sharefolder-popup").css("display","block");
  $("#sharefolderinput").focus();
  $(".imgcover").fadeTo(500, 0.5);

});

function shareClose(){
  $("#share-popup").css("display","none");
}



function shareStuffClose(){
  $("#sharestuff-popup").css("display","none");
  $(".cover").css("display","none");
}




$( "#subhshare" ).click(function() {
	$('#rename-popup').css('display','block');
    $('#popup-title').text('Share With');
    $(".cover").fadeTo(500, 0.5);
    $('#renameinput').focus();
            
	
	console.log('lastid',lastClickedEle);
	//check if quickaccess was select if so format id
	if(lastClickedEle[0] == 'q'){
		let id= [lastClickedEle.slice(0,1),'-', lastClickedEle.slice(1)].join('');
		$("#renameform").attr('action','/share/'+id + '/');
	}
	else{
		$("#renameform").attr('action','/share/'+lastClickedEle + '/');
	}

});

