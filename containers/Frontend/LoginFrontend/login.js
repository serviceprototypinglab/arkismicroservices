/**
 * Created by manuel on 25/01/17.
 */
$(document).ready(function(){
    var host = document.location.hostname;

    var port_users = 30001;
    var port_admin = 32002;
    var port_normal_user = 32001;
    var port_login = 32000;


    $("#loader_id").hide();

    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });


    $("#create_id").click(function(){
        var url = 'http://'+host+':'+port_users + '/users';
        var username =  $("#new_user_id").val();
        var pass =  $("#new_pass_id").val();
        var option =  $("#new_tenant_id").val();

        $.post( url, { username: username, pass: pass, option: option})
            .done(function( data ) {
                alert("Created");
                $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
                $("#new_user_id").val("");
                $("#new_pass_id").val("");
                $("#new_tenant_id").val("");
            });
        return false;
    });

    $("#login_id").click(function(){
        $("#loader_id").show();
        $("#no_loader_id").hide();

        var hostname = document.location.hostname;
        var res = "no";
        var url1 = 'http://'+host+':'+port_users + '/validate/' + $("#user_id").val() + '/' + $("#pass_id").val();
        $.get(url1, function(data){
        }).done(function( data ) {
            res = data[0]['res'];
            if (res == "yes") {
                var user = data[0]['user'];
                var option = data[0]['option'];
                var username = data[0]['username'];
                var role = data[0]['role'];
                var url = '';
                if (role == 'admin') {
                    url = 'http://' + hostname + ":"+ port_admin + "/index.html?user=" + user + "&option=" + option + "&username=" + username;
                } else {
                    url = 'http://' + hostname + ":" + port_normal_user+ "/index.html?user=" + user + "&option=" + option + "&username=" + username;
                }
                $("#loader_id").hide();
                $("#no_loader_id").show();
                window.location.replace(url);
            } else {
                alert("Try again!");
                $("#loader_id").hide();
                $("#no_loader_id").show();
            }
        });
        return false;
    });

    $("#title_arkis_id").click(function(){
        var url = 'http://' + host + ':' + port_login + '/login.html';
        window.location.replace(url);
    });

});