$("#email_code_submit").click(function(event){
    event.preventDefault();
    email = $("#email").val();
    csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: "/reg_mail_code/",
        dataType: "json",
        data: {'email': email, 'csrfmiddlewaretoken': csrfmiddlewaretoken},
        success: function(data){
            console.log(data);
        }});

});
