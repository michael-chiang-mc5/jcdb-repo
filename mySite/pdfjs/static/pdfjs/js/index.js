

$(document).ready(function() {

  alert("ready")


  // Create note
  $("#viewer").dblclick(function(e) {

    // Get mouse click coordinates
    var offset = $(this).offset();
    var x = e.pageX - offset.left;
    var y = e.pageY - offset.top;
    alert("x="+x+",y="+y)


    div_txt=''+
    '<div class="asdf">' +
    '    asdf<br />' +
    '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
    '    <br />' +
    '    <input type="submit" value="submit"/>' +
    '</div>'

    var d = $(div_txt);
    $(this).append(d)
    d.css({top: y, left: x });
    d.draggable()
  });

  // TODO: remove empty notes



});
