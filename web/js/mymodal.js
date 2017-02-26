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
        var songname = $("#songtitle").val();
        var twittername = $("#twitteraccount").val();
        $.ajax({
            url: "main.py",
            type: "POST",
            dataType: 'json',
            data: {
                songname:songname
            },
            success: function(data){
                $( "#processStat .songolink" ).html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
                $( "#processStat .song-o" ).html("Nice to meet you, where you been? I could show you incredible things Magic, madness, heaven, sin Saw you there and I thought Oh my God, look at that face You look like my next mistake Love's a game, want to play? New money, suit and tie I can read you like a magazine Ain't it funny, rumors fly And I know you heard about me So hey, let's be friends I'm dying to see how this one ends Grab your passport and my hand I can make the bad guys good for a weekend");
            },
            error: function (data) {
                console.log(data);
                $( ".alert-warning" ).removeClass( "hidden" );
            }
        });
        // $.ajax({
        //     type: "POST",
        //     dataType: 'json',
        //     data: {
        //         songname:songname
        //     },
        //     success: function(data){
        //
        //     },
        //     error: function (data) {
        //
        //     }
        // });
        $( "#processStat .songnlink" ).html('<a class="btn btn-primary" href="#" role="button">Download &raquo;</a>');
        $( "#processStat .song-n" ).html("Nice to meet you, where you been? I could show you incredible things Magic, madness, heaven, sin Saw you there and I thought Oh my God, look at that face You look like my next mistake Love's a game, want to play? New money, suit and tie I can read you like a magazine Ain't it funny, rumors fly And I know you heard about me So hey, let's be friends I'm dying to see how this one ends Grab your passport and my hand I can make the bad guys good for a weekend");
        Success();
    }

    function Success(){
        $( "#processStat" ).removeClass( "hidden" );
    }

    $(".mystart").on('click',function(event) {
        $( "#processStat" ).addClass( "hidden" );
    })
});