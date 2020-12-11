var isUploadInProgress = 0;
var uploadcount = 0;
var totaluploads = 0;
var folderuploadsinprogress = 0;
var uploadfinished = 0;
var uploadscanceled = 0;
var uploadsize = 0;
var fdata = new FormData();
var datalist = [];
var xhrcancel = new Set()
var xhr;
    

$("#uploadstop").click(function(e){
    if(xhrfolder){
      xhrfolder.abort();
      $("#fu").css("display","none");
      return;
    }
    xhr.abort();
    for(let i=uploadfinished+1; i<uploadcount; i++){
        xhrcancel.add(i);
        
    }
    datalist = [];
    uploadcount = 0;
    fdata = new FormData();
    return;
   
});


function initupload(){
         isUploadInProgress = 1;
         fdata.append("csrfmiddlewaretoken", $(this).attr("data-csrf-token"));
         console.log('data ',fdata.getAll('file'));
         $("#mbody").css('display','block');
         $("#fu").css("display","block");
         $(".fuheader").css('display','flex');
         $(".foldera").show();
         $(".fuprogresswrapper").css('display','flex');
         $(".futitle").text('Uploading '+uploadcount+' items');
         
        var y = 0;
        console.log('folderuploadsinprogress ',folderuploadsinprogress);
        //check to see if folder has not finished uploading yet
        for (let ix=uploadfinished+folderuploadsinprogress, y=0; ix<uploadcount+uploadfinished, y<uploadcount; ix++, y++){
            console.log('itemz ',fdata.getAll('file')[ix]);
            
            addupload(fdata.getAll('file')[y],ix);
        }

         startHover();
        
         ajaxupload(fdata.getAll('file')[0],0);  
}


function cancelupload(thisid){
     console.log('cancel upload ',thisid);
     console.log('cancel upload finished ',uploadfinished);
     $("#"+thisid).css("display","none");

     //check if canceled upload is a folder

     if(uploadfinished+uploadscanceled == thisid){
        //cancel current upload
        console.log('cancel current');
        if($("#"+thisid).hasClass("folder")){
          console.log('has class folder');
          xhrfolder.abort();
        }else{
          console.log('does not have class folder');
          xhr.abort();
        }
        uploadscanceled++;
        $("#"+thisid).css("display","none");
        console.log('dl ',datalist[thisid]);

        //check if the cancel upload is the only one left
        if(thisid+1 == uploadcount){
            console.log('only upload left');
              datalist = [];
              uploadcount = 0;
              fdata = new FormData();
              //$("#fu").css("display","none");
              return;
        }
        //start next upload
        ajaxuploadcallback(thisid++)
     }else{
        //add id to the cancel set to be canceled in the future before uploading
        console.log('added ',thisid);
        xhrcancel.add(thisid);
     }
}


