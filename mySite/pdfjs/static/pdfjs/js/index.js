
window.notes=0;

function createNote() {
}

// On page rendering, re-render notes
// https://github.com/mozilla/pdf.js/issues/5601
$(document).bind('pagerendered', function (e) {
  page_number = e.originalEvent.detail.pageNumber;
  console.log(page_number); // which page is rendered
  renderNotes(page_number);
});

// remove all saved notes on page=page_number


// render all saved notes on page=page_number
function renderNotes(page_number) {
  console.log(notes);
}

// On double click, place a note element on the page. This note can submit a
// post form
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



// note form submission via ajax
// TODO: also update note element
// https://scotch.io/tutorials/submitting-ajax-forms-with-jquery
$(document).ready(function() {
    // process the form
    $(".submit-previous-form").click(function() {
      var f = $(this).prev('form');
      var url = f.attr( 'action' );
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
