$(document).ready(function() {

  var canvas = document.getElementById('demo'),
      ctx = canvas.getContext('2d'),
      line = new Line(ctx),
      img = new Image;

  ctx.strokeStyle = '#fddd';
  img.onload = start;
  img.src = 'http://i.imgur.com/O712qpO.jpg';

  function start() {
      ctx.drawImage(img, 0, 0, demo.width, demo.height);
      //canvas.onmousemove = updateLine;
      canvas.addEventListener("mousedown", drawBox, false)

  }

  function drawBox(e) {
    var r = canvas.getBoundingClientRect(),
        x = e.clientX - r.left,
        y = e.clientY - r.top;
    ctx.fillStyle = '#f00';
    ctx.strokeStyle	= '#f00';

    //var x = e.pageX;
    //var y = e.pageY;
    //alert("x="+x+", y="+y);

    //ctx.drawImage(img, 0, 0, canvas.width, canvas.height);


    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x-10,y-10);
    ctx.lineTo(x+10,y-10);
    ctx.lineTo(x,y);
    ctx.closePath();
    ctx.fill();
    ctx.fillRect(x-10,y-30,20,20);



    ctx.stroke();


  }

  function updateLine(e) {
      var r = canvas.getBoundingClientRect(),
          x = e.clientX - r.left,
          y = e.clientY - r.top;

      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      line.x1 = x;
      line.y1 = 0;
      line.x2 = x;
      line.y2 = canvas.height;
      line.draw();
  }

  function Line(ctx) {

      var me = this;

      this.x1 = 0;
      this.x2 = 0;
      this.y1 = 0;
      this.y2 = 0;

      this.draw = function() {
          ctx.beginPath();
          ctx.moveTo(me.x1, me.y1);
          ctx.lineTo(me.x2, me.y2);
          ctx.stroke();
      }
  }


});
