console.log(server)



function api_call(input) {
    $.ajax({
        url: "http://"+server.host+":"+server.port+"/",
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(input),
        success: function( data, textStatus, jQxhr ){
            // $('#api_output').html( data.output );
            // $("#input").val("");
            console.log('success');
            console.log('data', data);
            console.log('textStatus', textStatus);
            console.log('jQxhr', jQxhr);

            create_alert(textStatus, data);
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

function create_alert(state, data) {
    $('.alert-display').append(
        '<div class="alert alert-' + state + ' alert-dismissible fade show" role="alert">' +
            '<strong>' + data + '</strong>, tout s\'est passé comme prévu.' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span>' +
            '</button>' +
        '</div>'); 
}