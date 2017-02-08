$(document).ready(function(){
    var host = document.location.hostname;
    var port_documents = 30000;
    var port_users = 30001;
    var port_data = 30002;
    var port_migrate = 30003;
    var port_login = 32000;

    var parameters = location.search.substring(1).split("&");
    var temp1 = parameters[0].split("=");
    var temp2 = parameters[1].split("=");
    var temp3 = parameters[2].split("=");

    var user = 0;
    var user_detail = 0;

    try {
        user = parseInt(temp1[1]);
        user_detail = parseInt(temp1[1]);
    } catch(exception) {
        user = 0;
    }

    var option = temp2[1];
    var option_detail = temp2[1];
    var username = temp3[1];
    var username_detail = temp3[1];

    show_hide("info");
    get_users1();
    get_option1();
    get_table();

    $("#info_l").click(function() {
            show_hide("info");
        });

    $("#user_l").click(function() {
            show_hide("user");
            get_table();
        });

    $("#detail_l").click(function() {
        show_hide("detail");
        $('#username_detail_id').text(username_detail);
        $('#select_multi_tenant_migrate').val(option_detail);
    });

    $("#migrate_id").click(function() {
        var migrate_option = $("#select_multi_tenant_migrate").val();
        var url = 'http://' + host + ':' + port_migrate + '/migrate/' + user_detail + '/' + migrate_option;
        $.get(url, function(data){
        }).done(function( data ) {
            alert(data['success']);
        });
    });

    $("#delete_id").click(function() {
        var url = 'http://' + host + ':' + port_users + '/delete/users/' + user_detail;
        $.get(url, function(data){
        }).done(function( data ) {
            alert(data[0]['res']);
        });
    });

    $("#add_data_id").click(function() {
        var number_documents = $("#number_documents_id").val();
        var url = 'http://' + host + ':' + port_data + '/data/' + user_detail + '/' + option_detail + '/' + number_documents;
        $.get(url, function(data){
        }).done(function( data ) {
            alert(data[0]['error']);
        });
    });

    function get_users1(){
        $("#select_user").append('<option id="user_'+user+'" value="'+ user+ '">' + username + '</option>');
        $("#select_user").val(user);
        $("#loader_id").hide();
        $("#no_loader_id").show();
    }

    function get_option1(){
        $("#select_multi_tenant").val(option);
    }

    function show_hide(id) {
        var ids = ["info", "user", "detail"];
        for (var j = 0; j < ids.length; j++) {
            if (id == ids[j]) {
                $("#" + ids[j]).addClass("active");
                $("#" + ids[j] + "_id").show();
            } else {
                $("#" + ids[j]).removeClass("active");
                $("#" + ids[j] + "_id").hide();
            }
        }
    }

    function get_table() {
        $("#loader_id").show();
        $("#no_loader_id").hide();
        var url = 'http://'+ host +':'+ port_users + '/users';
        $.getJSON(url , function(data) {
            var tbl_body = "";
            var odd_even = false;
            $.each(data, function() {
                var tbl_row = "";
                var dict_aux = {};
                $.each(this, function(k , v) {
                    dict_aux[k] = v;
                    //tbl_row += "<td>"+v+"</td>"
                });
                var aux_user = dict_aux['user'];
                tbl_row += "<td><a class='user_id'>"+dict_aux['user']+"</a></td>"
                    + "<td id='"+aux_user+"_username'>"+dict_aux['username']+"</td>"
                    + "<td>"+dict_aux['role']+"</td>"
                    + "<td id='"+aux_user+"_option'>"+dict_aux['option']+"</td>"
                    + "<td>"+dict_aux['host']+"</td>"
                    + "<td>"+dict_aux['port']+"</td>";
                tbl_body += "<tr class=\""+( odd_even ? "odd" : "even")+"\">"+tbl_row+"</tr>";
                odd_even = !odd_even;
            });
            $("#target_table_id").find("tbody").html(tbl_body);
            $("#loader_id").hide();
            $("#no_loader_id").show();
        });
    }

    $('body').on('click', 'a.user_id', function(){
        user_detail = $(this)[0].text;
        var option_id = '#' + user_detail + '_option';
        var username_id = '#' + user_detail + '_username';
        username_detail = $(username_id).text();
        option_detail = $(option_id).text();
        $('#username_detail_id').text(username_detail);
        $('#select_multi_tenant_migrate').val(option_detail);
        show_hide("detail");
    });

    $("#title_arkis_id").click(function(){
        var url = 'http://' + host + ':' + port_login + '/login.html';
        window.location.replace(url);
    });
});