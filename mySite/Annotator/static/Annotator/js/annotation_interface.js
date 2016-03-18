

$(document).ready(function() {

  // Create note
  $('.pdf-content').click(function(e) {
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
    $(this).parent().append(d)
    d.css({top: e.pageY, left: e.pageX });
    d.draggable()
  });

  // TODO: remove empty notes



});
