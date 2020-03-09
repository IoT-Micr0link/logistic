var firebaseConfig = {
apiKey: "AIzaSyDviIe6ezf1IkLGWxzTM0HWvXlzG7Jkh9Q",
authDomain: "healthy-zone-266815.firebaseapp.com",
databaseURL: "https://healthy-zone-266815.firebaseio.com",
projectId: "healthy-zone-266815",
storageBucket: "healthy-zone-266815.appspot.com",
messagingSenderId: "860922149741",
appId: "1:860922149741:web:16761fe8e63d43d7b77864"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

var database = firebase.database();

var readingsCountRef = database.ref('reads');


function highlightCard() {
  $("#newReadingCard .card-header").removeClass( "bg-gray-500" ).addClass( "bg-success" );
  $("#newReadingCard").addClass( "border-success" );
  $("#newReadingIcon").removeClass( "bg-secondary"  ).addClass( "bg-success" );

  setTimeout(resetCard,2500)
}

function resetCard() {
  $("#newReadingCard .card-header").removeClass("bg-success").addClass(  "bg-gray-500" );
  $("#newReadingCard").removeClass( "border-success" );
  $("#newReadingIcon").removeClass( "bg-success" ).addClass( "bg-secondary" );
}


function updateReading(readingSnapshot){

  highlightCard();
  data = readingSnapshot.val();
  console.log(data);
  itemCount = data.count_reads;
  timestamp = data.time;

  $('#item-count').fadeOut("fast", function(){
    var span = $("<span id='item-count'>"+itemCount+"</span>").hide();
    $(this).replaceWith(span);
    $('#item-count').fadeIn("slow");
  });

  $('#timestamp').fadeOut("fast", function(){
    var span = $("<span id='timestamp'>"+timestamp+"</span>").hide();
    $(this).replaceWith(span);
    $('#timestamp').fadeIn("slow");
  });

    $('#reader-name').fadeOut("fast", function(){
      var span = $("<span id='reader-name'>NODE-BODEGA-134</span>").hide();
      $(this).replaceWith(span);
      $('#reader-name').fadeIn("slow");
    });

    $('#node-name').fadeOut("fast", function(){
      var span = $("<span id='node-name'>ZEBRA - FX9600 </span>").hide();
      $(this).replaceWith(span);
      $('#node-name').fadeIn("slow");
    });


}

readingsCountRef.on('value',updateReading);

