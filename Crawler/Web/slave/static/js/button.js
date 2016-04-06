$(function() {
  $( "input[type=submit], a, button" )
    .button()
    .click(function( event ) {
    event.preventDefault();
  });
});

