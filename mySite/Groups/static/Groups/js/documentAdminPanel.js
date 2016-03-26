// show edit form when clicking edit
$(document).on('click', '.edit-link', function(){
  var editform = $(this).next(".editform")
  $(editform).toggle();
});

// this puts content in contenteditable div inside textarea for form submission
function getContent(){
  document.getElementById("notification-text").value = document.getElementById("contenteditable-notification").innerHTML;
}
