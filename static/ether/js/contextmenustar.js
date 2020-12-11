var globalid;
$(document)
    .on('contextmenu', '.file-content', function(e) {
        //remove style from previous selected
        resetQA();
        resetFile();
        e.preventDefault();
        var i = this.id
        globalid = i;
        if(document.getElementById("rmenufolder")){
            document.getElementById("rmenufolder").className = "hide";
        }
        var fileid  = i.substring(i.indexOf("-") + 1);
        var fid = '#file-infof' + fileid;
        var filefooterid = '#filefooter' + fileid;
        resetFile();
        $(fid).css('background', '#e8f0fe');
        $(filefooterid).css('color', '#1967d2');
        //if file is selected do not view on right click
        
      
        var renameurl = "/renamestar/";
    
        renameurl = renameurl + i;
       
        var movetourl = "/moveto/" + i;
        document.getElementById("rmenu").className = "show";
        document.getElementById("rmenu").style.top = mouseY(event) + 'px';
        document.getElementById("rmenu").style.left = mouseX(event) + 'px';



       if(isInViewport(document.getElementById("rmenu"))){
        }else{
          var element = document.getElementById("rmenu");
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
          element.style.top = (topVal - 300) + "px";
        }

        if (rect.right > (window.innerWidth || document.documentElement.clientWidth)) {
        // Right side is out of viewport
          var topVal = parseInt(element.style.left, 10);
          element.style.left = (topVal - 300) + "px";
        }
         
        }
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = '/removestar/'+i;
        }

        document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Rename');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            $("#renameform").attr('action',renameurl)
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
            document.getElementById("download").href = "/download/" + i;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = "/downloadfolder/" + i;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = '/trash/'+i;
        }


        document.getElementById("moved").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetourl)


        }


        document.getElementById("makeacopy").onclick = function(){
            document.getElementById("makeacopy").href = '/copystarfile/'+i;
        }


      window.event.returnValue = false;
});
$(document)
    .on('contextmenu', '.filetablerow', function(e) {
        //remove style from previous selected
        resetQA();
        resetFile();
        resetTableRow();
        document.getElementById("rmenufolder").className = "hide";
        e.preventDefault();
        var i = this.id
        globalid = i;
        var fileid  = i.substring(i.indexOf("-") + 1);
        var fid = '#filetablerow-' + fileid;
        $(fid).css('background', '#e8f0fe');
        //if file is selected do not view on right click
        
       
        var renameurl = "/rename/";
        renameurl = renameurl + i;
     
        var movetourl = "/moveto/" + i;
        document.getElementById("rmenu").className = "show";
        document.getElementById("rmenu").style.top = mouseY(event) + 'px';
        document.getElementById("rmenu").style.left = mouseX(event) + 'px';


       if(isInViewport(document.getElementById("rmenu"))){
        }else{
          var element = document.getElementById("rmenu");
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
            document.getElementById("addtostar").href = '/removestar/'+i;
        }

        document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            $("#renameform").attr('action',renameurl)
        }
    
        document.getElementById("sharecontext").onclick = function(){
             document.getElementById("shareform").action = "/share/"+ i + '/';

        }


        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = "/download/" + i;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = "/downloadfolder/" + i;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = '/trash/'+i;
        }

         

        document.getElementById("moved").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetourl)


        }


        document.getElementById("makeacopy").onclick = function(){
            document.getElementById("makeacopy").href = '/copystarfile/'+i;
        }


      window.event.returnValue = false;
});


$(document)
    .on('contextmenu', '.qafilea', function(e) {
        //reset selected style
        resetFile();
        e.preventDefault();
        document.getElementById("rmenufolder").className = "hide";
        var i = this.id
        globalid = i;
        var qaid = '#qfooter' + i;
        var qafooterid = '#qaname' + i;
        resetQA();
        $(qaid).css('background', '#e8f0fe');
        $(qafooterid).css('color', '#1967d2');
        let b = "-";
        let position = 1;
        var trashid = i.substring(0, position) + b + i.substring(position);
        let qid = i.substring(1);

        var renameurl = "/rename/g-" + qid;
        var tfull = turl + trashid;
        var durl = "/download/" + trashid;
      document.getElementById("rmenu").className = "show";

      document.getElementById("rmenu").style.top = mouseY(event) + 'px';
      document.getElementById("rmenu").style.left = mouseX(event) + 'px';

       if(isInViewport(document.getElementById("rmenu"))){
        }else{
          var element = document.getElementById("rmenu");
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
            document.getElementById("addtostar").href = '/removestar/g-'+gid;
            
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
            $("#renameform").attr('action',renameurl);
        }


            document.getElementById("sharecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Share With');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl =  "/share/q-"+ qid + '/';
            $("#renameform").attr('action',renameurl)

        }
    
        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = "/download/" + trashid;;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = "/downloadfolder/" + trashid;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = '/trashfolder/'+trash;
        }

           document.getElementById("makeacopy").onclick = function(){
            let tid = id.substr(1);
            document.getElementById("makeacopy").href = '/copystarfile/g-'+gid;
        }


      window.event.returnValue = false;
});




// this is from another SO post...
$(document).bind("click", function(event) {

  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
  document.getElementById("rmenuqa").className = "hide";
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
  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
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



function test(){
  alert(isInViewport(document.getElementById("elem"))?"Yes":"No"); 
}

$(document)
    .on('contextmenu', '.foldercontainer', function(e) {
        e.preventDefault();
        var i = this.id
        globalid = i;
        document.getElementById("rmenu").className = "hide";
   
        var renameurl = "/renamefolder/" + i;
        var movetofolderurl = "/movefolderto/" + i;
   
        document.getElementById("rmenufolder").style.top = mouseY(event) + 'px';
        document.getElementById("rmenufolder").style.left = mouseX(event) + 'px';
        document.getElementById("rmenufolder").className = "show";
        if(isInViewport(document.getElementById("rmenufolder"))){
        }else{
          var element = document.getElementById("rmenufolder");
          var rect = element.getBoundingClientRect();
          console.log(rect.top, rect.right, rect.bottom, rect.left);
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
            document.getElementById("removestarfolder").href = '/removefolderstar/'+i;
        }


       document.getElementById("sharefolder").onclick = function(){
            $('#rename-popup').css('display','block');
            $('#popup-title').text('Share With');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl =  "/sharefolder/"+ i + '/';
            $("#renameform").attr('action',renameurl)

          }
     document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = "/downloadfolder/" + i;
        }
        document.getElementById("trashfolder").onclick = function(){
            document.getElementById("addtotrashfolder").href = "/trashfolder/" + i;
        }
         
        document.getElementById("copyfolder").onclick = function(){
            document.getElementById("copyfolder").href = '/copystarfolder/'+i;
        }

        document.getElementById("renamefolderstar").onclick = function(){
            $('#renamefolder-popup').css('display','block');
            $('#popup-title').text('Rename');;
            $(".cover").fadeTo(500, 0.5);
            $('#renamefolderinput').focus();
            renameurl = renameurl + '/'
            $("#renamefolderform").attr('action','/renamefolderstar/'+i+'/')
        }


        document.getElementById("movetofolder").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetofolderurl)


        }

      window.event.returnValue = false;
});


// this is from another SO post...
$(document).bind("click", function(event) {
  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
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

