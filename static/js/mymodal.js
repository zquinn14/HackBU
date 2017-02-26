/**
 * Created by skale on 2/25/2017.
 */
jQuery(function($) {
    $('#simpleForm').on('submit', function(event) {
        event.preventDefault();
        submitform();
        $('#mymodal').modal('toggle');
    });

    function submitform(){
        var artistname = $("#artistname").val();
        var songname = $("#songtitle").val();
        var twittername = $("#twitteraccount").val();
        $.ajax({
            url: "/generate",
            type: "POST",
            dataType: 'application/json',
            data: {
                song_title:songname,
                song_artist:artistname,
                twitter_handle:twittername

            },
            success: function(data){
                console.log(data);
                if(!("error" in data)) {
                    $("#processStat .songolink").html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
                    $("#processStat .song-o").html(data['original']);
                    $("#processStat .songnlink").html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
                    $("#processStat .song-n").html(data['generated']);
                    Success();
                }
                else{
                    Error();
                }
            },
            error: function (data) {
                Error();
            }
        });
    }

    function Success(){
        $( "#processStat" ).removeClass( "hidden" );
    }

    function Error(){
        $( ".alert-warning" ).removeClass( "hidden" );
    }

    $(".mystart").on('click',function(event) {
        $( "#processStat" ).addClass( "hidden" );
        $( ".alert-warning" ).addClass( "hidden" );
    })
});