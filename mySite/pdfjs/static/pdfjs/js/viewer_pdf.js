// These are functions to modify notesDB_global
function delete_notetext(notetext_pk) {
  for (var i=0;i<notesDB_global.length;i++) {
    for (var j=0;j<notesDB_global[i].note_text.length;j++) {
        if (notesDB_global[i].note_text[j].pk == notetext_pk) {
          notesDB_global[i].note_text.splice(j, 1);
          break;
        }
    }
  }
}
function modify_widthheight(note_pk,width,height) {
  console.log(note_pk)
  for (var i=0;i<notesDB_global.length;i++) {
    if (notesDB_global[i].pk == note_pk) {
      console.log("found")
      notesDB_global[i].width=width
      notesDB_global[i].height=height
      break;
    }
  }
}
function modify_position(note_pk,x_normalized,y_normalized) {
  console.log(note_pk)
  for (var i=0;i<notesDB_global.length;i++) {
    if (notesDB_global[i].pk == note_pk) {
      notesDB_global[i].x_normalized_position=x_normalized
      notesDB_global[i].y_normalized_position=y_normalized
      break;
    }
  }
}
function modify_notetext(notetext_pk, text) {
  for (var i=0;i<notesDB_global.length;i++) {
    for (var j=0;j<notesDB_global[i].note_text.length;j++) {
        if (notesDB_global[i].note_text[j].pk == notetext_pk) {
          notesDB_global[i].note_text[j].text = text;
          break;
        }
    }
  }
}
function add_notetext(note_pk, notetext_obj) {
  for (var i=0;i<notesDB_global.length;i++) {
    if (notesDB_global[i].pk == note_pk) {
      console.log("found")
      notesDB_global[i].note_text.push(notetext_obj)
      break;
    }
  }
}

function delete_note(note_pk) {
  for (var i=0;i<notesDB_global.length;i++) {
      if (notesDB_global[i].pk == note_pk) {
        notesDB_global.splice(i, 1);
        break;
      }
  }
}

// these are function that draw from notesDB_global
function renderNoteByPk(note_pk) {
  for (var i=0;i<notesDB_global.length;i++) {
    if (notesDB_global[i].pk == note_pk) {
      var note_obj = notesDB_global[i]
      renderNote(note_obj)
      break;
    }
  }
}


/* Example of how to call cross-frame javascript function
$(document).ready(function() {
  $('*').dblclick(function (e) {
    var frames = window.parent.frames;
    frames[1].document.body.style.backgroundColor = "red";
    frames[1].abc();
  });
});
*/

// highlight div
function zoom(note_pk, page_number) {
  // first scroll to page in case not loaded
  $("#pageContainer"+page_number)[0].scrollIntoView(true);
  // TODO: best to wait if element loaded
  var note = $('#savednote'+note_pk)
  note[0].scrollIntoView(true);
  note.effect("shake", {}, 700);
}


// On page rendering, re-render notes
// https://github.com/mozilla/pdf.js/issues/5601
$(document).bind('pagerendered', function (e) {
  page_number = e.originalEvent.detail.pageNumber;
  renderNotes(page_number);
});


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
              '<div pagenumber="'+page_number+'" class="note-boundary">'+
                '<form role="form" class="fill-space" action="'+addnote_url+'" method=POST>'+
                  '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'" />'+
                  '<input type="hidden" name="document_pk" value="'+document_pk+'" />'+
                  '<input type="hidden" name="page_number" value="'+page_number+'" />'+
                  //'<input type="hidden" name="x_normalized" value="'+x_normalized+'" />'+
                  //'<input type="hidden" name="y_normalized" value="'+y_normalized+'" />'+
                  //'<input type="hidden" name="width" value="3" />'+
                  //'<input type="hidden" name="height" value="4" />'+
                  '<textarea name="form_text" placeholder="Type here" class="default-note-size"></textarea>'+
                '</form>'+
                '<a class="submit-note note-footer cursor right">submit</button>'+
                '<a class="remove-note-self note-footer cursor left">delete</button>'+
              '</div>'
      var d = $(div_txt);
      page.append(d)
      d.css({top: y, left: x });
      d.draggable()
    }
  });
});

// Implements submit on note buttons
// Will not submit if text is empty
// binding to dynamically created notes: http://stackoverflow.com/questions/203198/event-binding-on-dynamically-created-elements
$(document).on('click', '.submit-note', function(){
  // get note position
  var f = $(this).prev('form');
  var note = f.parent()
  var position = note.position();
  var page_number = note.attr('pagenumber')
  var page = $("#pageContainer"+page_number)
  var x = position.left;
  var y = position.top;
  var page_width = page.width()
  var page_height = page.height()
  var x_normalized = x/page_width;
  var y_normalized = y/page_height;
  // get note width and height
  var textarea = f.children('textarea');
  var width = textarea.width();
  var height = textarea.height();
  console.log(textarea.width(), textarea.height())


  var txt = f.children("textarea").val()
  if (txt.length==0) { // do not submit if form is empty
    f.parent().remove();
  } else {
    var url = f.attr( 'action' );
    var me = $(this)
    // process the form
    $.ajax({
      type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
      url         : url, // the url where we want to POST
      data        : f.serialize() + '&x_normalized='+x_normalized+'&y_normalized='+y_normalized+'&width='+width+'&height='+height, // our data object
      dataType    : 'json', // what type of data do we expect back from the server
                  encode          : true
    }).done(function(obj) {
      // remove note editor
      me.parent().remove();
      // create note json object
      note_obj = obj.note_obj
      // render note
      renderNote(note_obj)
      // save note to local db
      notesDB_global.push(note_obj)
      // write note to note iframe
      var frames = window.parent.frames;
      frames[1].createNote(note_obj);

    });
  }
  // stop the form from submitting the normal way and refreshing the page
  event.preventDefault();
});
// Implements delete on note buttons
$(document).on('click', '.remove-note-self', function(){
  $(this).parent().remove();
  event.preventDefault();
});

