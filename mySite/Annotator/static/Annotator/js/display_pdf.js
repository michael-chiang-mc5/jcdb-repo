// see http://jsfiddle.net/seikichi/RuDvz/2/
// https://developer.tizen.org/community/tip-tech/displaying-pdf-files-pdf.js-library



$(document).ready(function() {

  PDFJS.workerSrc = 'http://seikichi.github.io/tmp/PDFJS.0.8.715/pdf.min.worker.js';
  var scale = 3
  var currentPage = 1
  var cumulative_offset = 0

  PDFJS.getDocument(pdf_url).then(iterate);   // load PDF document
  function iterate(pdf) {
    // init parsing of first page
    if (currentPage <= pdf.numPages) getPage();

    // main entry point/function for loop
    function getPage() {
      // when promise is returned do as usual
      pdf.getPage(currentPage).then(function(page) {
        var viewport = page.getViewport(scale);
        var $canvas = $('#the-canvas-'+currentPage);
        var canvas = $canvas.get(0);
        var context = canvas.getContext("2d");
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };

        page.render(renderContext).then(function() {
          if (currentPage < pdf.numPages) {
            resize();
            // recursive step
            currentPage++;
            getPage();
          } else {
            resize();
            // eliminate whitespace
            var height = $('.content').height();
            $(".content").css("max-height",height/scale+20).css("overflow","hidden")
            done();
          }
        });

        function resize() {
          $("#the-canvas-"+currentPage).css("transform", "scale("+1/scale+","+1/scale+")").css("transform-origin", "top left");
          var pdfContainer = $("#pdfContainer-"+currentPage);
          var height = pdfContainer.height();
          var width = pdfContainer.width();
          $("#pdfContainer-"+currentPage).css("height", height/scale).css("width", width/scale);
          $("#pdfContainer-"+currentPage).css("transform", "translate(0px,-"+cumulative_offset+"px)");
          cumulative_offset += height-height/scale
        }

      });
    }

  }


});
