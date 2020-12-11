var uploadcount = 0;
var uploadfinished = 0;
var uploadscanceled = 0;
var fdata = new FormData();
var datalist = [];
let xhrcancel = new Set()
var xhr;
    

$("#uploadstop").click(function(e){
    xhr.abort();
    $("#fu").css("display","none");
    for(let i=uploadfinished+1; i<uploadcount; i++){
        xhrcancel.add(i);
        
    }
    datalist = [];
    uploadcount = 0;
    fdata = new FormData();
    return;
   
});

function cancelupload(thisid){
     console.log('cancel upload ',thisid);
     console.log('cancel upload finished ',uploadfinished);
     $("#"+thisid).css("display","none");
     if(uploadfinished+uploadscanceled == thisid){
        //cancel current upload
        console.log('cancel current');
        xhr.abort();
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

    function initupload(){
            fdata.append("csrfmiddlewaretoken", $(this).attr("data-csrf-token"));
             console.log('data ',fdata.getAll('file'));
             $("#mbody").css('display','block');
             $("#fu").css("display","block");
             $(".fuheader").css('display','flex');
             $(".foldera").show();
             $(".fuprogresswrapper").css('display','flex');
             $(".futitle").text('Uploading '+uploadcount+' items');
             
            var y = 0;
            for (let ix=uploadfinished, y=0; ix<uploadcount+uploadfinished, y<uploadcount; ix++, y++){
                console.log('itemz ',fdata.getAll('file')[ix]);
                
                addupload(fdata.getAll('file')[y],ix);
            }

             startHover();
            
             ajaxupload(fdata.getAll('file')[0],0);  
    }

    //adds uploaded file to upload UI
    function addupload(file, pcounter){
        console.log('in addUpload');
        var $fufilewrapper = $("<div id='"+pcounter+"' class='fufilewrapper'><i id='futype' class='far fa-image fa-lg'></i><span id='funame'>"+file.name+"</span><div id='chartwrapper"+pcounter+"' class='chartwrapper'><div id=progresscircle"+pcounter+" class='radialProgressBar progress-0'><div id=progresstext"+pcounter+" class='overlay'></div></div></div><div id='fucheck"+pcounter+"' class='fucheck' display='none' ><i class='fas fa-check'></i></div><div class='fufolder'><i class='far fa-folder fa-lg'></i></div><div id='fuclose"+pcounter+"'class='fuclose' onclick='cancelupload("+pcounter+")'><i class='fas fa-times'></i></div></div>");
        $("#mbody").prepend($fufilewrapper);
        //$("#gallery tbody").prepend("<tr><td><a href='#'>" + file.name + "</a></td></tr>")
      }

    function adduploadtable(fileurl,pcounter,filetype,fname){
        var newfile =  "<div id='filetablerow-"+pcounter+"' class='tablerowwrapper filetablerow' onclick='filetablerow(event,this.id)'>" +
        "<div class='tablenamecontainer'><div class='tableiconwrapper'><i class='fas fa-image'></i></div><div class='tablenamewrapper'><span>"+fname+"</span>" +
        "</div></div><div class='tablerightwrapper'><div class='tablerightowner'><span>Me</span></div><div class='tablerightmodified'><span>Now</span></div><div class='tablerightfile'><span>-</span></div></div></div></div>";
    
      $(".filetablerow:last").after(newfile);

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
        if(uploadfinished == uploadcount-1){
            console.log('last one');
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
            data = JSON.parse(this.responseText);
            console.log('response ',data.file);
            console.log('the id ',data.id);
            adduploadtable(data.file,data.id,data.filetype,data.name);
            if(this.status != 200){
                $('#driver-uploader-failure-alert').show();
                return;
            }
            finishupload(counter,data.id);
            ajaxuploadcallback(counter);
            });

            xhr.open('post', '/uploads/upload_driver/', true);
            var fd = new FormData();
            fd.append("filename", filename);
            fd.append("drive_file", file);
            xhr.send(fd);
    }




    $(document).ready(function(){
        $('#upload_file').change(function(){
            //reset
            uploadcount = 0;
            datalist = [];
            fdata = new FormData();
            uploadscanceled = 0;
             $.each($("#upload_file")[0].files, function(i, file) {
                fdata.append("file", file);
                datalist.push(file);
              
                uploadcount++;
            });
            initupload();
            
        });
    });


