

function createNote(page_number, x_normalized, y_normalized, width, height) {
  var page = $("#pageContainer"+page_number)
  div_txt=''+
  '<div class="note">' +
  '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
  '    <br />' +
  '    <input type="submit" value="submit"/>' +
  '</div>'
  var d = $(div_txt);
}

// On page rendering, re-render notes
// https://github.com/mozilla/pdf.js/issues/5601
$(document).bind('pagerendered', function (e) {
  console.log(e.originalEvent.detail.pageNumber); // which page is rendered

});

// remove all saved notes on page=page_number


// render all saved notes on page=page_number
function renderNotes(page_number) {

}

// remove all unsaved notes


$(document).ready(function() {

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
      '<div class="note">' +
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

});



// form submission via ajax
//  https://scotch.io/tutorials/submitting-ajax-forms-with-jquery
$(document).ready(function() {

    // process the form
    $(".submit-previous-form").click(function() {
      var f = $(this).prev('form');
      var url = f.attr( 'action' );
      alert(url)

      // process the form
      $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        url         : url, // the url where we want to POST
        data        : f.serialize(), // our data object
        dataType    : 'json', // what type of data do we expect back from the server
                    encode          : true
      }).done(function(data) {
        alert(data.document_pk)
      });

      // stop the form from submitting the normal way and refreshing the page
      event.preventDefault();
    });

});
