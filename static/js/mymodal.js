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
        loaderEnable();
        var artistname = $("#artistname").val();
        var songname = $("#songtitle").val();
        var twittername = $("#twitteraccount").val();
        $.ajax({
            url: "/generate",
            type: "POST",
            data: {
                song_title:songname,
                song_artist:artistname,
                twitter_handle:twittername

            },
            success: function(data){
                //console.log("Success: " + data);
                if(!("error" in data)) {
                    $("#processStat .songolink").html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
                    $("#processStat .song-o").html(data['original']);
                    $("#processStat .song-titleo").html(songname+" - Original");
                    $("#processStat .songnlink").html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
                    $("#processStat .song-n").html(data['generated']);
                    $("#processStat .song-titlen").html(songname+" - Converted");
                    Success();
                }
                else{
                    //console.log("Error: " + data);
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
        loaderDisable();
    }

    function Error(){
        $( ".alert-warning" ).removeClass( "hidden" );
        loaderDisable();
    }

    function loaderEnable() {
        $( ".loader" ).removeClass( "hidden" );
        $( ".container" ).addClass( "hidden" );
    }

    function loaderDisable() {
        $( ".loader" ).addClass( "hidden" );
        $( ".container" ).removeClass( "hidden" );
    }

    $(".mystart").on('click',function(event) {
        $( "#processStat" ).addClass( "hidden" );
        $( ".alert-warning" ).addClass( "hidden" );
    })
});