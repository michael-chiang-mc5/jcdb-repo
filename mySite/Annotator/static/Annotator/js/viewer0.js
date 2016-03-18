// see http://jsfiddle.net/seikichi/RuDvz/2/
// https://developer.tizen.org/community/tip-tech/displaying-pdf-files-pdf.js-library

$(document).ready(function() {

  PDFJS.workerSrc = 'http://seikichi.github.io/tmp/PDFJS.0.8.715/pdf.min.worker.js';

  $(function () {
      var scale = 4

      //PDFJS.getDocument(pdfData).then(function (pdf) {
      PDFJS.getDocument("/static/Annotator/Science.pdf").then(function (pdf) {
          return pdf.getPage(1);
      }).then(function (page) {
          var viewport = page.getViewport(scale);
          var $canvas = $('#the-canvas');
          var canvas = $canvas.get(0);
          var context = canvas.getContext("2d");
          canvas.height = viewport.height;
          canvas.width = viewport.width;

          var $pdfContainer = $("#pdfContainer");
          $pdfContainer.css("height", canvas.height + "px")
              .css("width", canvas.width + "px");

          var renderContext = {
              canvasContext: context,
              viewport: viewport
          };
          page.render(renderContext);



      }).then(function(e) {

        $("#the-canvas").css("transform", "scale("+1/scale+","+1/scale+")")
            .css("transform-origin", "top left");

        var pdfContainer = $("#pdfContainer");
        var height = pdfContainer.height();
        var width = pdfContainer.width();
        pdfContainer.css("height", height/scale)
            .css("width", width/scale);
      })
      ;


  });



  $('#the-canvas').click(function(e) {
    // Get mouse click coordinates
    var offset = $(this).offset();
    var x = e.pageX - offset.left;
    var y = e.pageY - offset.top;


    div_txt=''+
    '<div class="asdf">' +
    '    asdf<br />' +
    '    <textarea name="ta" id="ta" cols="10" rows="5"></textarea>' +
    '    <br />' +
    '    <input type="submit" value="submit"/>' +
    '</div>'

    var d = $(div_txt);
    $("#pdfContainer").append(d)
    d.css({top: e.pageY, left: e.pageX });
    d.draggable({

    })




  });


});
