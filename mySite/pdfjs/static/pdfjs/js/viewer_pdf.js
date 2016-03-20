
/* Example of how to call cross-frame javascript function
$(document).ready(function() {
  $('*').dblclick(function (e) {
    var frames = window.parent.frames;
    frames[1].document.body.style.backgroundColor = "red";
    frames[1].abc();
  });
});
*/


function createNote() {
}

// On page rendering, re-render notes
// https://github.com/mozilla/pdf.js/issues/5601
$(document).bind('pagerendered', function (e) {
  page_number = e.originalEvent.detail.pageNumber;
  renderNotes(page_number);
});

// remove all saved notes on page=page_number


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
      div_txt=''+
              '<div class="note-boundary">'+
                '<form role="form" class="fill-space" action="'+addnote_url+'" method=POST>'+
                  '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'" />'+
                  '<input type="hidden" name="document_pk" value="'+document_pk+'" />'+
                  '<input type="hidden" name="page_number" value="'+page_number+'" />'+
                  '<input type="hidden" name="x_normalized" value="'+x_normalized+'" />'+
                  '<input type="hidden" name="y_normalized" value="'+y_normalized+'" />'+
                  '<input type="hidden" name="width" value="3" />'+
                  '<input type="hidden" name="height" value="4" />'+
                  '<textarea name="form_text" placeholder="Type here" class="default-note-size"></textarea>'+
                '</form>'+
                '<a class="submit-previous-form note-footer cursor right">submit</button>'+
                '<a class="note-footer cursor left">delete</button>'+
              '</div>'
      var d = $(div_txt);
      page.append(d)
      d.css({top: y, left: x });
      d.draggable()
    }
  });
});

// Implements submit on note buttons
// binding to dynamically created notes
// http://stackoverflow.com/questions/203198/event-binding-on-dynamically-created-elements
$(document).on('click', '.submit-previous-form', function(){
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
  });
  // stop the form from submitting the normal way and refreshing the page
  event.preventDefault();
});


// POST to view getNotesJson
// returns a JSON object that represents notes in database
// Usage: notesDB_global[i].note_text[j].text
//        where i is the ith note, j is th jth comment in the ith note
window.notesDB_global=0; // global variable for storing database
function getNotesJson() {
  // process the form
  $.ajax({
    type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
    url         : getnotesjson_url, // the url where we want to POST
    data        : {'csrfmiddlewaretoken':csrf_token}, // our data object
    dataType    : 'json', // what type of data do we expect back from the server
                encode          : true
  }).done(function(data) {
    notesDB_global=data
    //alert(notes[0].note_text[0].text)
  });
}
// render all notes on a given page
function renderNotes(page_number) {
  for (i=0;i<notesDB_global.length;i++) { // iterate through all notes
    var pn = notesDB_global[i].page_number
    if (pn == page_number) {  // check if note is on the right page
      renderNote(notesDB_global[i])
    }
  }
}
// render a single note object. This function will not work properly
// if corresponding canvas has not been rendered
// Usage: note_obj.page_number
//        note_obj.x_normalized_position
//        note_obj.note_text[i].text
function renderNote(note_obj) {
  // get x,y position of note
  var page_number = note_obj.page_number
  var page = $("#pageContainer"+page_number)
  var page_width = page.width()
  var page_height = page.height()
  var x_normalized = note_obj.x_normalized_position;
  var y_normalized = note_obj.y_normalized_position;
  var x = x_normalized*page_width
  var y = y_normalized*page_height
  var num_replies = note_obj.note_text.length - 1 // minus one because first text is original note

  // create note
  div_txt=''+
          '<div id="savednote-'+note_obj.pk+'" class="note-boundary">'+
            '<div class="resizable">'+
                note_obj.note_text[0].text+
            '</div>'+
            '<a class="note-footer cursor right">'+num_replies+' replies</button>'+
          '</div>'
  var d = $(div_txt);
  page.append(d)
  d.css({top: y, left: x });
  d.draggable()
  var resizable = d.children( ".resizable" )
  make_resizable(resizable)
}


function make_resizable(obj) {
  obj
    .wrap('<div/>')
      .css({'overflow':'hidden'})
        .parent()
          .css({'display':'block',
                'overflow':'hidden',
                'height':function(){return $('.resizable',this).height();},
                'width':  function(){return $('.resizable',this).width();},
               }).resizable()
                  .find('.resizable')
                    .css({overflow:'auto',
                          width:'100%',
                          height:'100%'});
}