// zoom to corresponding post in note iframe
$(document).on('click', '.zoom-iframe', function(){
  var note_pk = $(this).attr('id')
  var frames = window.parent.frames;
  frames[1].zoom(note_pk);
  event.preventDefault();
});

// POST to view getNotesJson
// returns a JSON object that represents notes in database
// Usage: notesDB_global[i].note_text[j].text
//        where i is the ith note, j is th jth comment in the ith note
window.notesDB_global=0; // global variable for storing database

/* deprecated
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
    removeNotes(-1)
    renderNotes(-1)
    window.parent.frames[1].location.reload();

    //alert(notes[0].note_text[0].text)
  });
}
*/

/* deprecated
// removes all notes on a given page
// if page_number == -1, then remove all notes over entire pdf
function removeNotes(page_number) {
  $(".note-boundary").remove()
}
*/

function removeNote(note_pk) {
  $("#savednote"+note_pk).remove()
}

// render all notes on a given page
// if page_number == -1, then do all notes over entire pdf
function renderNotes(page_number) {
  for (var i=0;i<notesDB_global.length;i++) { // iterate through all notes
    var pn = notesDB_global[i].page_number
    if (pn == page_number || page_number == -1) {  // check if note is on the right page
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
  var width = note_obj.width
  var height = note_obj.height
  // create note
  div_txt=''+
          '<div notepk="'+note_obj.pk+'" pagenumber="'+page_number+'" id="savednote'+note_obj.pk+'" class="note-boundary">'+
            '<div notepk="'+note_obj.pk+'" class="resizable">'+
                note_obj.note_text[0].text+
            '</div>'+
            '<a id="'+note_obj.pk+'" class="zoom-iframe note-footer cursor right">'+num_replies+' replies</button>'+
          '</div>'
  var d = $(div_txt);
  page.append(d)
  d.css({top: y, left: x });
  var resizable = d.children( ".resizable" )
  resizable.css({'width':width,'height':height})
  d.draggable({
    // http://api.jqueryui.com/draggable/
    stop: function( event, ui ) {
      var note_pk = $(this).attr('notepk') // $(this) is d
      // get position
      var position = $(this).position();
      var page_number = $(this).attr('pagenumber')
      var page = $("#pageContainer"+page_number)
      var x = position.left;
      var y = position.top;
      var page_width = page.width()
      var page_height = page.height()
      var x_normalized = x/page_width;
      var y_normalized = y/page_height;
      // update position on server
      console.log(dragnote_url)
      $.ajax({
        type        : 'POST',
        url         : dragnote_url,
        data        : {'csrfmiddlewaretoken':csrf_token,
                       'x_normalized':x_normalized,
                       'y_normalized':y_normalized,
                       'note_pk':note_pk}, // our data object
        dataType    : 'json',
                    encode          : true
      }).done(function(data) {
        // update position on local db
        modify_position(note_pk,x_normalized,y_normalized)
        // no need to draw because already resized
      });
    }
  });
  resizable.resizable({
    stop: function( event, ui ) {
      var note_pk = $(this).attr('notepk') // $(this) is resizable
      // get width and height
      var width = $(this).width();
      var height = $(this).height();
      // update width, height on server
      $.ajax({
        type        : 'POST',
        url         : resizenote_url,
        data        : {'csrfmiddlewaretoken':csrf_token,
                       'width':width,
                       'height':height,
                       'note_pk':note_pk}, // our data object
        dataType    : 'json',
                    encode          : true
      }).done(function(data) {
        // update width, height on local db
        modify_widthheight(note_pk,width,height)
        // no need to draw because already resized
      });
    }
  });
}



$(document).bind('resizestop', function (e) {
});


// deprecated
/*
function make_resizable(obj) {
  obj
    .wrap('<div/>')
      .css({'overflow':'hidden'})
        .parent()
          .css({'display':'block',
                'overflow':'hidden',
                'height':function(){return $('.resizable',this).height();},
                'width':  function(){return $('.resizable',this).width();},
               }).resizable({
                  stop: function( event, ui ) {}
                  }).find('.resizable')
                    .css({overflow:'auto',
                          width:'100%',
                          height:'100%'});
}
*/
