var vids = {};

// TODO modularize via database.
vids["allemande"] = "allemande.mp4";
vids["box the gnat"] = "gnat.mp4";
vids["california"] = "cal.mp4";
vids["chain"] = "chain.mp4";
vids["circle left"] = "circle.mp4";
vids["circle right"] = "circle.mp4";
vids["do si do"] = "dosido.mp4";
vids["hey"] = "hey.mp4";
vids["forward and back"] = "llfb.mp4";
vids["magnetize"] = "magnetize.mp4";
vids["pass through"] = "pass.mp4";
vids["petronella"] = "petr.mp4";
vids["promenade"] = "promenade.mp4";
vids["right/left through"] = "rlth.mp4";
vids["star"] = "star.mp4";
vids["swing"] = "swing.mp4";

var vidKeys = Object.keys(vids);
var vidsNum = vidKeys.length;

// Add event listener 
for (i=0; i < vidsNum; i++){
  $('#choreo').each(function() {
    var text = $(this).html();
    $(this).html(text.split(vidKeys[i]).join('<a class="visual_move" data-url="../static/move_vids/' + vids[vidKeys[i]] + '">' + vidKeys[i] + '</a>'));
  });
}

$('.visual_move').on('click', function(evt){
  console.log($(this).data("url"));
  playMove($(this).data("url"));
});

function playMove(moveId){
  $('#clips').html('<video src=' + moveId + ' autoplay="True" muted="True" type="video/mp4"></video>');
}