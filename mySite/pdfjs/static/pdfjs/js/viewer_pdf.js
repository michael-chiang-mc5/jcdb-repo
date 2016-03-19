
/* Example of how to call cross-frame javascript function
$(document).ready(function() {
  $('*').dblclick(function (e) {
    var frames = window.parent.frames;
    frames[1].document.body.style.backgroundColor = "red";
    frames[1].abc();
  });
});
*/

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
      var page_number = closest_page_id.substring(13)
      var offset = page.offset();
      var x = e.pageX - offset.left;
      var y = e.pageY - offset.top;
      var page_width = page.width()
      var page_height = page.height()
      var x_normalized = x/page_width;
      var y_normalized = y/page_height;
      // place note
      /*
      div_txt=''+
      '<div class="note">' +
      '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
      '    <br />' +
      '    <input type="submit" value="submit"/>' +
      '</div>'
      */
      div_txt=''+
              '<div class="note">'+
                'Type here:'+
                '<form role="form" action="'+addnote_url+'" method=POST>'+
                  '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'" />'+
                  '<input type="hidden" name="document_pk" value="'+document_pk+'" />'+
                  '<input type="hidden" name="page_number" value="'+page_number+'" />'+
                  '<input type="hidden" name="x_normalized" value="'+x_normalized+'" />'+
                  '<input type="hidden" name="y_normalized" value="'+y_normalized+'" />'+
                  '<input type="hidden" name="width" value="3" />'+
                  '<input type="hidden" name="height" value="4" />'+
                  '<textarea name="form_text" cols="10" rows="5"></textarea>'+
                '</form>'+
                '<button class="submit-previous-form">submit</button>'+
              '</div>'
      var d = $(div_txt);
      page.append(d)
      d.css({top: y, left: x });
      d.draggable()
    }
  });
});

// binding to dynamically created notes
// http://stackoverflow.com/questions/203198/event-binding-on-dynamically-created-elements
$(document).on('click', '.submit-previous-form', function(){
  alert("submitted")
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



// note form submission via ajax
// TODO: also update note element, note global variable via ajax
// https://scotch.io/tutorials/submitting-ajax-forms-with-jquery
$(document).ready(function() {
    // process the form
    $(".submit-previous-form").click(function() {
      alert("submitted")
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
