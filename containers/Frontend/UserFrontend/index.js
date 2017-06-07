$(document).ready(function(){
    var host = document.location.hostname;
    var port_documents = 31999;
    var port_users = 30001;
    var port_search = 30004;
    var port_login = 32000;

    var parameters = location.search.substring(1).split("&");
    var temp1 = parameters[0].split("=");
    var temp2 = parameters[1].split("=");
    var temp3 = parameters[2].split("=");

    var user = 0;
    try {
        user = parseInt(temp1[1]);
    } catch(exception) {
        user = 0;
    }
    var option = temp2[1];
    var username = temp3[1];

    $("#new_blob").hide();
    $("#new_blob_doc").hide();
    show_hide("info");
    get_users1();
    get_option1();
    get_last_document();

    var array_json_to_table = function(url) {
        $("#target_table_id").show();
        $("#new_blob").hide();
        $("#loader_id").show();
        $("#no_loader_id").hide();
        $.getJSON(url , function(data) {
            var tbl_body = "";
            var odd_even = false;
            $.each(data, function() {
                var tbl_row = "";
                $.each(this, function(k , v) {
                    if (k == 'ZBlob') {
                        v = v.substring(1,100);
                    }
                    if (k != 'score') {
                        tbl_row += "<td>"+v+"</td>";
                    }
                    if ((1 == 0) && (k == 'ZRowIdent')) {
                        tbl_row += "<td><button class='update_button'>"+v+"</button></td>";
                        tbl_row += "<td><button class='delete_button'>"+v+"</button></td>";
                    }
                });
                tbl_body += "<tr class=\""+( odd_even ? "odd" : "even")+"\">"+tbl_row+"</tr>";
                odd_even = !odd_even;
            });
            $("#target_table_id tbody").html(tbl_body);
            $("#loader_id").hide();
            $("#no_loader_id").show();
        });
    };

    function array_json_to_list(url) {
        $.get(url, function(data){
        }).done(function( data ) {
            for (var i = 0; i < data.length; i++) {
                var other_id = data[i].other_id;
                var name = data[i].name;
                $("#list_document_id").append('<li class="doc_other_id_li" >'+name+'<a class="doc_other_id">'
                    +other_id+'</a></li>');
            }
        });
    }

    $("#button_search_id").click(function(){
            var url = 'http://'+host+':'+port_documents+'/blobs/search/' +  user + '/' + option +'/'  +  $("#text_search_id").val();
            array_json_to_table(url);
        });

    $("#button_search_id_doc").click(function(){
        get_by_search_document();
    });

    $("#button_new_id").click(function(){
            $("#new_blob").show();
            $("#target_table_id").hide();
    });

    $("#button_new_id_doc").click(function(){
        $("#new_blob_doc").show();
        $("#document_id").hide();
    });

    $("#button_back_id_doc").click(function(){
        $("#new_blob_doc").hide();
        $("#document_id").show();
        $("#one_doc").show();
        $("#list_doc").hide();
        get_last_document();
    });

    $("#button_all_id").click(function(){
            var url = 'http://'+host+':'+port_documents+'/blobs' + '/' + user + '/' + option;
            array_json_to_table(url);
        });

    $("#button_all_id_doc").click(function(){
        var lim = $("#text_limit_id_doc").val();
        if (lim){
        } else {
            lim = "nolimit";
        }
        var url = 'http://'+host+':'+port_documents+'/documents' + '/' + user + '/' + option + '/lim/' + lim;
        $("#one_doc").hide();
        $("#list_doc").show();
        array_json_to_list(url);
    });

    $("#button_delete_id").click(function(){
            var url1 = 'http://'+host+':'+port_documents+'/delete' + '/' + user + '/' + option +'/'   + $("#text_search_id").val();
            $.get(url1, function(data){
                var url = 'http://'+host+':'+port_documents+'/blobs' + '/' + user + '/' + option;
                array_json_to_table(url);
            });
        });

    $("#button_delete_id_doc").click(function(){
        var url1 = 'http://'+host+':'+port_documents+'/delete/documents' + '/' + user + '/' + option +'/'   + $("#text_delete_id_doc").val();
        $.get(url1, function(data){}).done(function( data ) {
            try {
                alert(data[0]['res']);
            } catch(exception) {
                alert(data[0]['error']);
            }
            get_last_document();
        });
    });

    $("#button_update_id").click(function(){
            var url1 = 'http://'+host+':'+port_documents+'/put' + '/' + user + '/' + option +'/'  + $("#text_search_id").val();
            var blob1 =  $("#text_blob").val();
            var domain1 =  $("#text_domain").val();
            var filename1 =  $("#text_filename").val();
            var nodeid1 =  $("#text_nodeid").val();
            var extension1 =  $("#text_extension").val();
            $.post(url1, { blob: blob1, domain: domain1, filename: filename1, nodeid: nodeid1, extension: extension1 })
            .done(function(data){
                var url1 = 'http://'+host+':'+port_documents+'/blobs/' + user + '/' + option;
                array_json_to_table(url1);
            });
         });

    $("#button_update_id_doc").click(function(){
        var other_id = $("#text_other_id_doc").val();
        var url = 'http://'+host+':'+port_documents + '/put/documents' + '/' + user + '/' + option + '/' + other_id;
        var blob1 =  $("#text_blob_doc").val();
        var number1 =  $("#text_number_doc").val();
        var name =  $("#text_name_doc").val();
        var title =  $("#text_title_doc").val();

        $.post( url, { blob: blob1, number: number1, name: name, title: title})
            .done(function( data ) {
                get_last_document();
                $("#new_blob_doc").hide();
                $("#document_id").show();
            });
    });

    $("#button_create_id").click(function(){
            var url = 'http://'+host+':'+port_documents + '/blobs' + '/' + user + '/' + option;
            var blob1 =  $("#text_blob").val();
            var domain1 =  $("#text_domain").val();
            var filename1 =  $("#text_filename").val();
            var nodeid1 =  $("#text_nodeid").val();
            var extension1 =  $("#text_extension").val();
            $.post( url, { blob: blob1, domain: domain1, filename: filename1, nodeid: nodeid1, extension: extension1 })
            .done(function( data ) {
                var url1 = 'http://'+host+':'+port_documents + '/blobs' + '/' + user + '/' + option;
                array_json_to_table(url1);
            });
        });

    $("#button_create_id_doc").click(function(){
        var url = 'http://'+host+':'+port_documents + '/documents' + '/' + user + '/' + option;
        var blob1 =  $("#text_blob_doc").val();
        var number1 =  $("#text_number_doc").val();
        var name =  $("#text_name_doc").val();
        var title =  $("#text_title_doc").val();
        $.post( url, { blob: blob1, number: number1, name: name, title: title})
            .done(function( data ) {
                get_last_document();
                $("#new_blob_doc").hide();
                $("#document_id").show();
            });
    });

    $("#button_host_db_id").click(function(){
            var host_db = $("#text_host_db_id").val();
            var port_db = $("#text_port_db_id").val();
            var url1 = 'http://'+host+':'+port_documents+'/blobs/host/' + host_db;
            $.get(url1, function(data){
            });
            var url1 = 'http://'+host+':'+port_documents+'/blobs/port/' + port_db;
            $.get(url1, function(data){
            });
        });

    $("#button_cyclops_id").click(function(){
            var rcb = $("#text_cyclops_id").val();
            var url1 = 'http://'+host+':'+port_documents+'/blobs/rcb/' + rcb;
            $.get(url1, function(data){
            });
        });

    $("#button_migrate").click(function(){
            $("#loader_id").show();
            $("#no_loader_id").hide();
            var option1 = $( "#select_multi_tenant1" ).val();
            var m = option + option1;
            var url1 = 'http://192.168.99.100:31000/migrate/'+m+'/' + user;
            $.get(url1, function(){}).always(function() {
            var url2 = 'http://'+host+':'+port_documents+'/option/' + user;
            $.get(url2, function(data){
            }).done(function( data ) {
                option = data['option'];
                $("#select_multi_tenant").val(option);
                $("#migration_label").text('Migrate from ' + option + ' to: ');
                    var url3 = 'http://'+host+':'+port_documents + '/blobs' + '/' + user + '/' + option;
                    array_json_to_table(url3);
                });
            });
        });

    $("#button_BA").click(function(){
            var url1 = 'http://192.168.99.100:31000/migrate/BA/' + user;
            $.get(url1, function(data){
            }).done(function( data ) {
                var url1 = 'http://'+host+':'+port_documents + '/blobs' + '/' + user + '/A';
                array_json_to_table(url1);
            });
        });

    $("#button_host_b_id").click(function(){
            host = $('#text_host_b_id').val();
            port_documents = $("#text_port_b_id").val();
        });

    $("#select_user").change(function() {
            user = $("#select_user").val().substring(5);
            get_option();
            get_last_document();
            /*$("#select_multi_tenant").val('E');
            $("#migration_label").text('Migrate from (Loading) to: ');
            var url1 = 'http://'+host+':'+port_documents+'/option/' + user;
            $.get(url1, function(data){
            }).done(function( data ) {
                option = data['option'];
                $("#select_multi_tenant").val(option);
                $("#migration_label").text('Migrate from ' + option + ' to: ');
                $("#loader_id").hide();
                $("#no_loader_id").show();
            });*/
        });

    $("#select_multi_tenant").change(function(){
            option = $( "#select_multi_tenant" ).val();
        });

    $("#conf_l").click(function(){
            show_hide("conf");
        });

    $("#migration_l").click(function(){
            show_hide("migration");
        });

    $("#blob_l").click(function(){
            show_hide("blob");
        });

    $("#info_l").click(function(){
            show_hide("info");
        });

    $("#user_l").click(function(){
            show_hide("user");
        });

    $("#data_l").click(function(){
            show_hide("data");
    });

    $("#documents_l").click(function(){
            show_hide("documents");
            get_last_document();
    });

    $("#button_get_id_doc").click(function(){
        show_hide("documents");
        var other_id =  $("#text_id_doc").val();
        get_by_id_document(other_id);

    });

    $('body').on('click', 'a.doc_other_id', function(){
        show_hide("documents");
        var other_id = $(this)[0].text;
        get_by_id_document(other_id);
        $( 'a.doc_other_id' ).remove();
        $( 'li.doc_other_id_li' ).remove();
        $("#list_doc").hide();
        $("#one_doc").show();

    });

    function get_users(){
        var aux_max = 5;
        var url1 = 'http://' + host+':'+port_users+'/len';
        //var url1 = 'http://104.198.249.229:30001/len';
        $("#loader_id").show();
        $("#no_loader_id").hide();
        $.get(url1, function(data){
            aux_max = data['len'];
            for (var i = 0; i < aux_max; i++){
                $("#select_user").append('<option id="user_'+i+'" value="'+ i + '">User '+i+'</option>');
            }

        }).done(function() {
            $("#select_user").val(user);
            $("#loader_id").hide();
            $("#no_loader_id").show();
        });
    }

    function get_users1(){
        $("#select_user").append('<option id="user_'+user+'" value="'+ user+ '">'+username+'</option>');
        $("#select_user").val(user);
        $("#loader_id").hide();
        $("#no_loader_id").show();
    }

    function get_option(){
        $("#loader_id").show();
        $("#no_loader_id").hide();
        var url1 = 'http://' + host +':'+port_users + '/users/' + user +'/option';
        //var url1 = 'http://104.198.249.229:30001/users/' + user +'/option';
        $.get(url1, function(data){
        }).done(function( data ) {
            option = data['option'];
            $("#select_multi_tenant").val(option);
            $("#migration_label").text('Migrate from ' + option + ' to: ');
            $("#loader_id").hide();
            $("#no_loader_id").show();
        });
    }

    function get_option1(){
        $("#select_multi_tenant").val(option);
    }

    function get_last_document(){
        var url1 = 'http://' + host+':'+port_documents+'/documents/'+ user +'/' + option + '/last';
        $.get(url1, function(data){
        }).done(function( data ) {
            try  {
                $("#document_other_id").text("Last document added");
                $("#document_title_id").text(data['title']);
                $("#document_blob_id").text(data['blob']);
            } catch(exception) {
                $("#document_other_id").text("No found");
                $("#document_title_id").text("");
                $("#document_blob_id").text("");
            }
        });
    }

    function get_by_id_document(other_id){
        var url1 = 'http://' + host+':'+port_documents+'/documents/'+ user +'/' + option + '/' + other_id;
        $.get(url1, function(data){
        }).done(function( data ) {
            try  {
                $("#document_other_id").text("Id: " + data['other_id']);
                $("#document_title_id").text(data['title']);
                $("#document_blob_id").text(data['blob']);
            } catch(exception) {
                $("#document_other_id").text("No found");
                $("#document_title_id").text("");
                $("#document_blob_id").text("");
            }
        });
    }

    function get_by_search_document(){
        var url1 = 'http://'+host+':' + port_search + '/documents/search' + '/' + user + '/' + option +'/'
            + $("#text_search_id_doc").val();
        $.get(url1, function(data){
        }).done(function( data ) {
            try {
                $("#document_other_id").text("Id: " + data['other_id']);
                $("#document_title_id").text(data['title']);
                $("#document_blob_id").text(data['blob']);
            } catch(exception) {
                $("#document_other_id").text("No found");
                $("#document_title_id").text("");
                $("#document_blob_id").text("");
            }
        });
    }

    function show_hide(id){
        var ids = ["documents","info","conf","migration","blob", "user", "data"];
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

    $("#title_arkis_id").click(function(){
        var url = 'http://' + host + ':' + port_login + '/login.html';
        window.location.replace(url);
    });
});