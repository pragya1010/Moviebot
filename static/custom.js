  function submit_message(message) {
        $.post( "/send_message", {message: message}, handle_response);

        function handle_response(data) {
            // $reg_exUrl = "/(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?/";
            // $text = data.message

          $('.chat-container').append(`
                <div class="chat-message col-md-8 offset-md-4 bot-message" style="width: 100vw">
                   ${data.message.replace(/\n/g,'<br/><br/>')}
                   ${data.poster}
              
                </div>
                
          `)
          // remove the loading indicator
          $( "#loading" ).remove();
        }
    }


    $('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()

        // return if the user does not enter any text
        if (!input_message) {
          return
        }



        $('.chat-container').append(`
            <div class="chat-message col-md-4 human-message">
                ${input_message}
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center col-md-8 offset-md-10 bot-message" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')


        $('.chat-container').stop().animate({ scrollTop: $('.chat-container')[0].scrollHeight}, 1000);



        // send the message
        submit_message(input_message)
    });