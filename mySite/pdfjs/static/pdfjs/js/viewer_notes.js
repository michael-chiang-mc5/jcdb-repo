// form submission via ajax
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
        window.location.reload();
      });
      // stop the form from submitting the normal way and refreshing the page
      event.preventDefault();
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

function zoom_out(note_pk) {
  var note = $("#note"+note_pk)
  var page_number = note.attr('pagenumber')

  zoom(note_pk);
  var frames = window.parent.frames;
  frames[0].zoom(note_pk,page_number);
}


$(document).ready(function() {
    // process the form
    $(".zoom").click(function() {
      var note_pk =$(this).attr("notepk")
      zoom_out(note_pk);
    });
});
