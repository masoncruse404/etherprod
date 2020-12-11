var globalid;

$(document)
    .on('contextmenu', '.filetablerow', function(e) {
        //remove style from previous selected
        resetQA();
        resetFile();
        resetTableRow();
        document.getElementById("rmenutablefolder").className = "hide";

        e.preventDefault();
        var i = this.id
        globalid = i;
        var fileid  = i.substring(i.indexOf("-") + 1);
        var fid = '#filetablerow-' + fileid;
        $(fid).css('background', '#e8f0fe');
        //if file is selected do not view on right click
 
        var movetourl = "/moveto/" + i;
        document.getElementById("rmenutable").className = "show";
        document.getElementById("rmenutable").style.top = mouseY(event) + 'px';
        document.getElementById("rmenutable").style.left = mouseX(event) + 'px';


       if(isInViewport(document.getElementById("rmenutable"))){
        }else{
          var element = document.getElementById("rmenutable");
          var rect = element.getBoundingClientRect();
        if (rect.top < 0) {
        // Top is out of viewport
        }

        if (rect.left < 0) {
        // Left side is out of viewoprt
        }

        if (rect.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
        // Bottom is out of viewport    
          var topVal = parseInt(element.style.top, 10);
          element.style.top = (topVal - 350) + "px";
        }

        if (rect.right > (window.innerWidth || document.documentElement.clientWidth)) {
        // Right side is out of viewport
          var topVal = parseInt(element.style.left, 10);
          element.style.left = (topVal - 300) + "px";
        }
         
        }
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = '/startable/'+i;
        }

        document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            let atc = '/renametrashtable/'+i+'/'
            $("#renameform").attr('action',atc)
        }
    
       document.getElementById("sharecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Share With');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl =  "/share/"+ i + '/';
            $("#renameform").attr('action',renameurl)
             

        }


        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = '/download/'+i;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = '/downloadfolder/'+i;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = '/trashtable/'+i;
        }

        document.getElementById("removetrashlink").onclick = function(){
            document.getElementById("removetrashlink").href = '/removetrashtable/'+i;
        }
         

        document.getElementById("moved").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetourl)


        }


        document.getElementById("makeacopy").onclick = function(){
            document.getElementById("makeacopy").href = '/copyfiletrashtable/'+i;
        }


      window.event.returnValue = false;
});


$(document)
    .on('contextmenu', '.qafilea', function(e) {
        //reset selected style
        resetFile();
        e.preventDefault();
        document.getElementById("rmenutablefolder").className = "hide";
        var i = this.id
        globalid = i;
        var qaid = '#qfooter' + i;
        var qafooterid = '#qaname' + i;
        resetQA();
        $(qaid).css('background', '#e8f0fe');
        $(qafooterid).css('color', '#1967d2');
        
        var trashid = i.substring(0, 1) + "-" + i.substring(1);
        var url = "/star/";
        var full = url + trashid;
        var turl = "/trash/";
        let qid = i.substring(1);

        var renameurl = "/rename/g-" + qid;
        var tfull = turl + trashid;
      
      document.getElementById("rmenutable").className = "show";

      document.getElementById("rmenutable").style.top = mouseY(event) + 'px';
      document.getElementById("rmenutable").style.left = mouseX(event) + 'px';

       if(isInViewport(document.getElementById("rmenutable"))){
        }else{
          var element = document.getElementById("rmenutable");
          var rect = element.getBoundingClientRect();
        if (rect.top < 0) {
        // Top is out of viewport
        }

        if (rect.left < 0) {
        // Left side is out of viewoprt
        }

        if (rect.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
        // Bottom is out of viewport    
          var topVal = parseInt(element.style.top, 10);
          element.style.top = (topVal - 150) + "px";
        }

        if (rect.right > (window.innerWidth || document.documentElement.clientWidth)) {
        // Right side is out of viewport
          var topVal = parseInt(element.style.left, 10);
          element.style.left = (topVal - 300) + "px";
        }
         
         
        }
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = '/startable/'+trashid;
        }
     

        document.getElementById("movetoplace").onclick = function(){

            $("#movetopopupwrap").css("display","flex");

            var act = '/moveto/q-'+qid;
            $("#movetoform").attr('action',act)
        }



         document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Rename');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            $("#renameform").attr('action','/renametrashtable/'+trashid+'/')
        }
    
        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = '/download/'+trashid;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = '/downloadfolder/'+trashid;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = '/trashtable/'+trashid;
        }

           document.getElementById("makeacopy").onclick = function(){
            document.getElementById("makeacopy").href = '/copyfiletable/q-'+qid;
        }


      window.event.returnValue = false;
});




