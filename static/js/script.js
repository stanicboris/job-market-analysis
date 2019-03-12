console.log(data)

function api_call(input) {
    $.ajax({
        url: "http://"+data.host+":"+data.port+"/",
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(input),
        success: function( data, textStatus, jQxhr ){
            // $('#api_output').html( data.output );
            // $("#input").val("");
            console.log('success');
        },
        error: function( jqXhr, textStatus, errorThrown ){
            // $('#api_output').html( "There was an error" );
            console.log( errorThrown );
        },
        timeout: 3000
    });
}
$( document ).ready(function() {
    // request when clicking on the button
    $('.btn-danger').click(function() {
        var input = $(".btn-danger").val();
        api_call(input);
        input = "";
    });
    $('.btn-primary').click(function() {
        var input = $(".btn-primary").val();
        api_call(input);
        input = "";
    });
});