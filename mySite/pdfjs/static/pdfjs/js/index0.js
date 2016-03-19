

$(document).ready(function() {


  $('*').off().dblclick(function (e) {
  //$('*').one("dblclick",function (e) {
      e.stopImmediatePropagation();

      document.title = e.target.tagName + '#' + e.target.id + '.' + e.target.className;
      //alert(e.target.tagName + '#' + e.target.id + '.' + e.target.className)

      var asdf = $(e.target)
      alert(asdf.attr("class"))
      var asdf2 = asdf.closest(".page")
      alert("clostest="+asdf2.attr("id"))

  });

  alert("ready")


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