function startHover(){
$(document).on("mouseenter", ".fufilewrapper", function() {
   let thisid = $(this).attr("id");
   if( $("#"+thisid).hasClass("udone") ){
     $(this).children('.fufolder').css('display','flex');
     $(this).children('.fucheck').css('display','none');
     console.log('im done');
   }else{
     $('#chartwrapper'+thisid).css('display','none');
     $(this).children('.fuclose').css('display','flex');
   }
   console.log('thisid ',thisid);
       

});

$(document).on("mouseleave", ".fufilewrapper", function() {
     let thisid = $(this).attr("id");
     if( $("#"+thisid).hasClass("udone") ){
     $(this).children('.fucheck').css('display','flex');
     $(this).children('.fufolder').css('display','none');
   }else{
     $(this).children('.fuclose').css('display','none');
     $(this).children('.chartwrapper').css('display','flex');
   }
   
      
});
}

    //is called after a file has finished uploading
    function ajaxuploadcallback(counter){
        console.log('in ajaxuploadcallback');
        console.log('upload counter ',uploadcount);
        if(counter < uploadcount-1){
            counter++;
            console.log('conter=',counter);
            let startTime = new Date(Date.now());
            console.log('start time',startTime.getTime());
            ajaxupload(fdata.getAll('file')[counter], counter);
        }
    }

 
    //adds uploaded file to upload UI
    function addupload(file, pcounter){
        console.log('in addUpload');
        var $fufilewrapper = $("<div id='"+pcounter+"' class='fufilewrapper'><i id='futype' class='far fa-image fa-lg'></i><span id='funame'>"+file.name+"</span><div id='chartwrapper"+pcounter+"' class='chartwrapper'><div id=progresscircle"+pcounter+" class='radialProgressBar progress-0'><div id=progresstext"+pcounter+" class='overlay'></div></div></div><div id='fucheck"+pcounter+"' class='fucheck' display='none' ><i class='fas fa-check'></i></div><div class='fufolder'><i class='far fa-folder fa-lg'></i></div><div id='fuclose"+pcounter+"'class='fuclose' onclick='cancelupload("+pcounter+")'><i class='fas fa-times'></i></div></div>");
        $("#mbody").prepend($fufilewrapper);
        //$("#gallery tbody").prepend("<tr><td><a href='#'>" + file.name + "</a></td></tr>")
      }

    function adduploadgrid(fileurl,pcounter,filetype,fname){
      var footerid = "file-infof"+pcounter;
      if(filetype === 'png' || filetype === 'jpg' || filetype === 'jpeg'){
        var newfile = "<div class='list-item "+pcounter+"' id=f"+pcounter+" onclick='t(this.id)'>"
      +"<a href='#!' class='file'>"
      +"<div class='list-content file-content file-content' id='fcontent-"+pcounter+"' onclick='t(event,this.id)'>"
      +"<img id='img' class='img-"+pcounter+"' src='"+ fileurl +"'></img>"
      +"<div class='list-footer' id='"+footerid+"'>"
      +"<div class='list-icon-wrapper'>"
      +"<div class='file-icon-circle'>"
      +"<i id='file-icon' class='far fa-hdd file-icon'></i>"
      +"</div>"
      +"<div class='list-footer-name'>"
      +"<span>"
      +fname
      +"</span>"
      +"</div>"

      +"</div>"
      + "</div></a></div>";
      $(newfile).appendTo(".flexbox");
      }
      else{
    
         var newfile = 
        "<div class='list-item "+pcounter+"' id="+pcounter+" onclick='t(this.id)'>"
      +"<a href='#!' class='file'>"
      +"<div class='list-content file-content file-content' id='"+pcounter+"' onclick='t(event,this.id)'>"
      +"<img id='img' class='"+pcounter+"' src=''></img>"
      +"<div class='list-footer' id='"+footerid+"'>"
      +"<div class='list-icon-wrapper'>"
      +"<div class='file-icon-circle'>"
      +"<i id='file-icon' class='far fa-hdd file-icon'></i>"
      +"</div>"
      +"<div class='list-footer-name'>"
      +"<span>"
      +fname
      +"</span>"
      +"</div>"

      +"</div>"
      + "</div></a></div>";
       $(newfile).appendTo(".flexbox");
       var baseURL = "{% static 'images/question-icon.png' %}";
       var imgclass = '.' + pcounter;
       $(imgclass).attr('src', '/static/images/question-icon3.png');
        
      
    }
    }

    function finishupload(counter,fid){
        let mid = uploadscanceled + uploadfinished;
        console.log('uploads canceled ',mid);
        $("#"+mid).addClass('udone');
        let a = $("#"+mid);
        a.attr("onClick", "findfilepk(" + fid+ ")");
        $("#chartwrapper"+mid).css("display","none");
        $("#fucheck"+mid).css("display","flex");
        $("#fuclose"+mid).css("display","none");
        uploadfinished++;
        if(uploadfinished == 1){
            $(".futitle").text("1 upload complete");
        }else{
            $(".futitle").text(uploadfinished + " uploads complete");
        }
        if(uploadfinished == totaluploads){
            console.log('last one');
            isUploadInProgress = 0;
            $("#fupro").css("display","none");
        }
    }

    function ajaxupload(file, counter){
        console.log('in ajaxupload ', file);
         filename = '';
            if('name' in file)

              filename= file.name;

            else
              filename = file.fileName;
            if(filename.length > 60){
              uploadfiletype = filename.split('.').pop();
              filename = filename.slice(0,59);
              console.log('file ',file);
              filename = filename + '.' + uploadfiletype
            }
            let mid = uploadscanceled + uploadfinished;

            //check if file upload has been canceled
            if (xhrcancel.has(mid)){
                //upload next file in queue
                uploadscanceled++;
                console.log('xhrcancel ',xhrcancel);
                return ajaxuploadcallback(mid++);
            }
            var started_at = new Date();
            xhr = new XMLHttpRequest();
            (xhr.upload || xhr).addEventListener('progress', function(e) {
           
            if( e.lengthComputable )
            {
                // Append progress percentage.
                var loaded = e.loaded;
                var total = e.total;
                var progressValue = Math.round( ( loaded / total ) * 100 );

               

                // Time Remaining
                var seconds_elapsed =   ( new Date().getTime() - started_at.getTime() )/1000;
                var bytes_per_second =  seconds_elapsed ? loaded / seconds_elapsed : 0 ;
                var Kbytes_per_second = bytes_per_second / 1000 ;
                var remaining_bytes =   total - loaded;
                var seconds_remaining = seconds_elapsed ? remaining_bytes / bytes_per_second : 'calculating' ;
                console.log('seconds remaing ',seconds_remaining);
                $("#futimer").text(Math.round(seconds_remaining) + ' seconds remaining');
                 //$("#progresscircle"+counter+uploadfinished).addClass('progress-'+progressValue);

             
            }
                var done = e.position || e.loaded
                var total = e.totalSize || e.total;
                var prog = Math.round(done/total*100);
              
                console.log('done ',done);
            
                //console.log('xhr progress: ' + prog + '%');
                //console.log('counter=',counter);
                //$("#progresstext"+counter).text(prog);
                console.log('am i correct ',uploadfinished);
                console.log('the progress ',prog);
                $("#progresscircle"+mid).addClass('progress-'+prog);


            });
            xhr.addEventListener('load', function(e) {

            if(this.status == 406){
                $("#fu").css("display","none");
                $("#myalertupload").css("display","block");
                return;
            }
            data = JSON.parse(this.responseText);
            console.log('response ',data.file);
            console.log('the id ',data.id);
            adduploadgrid(data.file,data.id,data.filetype,data.name);
            if(this.status != 200){
                $('#driver-uploader-failure-alert').show();
                return;
            }
            finishupload(counter,data.id);
            ajaxuploadcallback(counter);
            });

            xhr.open('post', '/uploads/sub_upload_driver/', true);
            var fd = new FormData();
            fd.append("filename", filename);
            fd.append("drive_file", file);
           
            xhr.send(fd);
    }




    $(document).ready(function(){
        $('#upload_file').change(function(){
            //reset

            if(isUploadInProgress){
                $("#myalertupload").css('display','block');
                $("#alertmsg").text("Please wait until current upload has finished");
                return;
            }
            uploadcount = 0;
            datalist = [];
            fdata = new FormData();
            uploadscanceled = 0;
             $.each($("#upload_file")[0].files, function(i, file) {

                fdata.append("file", file);
                datalist.push(file);
                console.log('upload file111',   file)
                uploadsize += file.size;
                console.log('uploadsize ',uploadsize)
                uploadcount++;
                totaluploads++;
            });
            initupload();
            
        });
    });




