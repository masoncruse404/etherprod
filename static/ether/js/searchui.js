//when input search drive is clicked the search type ui is displayed
//change focus to new input bar in the search type ui
//remove text

$(".search").click(function() {
    $("#searchui").css('display','block');
    $("#searchtypewrapper").css('display','block');
    $(".search").css('display','none');
    document.getElementById("searchuinput").focus();
    $("#searchuinput").attr('value','');
});

$("#searchimagerow").click(function() {
    window.location.href = '#';
    $("#searchui").css('display','block');
    $("#searchtypewrapper").css('display','block');
    $(".search").css('display','none');
    document.getElementById("searchuinput").focus();
    $("#searchuinput").attr('value','');
});

    $(function(){
            $("#searchuinput").keyup(function () {
      var searchq = $("#searchuinput").val();
      $.ajax({
        type: "POST",
        url: '/ajax/searchajax/',
        data: {
          'searchq': searchq
        },
        success: searchSuccess,
        dataType: 'html'
        

    });
    });
});
function searchSuccess(data, textStatus, jqXHR){
      var searchq = $("#searchuinput").val();
    if(searchq.length === 0){

    $('#search-results-wrapper').css('display','none');
    $('#searchtypewrapper').css('display','block');
    }
    else
    {
    $('#search-results-wrapper').css('display','block');
    $('#searchtypewrapper').css('display','none');
    }
    $('#search-results-wrapper').html(data);
}   

//right down arrow
//does nothing when clicked 
$("#searchdown1").click(function() {
});

//clears the input when the x icon is clicked
function searchclear(){
    //clear old input
    document.getElementById("searchuinput").value = '';
    //get ready for new input
    $("#searchuinput").focus()
}
//when x is clicked clears the value of the input 
//removes search results
//adds search type 
$("#searchdown").click(function() {
    $(".searchinput").attr('value','');
    if($(this).val().length === 0){
    $("#sclosehover").css('display','none');
    $('#search-results').css('display','none');
    $('#search-results-wrapper').css('display','none');
    $("#searchtypewrapper").css('display','block');
    }
    $("#sclosehover").css('display','flex');
});

$(".searchinput").click(function() {
    $(".searchinput").attr('value','');
    if($(this).val().length === 0){
    $("#sclosehover").css('display','none');
    $('#search-results').css('display','none');
    }
    $("#sclosehover").css('display','flex');
})

$(".searchinput").on('input', function(){

    if($(this).val().length === 0){
    $("#sclosehover").css('display','none');
    $('#search-results').css('display','none');
    }
    $("#sclosehover").css('display','flex');
});

$(function() {
  $("body").click(function(e) {
    if (e.target.id == "searchui" || e.target.id == "searchheader" || $(e.target).parents("#searchui").length) {
    } else {
        if($('#searchui').css('display') == 'none'){

        }
        {
        $("#searchui").css('display','none');
        $("#searchheader").css('display','block');
        }
    }
  });
})