// this is from another SO post...
$(document).bind("click", function(event) {
  //alert('here');

  document.getElementById("rmenutable").className = "hide";
  document.getElementById("rmenutablefolder").className = "hide";
});



function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

$(document).bind("click", function(event) {
  document.getElementById("rmenutable").className = "hide";
  document.getElementById("rmenutablefolder").className = "hide";
});



function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

function isInViewport(element){
var myElement = element
var bounding = myElement.getBoundingClientRect();

if (bounding.top >= 0 && bounding.left >= 0 && bounding.right <= window.innerWidth && bounding.bottom <= window.innerHeight) {

    return 1
} else {

    return 0
}
}


$(document)
    .on('contextmenu', '.foldercontainer', function(e) {
        e.preventDefault();
        var i = this.id
        globalid = i;
        document.getElementById("rmenutable").className = "hide";
    
        var movetofolderurl = "/movefolderto/" + i;

   
      document.getElementById("rmenutablefolder").style.top = mouseY(event) + 'px';
      document.getElementById("rmenutablefolder").style.left = mouseX(event) + 'px';
        document.getElementById("rmenutablefolder").className = "show";
        if(isInViewport(document.getElementById("rmenutablefolder"))){
        }else{
          var element = document.getElementById("rmenutablefolder");
          var rect = element.getBoundingClientRect();
        if (rect.top < 0) {
        // Top is out of viewport
        }

        if (rect.left < 0) {
        // Left side is out of viewoprt
        }

        if (rect.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
        // Bottom is out of viewport    
          var topVal = parseInt(element.style.top, 10);
          element.style.top = (topVal - 150) + "px";
        }

        if (rect.right > (window.innerWidth || document.documentElement.clientWidth)) {
        // Right side is out of viewport
          var topVal = parseInt(element.style.top, 10);
          element.style.left = (topVal + 150) + "px";
        }
         
        }
        document.getElementById("starredfolder").onclick = function(){
            document.getElementById("addtostarfolder").href = '/startablefolder/'+i;
        }


        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = '/downloadfolder/'+i;
        }

        document.getElementById("trashfolder").onclick = function(){
            document.getElementById("addtotrashfolder").href = '/trashtablefolder/'+i;
        }

        document.getElementById("removetrashfolder").onclick = function(){
            document.getElementById("removetrashfolderlink").href = '/removetrashfoldertable/'+i;
        }
         
         
        document.getElementById("copyfolder").onclick = function(){
            document.getElementById("copyfolder").href = '/copytrashfoldertable/'+i;
        }


        document.getElementById("renametablefoldercontext").onclick = function(){
            let atc = '/renamefoldertabletrash/'+i+'/';
            $('#renamefolder-popup').css('display','block');
            $('#popup-title').text('Rename');
            $(".cover").fadeTo(500, 0.5);
            $('#renamefolderinput').focus();
            $("#renamefolderform").attr('action',atc)
        }


        document.getElementById("sharecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Share With');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl =  "/sharefolder/"+ i + '/';
            $("#renameform").attr('action',renameurl)
        }
    



        document.getElementById("movetofolder").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetofolderurl)


        }

      window.event.returnValue = false;
});


// this is from another SO post...
$(document).bind("click", function(event) {
  document.getElementById("rmenutable").className = "hide";
  document.getElementById("rmenutablefolder").className = "hide";
});



function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