//folder upload 


   var folderuploadcount = 0;
        var folderuploadfinished = 0;
        var folderuploadscanceled = 0;
        var xhrfoldercancel = new Set()
        var xhrfolder = 0;
        var folderuploadinprogress = 0;
        var lastuploadfinishedid = 0;

        $("#uploadstop").click(function(e){
            xhr.abort();
            $("#fu").css("display","none");
           
            datalist = [];
            uploadcount = 0;
            fdata = new FormData();
            return;
        });


        function displayfolder(id){
            window.location = '/subfolder/' + id;
        }

   



        function finishuploadfolder(fid, folderid){
            console.log('lastuploadfinishedid',lastuploadfinishedid)
        let a = $("#"+fid);
        a.attr("onClick", "displayfolder(" + folderid+ ")");
        $("#chartwrapper"+fid).css("display","none");
        $("#fuclose"+fid).css("display","none");
        $("#fucheck"+fid).css("display","flex");
       
        uploadfinished++;
        console.log('folderuploadfinished ',uploadfinished)
        if(uploadfinished == 1){
            $(".futitle").text("1 folder upload complete");
        }else{
            $(".futitle").text(uploadfinished + "  uploads complete");
        }

        if(uploadfinished == totaluploads){
            $("#fupro").css("display","none");
        }

        return 
    
    }

    function addfolder(fname, fid){
        var newfolder = $("<a href='/subfolder/"+fid+"'><div class='foldercontainer'><i id='folder' class='fas fa-folder fa-lg icon'></i><span>"+fname+"</span></div></a>");

        $(newfolder).appendTo(".folders-wrapper");
    }

      function adduploadfolder(fname,pcounter){
        console.log('in addUpload');
        var $fufilewrapper = $("<div id='"+pcounter+"' class='fufilewrapper folder'><i id='futype' class='far fa-folder fa-lg'></i><span id='funame'>"+fname+"</span><div id='chartwrapper"+pcounter+"' class='chartwrapper'><div id=progresscircle"+pcounter+" class='radialProgressBar progress-0'><div id=progresstext"+pcounter+" class='overlay'></div></div></div><div id='fucheck"+pcounter+"' class='fucheck' display='none' ><i class='fas fa-check'></i></div><div class='fufolder'><i class='far fa-folder fa-lg'></i></div><div id='fuclose"+pcounter+"'class='fuclose' onclick='cancelupload("+pcounter+")'><i class='fas fa-times'></i></div></div>");
            $("#mbody").prepend($fufilewrapper);
        return pcounter
      }


    function folderPopup(){
             $("#mbody").css('display','block');
             $("#fu").css("display","block");
             $(".fuheader").css('display','flex');
             $(".foldera").show();
             $(".fuprogresswrapper").css('display','flex');
    }
    var fQueue = [];
    var uploadinprocess = 0;
    $(function () {
        $("#filepicker").change(function () {

            if(isUploadInProgress){
                $("#myalertupload").css('display','block');
                $("#alertmsg").text("Please wait until current upload has finished");
                return;
            }
    
            // constructor form objects, mass participation form must pass node object constructor
            // $ ( "# formUploadDir") is taken to form an array of objects, and then take the form of data corresponding to the index by
            var formData = new FormData($("#folderuploadform")[0]);
            // get the value of the cookie csrf, jquery dependent on third-party libraries
            //var token = $.cookie("csrftoken");
            // judge upload directory is empty, is not empty files in a directory corresponding to the first file of the Road King
            // C: \ fakepath \ desktop.ini: For security browser does not expose the full file path to the client
            var otherfiles = document.querySelector("#filepicker").files;
            var files = $("#filepicker").val();
            console.log('uploaded files ',files)
            console.log('otherfiles ',otherfiles)
            for (var file of otherfiles) {
                let fpath = file.webkitRelativePath
                console.log('file ',file)
                console.log('fpath ',fpath)
                var uploadfoldername = fpath.split('/')[0]
                formData.append('fpath',fpath)
                formData.append('files',file)

            }
            if(files==""){
                alert("Please select the upload directory or the directory is empty.")
                return
            }
          
            var ajaxfolderupload = $.ajax({
                xhr: function(){
                       isUploadInProgress = 1;
                       folderPopup();
                       uploadcount++;
                       totaluploads++;
                       let mid = uploadscanceled + uploadfinished+folderuploadsinprogress;
                       console.log('mid id:',mid)
                       adduploadfolder(uploadfoldername,uploadfinished+folderuploadsinprogress);
                       folderuploadsinprogress++;
                       console.log('folderuploadcount ',uploadcount)
                  
                       startHover();
                       var started_at = new Date();
                       xhrfolder = new window.XMLHttpRequest();
                       //Upload progress
                       xhrfolder.upload.addEventListener("progress", function(e){

                           //check if file upload has been canceled
                    if (xhrcancel.has(mid)){
                        //upload next file in queue
                        uploadscanceled++;
                        console.log('xhrcancel ',xhrfoldercancel);
                        xhr.abort();
                    }
                       if( e.lengthComputable )
            {
                // Append progress percentage.
                var loaded = e.loaded;
                var total = e.total;
                var progressValue = Math.round( ( loaded / total ) * 100 );

               

                // Time Remaining
                var seconds_elapsed =   ( new Date().getTime() - started_at.getTime() )/1000;
                var bytes_per_second =  seconds_elapsed ? loaded / seconds_elapsed : 0 ;
                var Kbytes_per_second = bytes_per_second / 1000 ;
                var remaining_bytes =   total - loaded;
                var seconds_remaining = seconds_elapsed ? remaining_bytes / bytes_per_second : 'calculating' ;
                console.log('seconds remaing ',seconds_remaining);
                $("#futimer").text(Math.round(seconds_remaining) + ' seconds remaining');
                 //$("#progresscircle"+counter+uploadfinished).addClass('progress-'+progressValue);

             
            }
                var done = e.position || e.loaded
                var total = e.totalSize || e.total;
                var prog = Math.round(done/total*100);
              
                console.log('done ',done);
            
                //console.log('xhr progress: ' + prog + '%');
                //console.log('counter=',counter);
                //$("#progresstext"+counter).text(prog);
                console.log('am i correct ',uploadfinished);
                console.log('the progress ',prog);
                $("#progresscircle"+mid).addClass('progress-'+prog);
                if(prog == 100){
                    console.log('folderuploadinprogress ',folderuploadsinprogress)
                    console.log('uploadfinished ', mid)
                    $("#"+mid).addClass('udone');
                    console.log('class udone added to ',mid)
                     
                }
            });



                     //Download progress
                       return xhrfolder;
                },
                url: '/uploads/subfolderupload/',
                type: 'post',
                data: formData,

                //headers: token,    // django post requests are blocked by default, bring csfr_token
                cache: false,
                // tell jquery not set Content-Type request header
                contentType: false,
                // tell jquery do not have to deal with the data sent
                processData: false,
                success: function (resp) {
                    console.log('resp', resp)
                    foldername = resp.split('-')[0]
                    fid = resp.split('-')[1]
                    console.log('foldername ',foldername)
                    console.log('fid ',fid)
                    console.log('folderuploadfinished success ',uploadfinished)
                    finishuploadfolder(uploadfinished+folderuploadinprogress, fid);
                    console.log('folderuploadfinished return ',uploadfinished)
                    folderuploadsinprogress--;
                    isUploadInProgress = 0;
                    addfolder(foldername,fid)
                  
                },
                error: function (resp) {
                    
                }
            })
        })
    })