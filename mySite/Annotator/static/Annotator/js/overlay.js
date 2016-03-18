$(document).ready(function() {

  $('img').click(function(e) {

    // Get mouse click coordinates
    var offset = $(this).offset();
    var x = e.pageX - offset.left;
    var y = e.pageY - offset.top;


    div_txt=''+
    '<div class="asdf">' +
    '    asdf<br />' +
    '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
    '    <br />' +
    '    <input type="submit" value="submit"/>' +
    '</div>'

    var d = $(div_txt);
    $("#box").append(d)
    d.css({top: y, left: x});
    d.draggable({

    })




    //d.resizable();






  });


});
