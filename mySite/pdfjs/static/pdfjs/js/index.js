

$(document).ready(function() {

  /*
  $('*').dblclick(function (e) {
      e.stopImmediatePropagation();
      document.title = e.target.tagName + '#' + e.target.id + '.' + e.target.className;
      var asdf = $(e.target)
      alert(asdf.attr("class"))
      var asdf2 = asdf.closest(".page")
      alert("closest="+asdf2.attr("id"))

  });
  */

  $('*').dblclick(function (e) {

    // Only process first event
    e.stopImmediatePropagation();

    // check if we are clicking on a page
    var closest_page_id = $(e.target).closest(".page").attr("id")
    if(typeof closest_page_id != 'undefined') {
      // Get mouse click coordinates (normalized to page width,height)
      var page = $("#"+closest_page_id)
      var offset = page.offset();
      var x = e.pageX - offset.left;
      var y = e.pageY - offset.top;
      var page_width = page.width()
      var page_height = page.height()
      var x_normalized = x/page_width;
      var y_normalized = y/page_height;
      //alert("x="+x+",y="+y+", id="+closest_page_id+", pagewidth="+page_width+", pageheight="+page_height)
      //alert("x="+x_normalized+",y="+y_normalized+", id="+closest_page_id)

      // place note
      div_txt=''+
      '<div class="asdf">' +
      '    asdf<br />' +
      '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
      '    <br />' +
      '    <input type="submit" value="submit"/>' +
      '</div>'
      var d = $(div_txt);
      page.append(d)
      d.css({top: y, left: x });
      d.draggable()

    }



  });





  // Create note
  $(".asdf").dblclick(function(e) {

    var p = $(this).closest(".page")
    alert(p.attr(""))

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
