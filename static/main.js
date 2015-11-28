var vids = new Object();

vids["allemande"] = "allemande.mp4";
vids["box the gnat"] = "gnat.mp4";
vids["california"] = "cal.mp4";
vids["chain"] = "chain.mp4";
vids["magnetize"] = "magnetize.mp4";
vids["petronella"] = "petr.mp4";
vids["star"] = "star.mp4";
vids["swing"] = "petr.mp4";
// vids[""] = ".mp4";

var vidKeys = Object.keys(vids);
var vidsNum = vidKeys.length;

for (i=0; i < vidsNum; i++){
  $('#choreo').each(function() {
    var text = $(this).html();
    $(this).html(text.split(vidKeys[i]).join('<a class="visual_move" data-url="../static/' + vids[vidKeys[i]] + '">' + vidKeys[i] + '</a>'));
  });
}

$('.visual_move').on('click', function(evt){
  console.log($(this).data("url"));
  playMove($(this).data("url"));
});

function playMove(moveId){
  $('#clips').html('<video src=' + moveId + ' autoplay="True" muted="True" type="video/mp4"></video>');
}