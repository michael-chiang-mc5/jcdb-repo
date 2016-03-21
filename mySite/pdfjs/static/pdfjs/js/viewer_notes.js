// implements submit button
// https://scotch.io/tutorials/submitting-ajax-forms-with-jquery
$(document).on('click', ".submit-previous-form", function(){

    // process the form
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
        window.location.reload();
      });
      // stop the form from submitting the normal way and refreshing the page
      event.preventDefault();
});

// implements delete button
$(document).on('click', ".delete-link", function(){
  var notetext_pk = $(this).attr('pk')
  var note_pk = $(this).attr('notepk')
  $.ajax({
    type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
    url         : url_deletenotetext, // the url where we want to POST
    data        : {'notetext_pk':notetext_pk,
                   'csrfmiddlewaretoken':csrf_token}, // our data object
    dataType    : 'json', // what type of data do we expect back from the server
                encode          : true
  }).done(function(data) {
    if (data.delete_entire_note) {
      $("#note"+note_pk).remove()
      var frames = window.parent.frames;
      frames[0].removeNote(note_pk);
    } else {
      $("#notetext"+notetext_pk).remove()
      var frames = window.parent.frames;
      frames[0].removeNote(note_pk);
      frames[0].delete_notetext(notetext_pk);
      frames[0].renderNoteByPk(note_pk);
    }
  });
});


// zoom in response from action in pdf frame
function zoom(note_pk) {
  var note = $("#note"+note_pk)

  // turn note yellow, all others grey
  $(".note").css({'background-color':'#F5F5F5'})
  note.css({'background-color':'yellow'})

  // scroll to div
  $("body, html").animate({
    scrollTop: note.offset().top
  }, 600);
}

// implements zoom button
function zoom_out(note_pk) {
  var note = $("#note"+note_pk)
  var page_number = note.attr('pagenumber')
  var frames = window.parent.frames;
  frames[0].zoom(note_pk,page_number);
}

// implements zoom button
$(document).on('click', '.zoom', function(){
    var note_pk =$(this).attr("notepk")
    zoom_out(note_pk);
});
// show reply,edit form when clicking reply, edit
$(document).on('click', '.edit-link', function(){
  var pk = $(this).attr( 'pk' );
  $("#editform"+pk).toggle();
});
$(document).on('click', '.reply-link', function(){
  var pk = $(this).attr( 'pk' );
  $("#replyform"+pk).toggle();
});


// create note in response to note added in pdf iframe
// note: json object of note
function createNote(note) {
  var notetext = note.note_text[0]
  html_txt= ''+
            '<div pagenumber="'+note.page_number+'" id="note'+note.pk+'" class="note">'+
              '<div>'+
                notetext.text+"<br />"+
                '<div class="signature left">'+
                  '--'+notetext.username+', '+notetext.time+
                '</div>'+
                '<div class="right signature edit_button">'+
                  '<a notepk="'+note.pk+'" pk="'+notetext.pk+'" class="delete-link">delete</a>&nbsp;'+
                  '<a pk="'+notetext.pk+'" class="edit-link">edit</a>'+
                '</div>'+
                '<div style="clear: both;"></div>'+
                '<div id="editform'+notetext.pk+'" class="hidden">'+
                  '<form class="note-form" role="form" action="'+url_editNotetext+'" method=POST>'+
                    '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'" />'+
                    '<input type="hidden" name="notetext_pk" value="'+notetext.pk+'" />'+
                    '<textarea name="form_text" cols="10" rows="5">'+notetext.text+'</textarea>'+
                  '</form>'+
                  '<button class="submit-previous-form">submit edit</button>'+
                '</div>'+
              '</div>'+
              '<div>'+
                '<a notepk="'+note.pk+'" class="note_footer zoom left">zoom</a>'+
                '<a pk="'+note.pk+'" class="note_footer reply-link right">reply</a>'+
              '</div>'+
              '<div style="clear: both;"></div>'+
              '<div id="replyform'+note.pk+'" class="hidden">'+
                '<form class="note-form" role="form" action="'+url_replynote+'" method=POST>'+
                  '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'" />'+
                  '<input type="hidden" name="note_pk" value="'+note.pk+'" />'+
                  '<textarea name="form_text" cols="10" rows="5"></textarea>'+
                '</form>'+
                '<button class="submit-previous-form">submit</button>'+
              '</div>'+
            '</div>'
    var el = $(html_txt);
    $("body").append(el)
    zoom(note.pk)
}
