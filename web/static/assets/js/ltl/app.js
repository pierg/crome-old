$(document).ready(function () {

    $('.lazy').Lazy();

    //Preloader
    $(window).on('load', function () { // makes sure the whole site is loaded
        $('#status').fadeOut(); // will first fade out the loading animation
        $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
        $('body').delay(350).css({'overflow': 'visible'});
    });

    //Mobile menu toggle
    if ($('.navbar-burger').length) {
        $('.navbar-burger').on("click", function () {

            var menu_id = $(this).attr('data-target');
            $(this).toggleClass('is-active');
            $("#" + menu_id).toggleClass('is-active');
            $('.navbar.is-light').toggleClass('is-dark-mobile')
        });
    }

    //Animate left hamburger icon and open sidebar
    $('.menu-icon-trigger').click(function (e) {
        e.preventDefault();
        $('.menu-icon-wrapper').toggleClass('open');
        $('.sidebar').toggleClass('is-active');
    });

    //Close sidebar
    $('.sidebar-close').click(function () {
        $('.sidebar').removeClass('is-active');
        $('.menu-icon-wrapper').removeClass('open');
    })

    //Sidebar menu
    if ($('.sidebar').length) {
        $(".sidebar-menu > li.have-children a").on("click", function (i) {
            //i.preventDefault();
            if (!$(this).parent().hasClass("active")) {
                $(".sidebar-menu li ul").slideUp();
                $(this).next().slideToggle();
                $(".sidebar-menu li").removeClass("active");
                $(this).parent().addClass("active");
            } else {
                $(this).next().slideToggle();
                $(".sidebar-menu li").removeClass("active");
            }
        });
    }

    //Navbar Clone
    if ($('#navbar-clone').length) {
        $(window).scroll(function () {    // this will work when your window scrolled.
            var height = $(window).scrollTop();  //getting the scrolling height of window
            if (height > 50) {
                $("#navbar-clone").addClass('is-active');
            } else {
                $("#navbar-clone").removeClass('is-active');
            }
        });
    }

    //Init feather icons
    //feather.replace(); // wtf is this !?

    //reveal elements on scroll so animations trigger the right way
    var $window = $(window),
        win_height_padded = $window.height() * 1.1,
        isTouch = Modernizr.touch;

    $window.on('scroll', revealOnScroll);

    function revealOnScroll() {
        var scrolled = $window.scrollTop();
        $(".revealOnScroll:not(.animated)").each(function () {
            var $this = $(this),
                offsetTop = $this.offset().top;

            if (scrolled + win_height_padded > offsetTop) {
                if ($this.data('timeout')) {
                    window.setTimeout(function () {
                        $this.addClass('animated ' + $this.data('animation'));
                    }, parseInt($this.data('timeout'), 10));
                } else {
                    $this.addClass('animated ' + $this.data('animation'));
                }
            }
        });
    }

    // Back to Top button behaviour
    var pxShow = 600;
    var scrollSpeed = 500;
    $(window).scroll(function () {
        if ($(window).scrollTop() >= pxShow) {
            $("#backtotop").addClass('visible');
        } else {
            $("#backtotop").removeClass('visible');
        }
    });
    $('#backtotop a').on('click', function () {
        $('html, body').animate({
            scrollTop: 0
        }, scrollSpeed);
        return false;
    });

    //modals
    $('.modal-trigger').on('click', function () {
        var modalID = $(this).attr('data-modal');
        $('#' + modalID).addClass('is-active');
    })
    $('.modal-close, .close-modal').on('click', function () {
        $(this).closest('.modal').removeClass('is-active');
    })

    // Select all links with hashes
    $('a[href*="#"]')
    // Remove links that don't actually link to anything
        .not('[href="#"]')
        .not('[href="#0"]')
        .click(function (event) {
            // On-page links
            if (
                location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
                &&
                location.hostname == this.hostname
            ) {
                // Figure out element to scroll to
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                // Does a scroll target exist?
                if (target.length) {
                    // Only prevent default if animation is actually gonna happen
                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 550, function () {
                        // Callback after animation
                        // Must change focus!
                        var $target = $(target);
                        $target.focus();
                        if ($target.is(":focus")) { // Checking if the target was focused
                            return false;
                        } else {
                            $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                            $target.focus(); // Set focus again
                        }
                        ;
                    });
                }
            }
        });


    function animateCSS(element, animationName, callback) {
        const node = document.querySelector(element)
        node.classList.add('animated', animationName)

        function handleAnimationEnd() {
            node.classList.remove('animated', animationName)
            node.removeEventListener('animationend', handleAnimationEnd)

            if (typeof callback === 'function') callback()
        }

        node.addEventListener('animationend', handleAnimationEnd)
    }

    // ON CLICK EVENTS

    $("#insert_goals_button").on("click", function () {
        toggle_insert_goal_div()
    });


    $("#link_goals_button").on("click", function () {
        toggle_link_goals_div()
    });

    $("#console_button").on("click", function () {
        toggle_console_div()
    });

    // $("#load_example_dropdown").click(function () {
    //     alert($('#dropDownId').val());
    //     $("#textarea_insert_goals").load("static/assets/examples/platooning.txt");
    // });

    $('#load_example_dropdown').on('click', function (event) {
        if (event.target !== this) {
            file_name = $(event.target).attr("download");
            $("#textarea_insert_goals").load("static/assets/examples/" + file_name);
        }
    });

    function toggle_insert_goal_div() {
        $("#insert_goals_button").toggleClass("is-active");
        $("#insert_goals_div").toggle();
        $("#link_goals_div").hide();
        $("#link_goals_button").removeClass("is-active");
    }

    var_link_toggled = false;

    function toggle_link_goals_div() {
        $("#link_goals_button").toggleClass("is-active");
        $("#link_goals_div").toggle();
        $("#insert_goals_div").hide();
        $("#insert_goals_button").removeClass("is-active");
    }

    function toggle_console_div() {
        $("#console_div").toggle();
    }


    function show_goals(goals_json, ops_json, edges_json) {

        $('#goal_list_linking_checkbox').empty();

        $('#options_of_goals').empty();

        $('#options_of_goals_1').empty();

        $('#options_of_goals_2').empty();

        $('#goal_list').empty();

        var modal_goal_list = $.trim($('#modal_goal').html());
        var goal_list = $.trim($('#goal').html());
        var goal_list_checkbox = $.trim($('#goal_checkbox').html());
        var options_of_goals_template = $.trim($('#options_of_goals_template').html());
        var options_of_goals_1_template = $.trim($('#options_of_goals_1_template').html());
        var options_of_goals_2_template = $.trim($('#options_of_goals_2_template').html());


        nodes = [];

        edges = [];

        $.each(JSON.parse(goals_json), function (index, obj) {

            var cas = [];
            var cgs = [];

            $.each(obj.contracts, function (i, c) {

                ca = c.assumptions.join(",<br>");
                cg = c.guarantees.join(",<br>");

                cas.push(ca);
                cgs.push(cg);

            });

            var assumptions = cas.join("<br><br>OR<br><br>");
            var guarantees = cgs.join("<br><br>AND<br><br>");

            var checkbox = goal_list_checkbox.replace("__NAME__", obj.name);
            checkbox = checkbox.replace("__GOAL_ID__", obj.name);

            var options = options_of_goals_template.replace("__NAME__", obj.name);
            options = options.replace("__GOAL_ID__", obj.name);

            var x = goal_list.replace("__NAME__", obj.name);
            x = x.replace("__DESCRIPTION__", obj.description);
            x = x.replace("__CONTRACTS", JSON.stringify(obj.contracts, null, '\t'));

            x = x.replace("__EDIT_ID_BTN__", obj.name + "_e_btn");
            x = x.replace("__EDIT_ID_CTN__", obj.name + "_e_ctn");

            var y = modal_goal_list.replace("__NAME__", obj.name);
            y = y.replace("__DESCRIPTION__", obj.description);
            y = y.replace("__ASSUMPTIONS__", assumptions);
            y = y.replace("__GUARANTEES__", guarantees);
            y = y.replace("__GOAL_ID__", obj.name);

            $('#goal_list').append(x);
            $('#modal_goal_list').append(y);


            $('#goal_list_linking_checkbox').append(checkbox);

            $('#options_of_goals').append(options);

            $('#options_of_goals_1').append(options);
            $('#options_of_goals_2').append(options);


            $("#" + obj.name + "_e_btn").click(function () {
                $("#" + obj.name + "_e_ctn").addClass("is-active");
            });

            nodes.push(
                {
                    data: {
                        type: "goal",
                        id: obj.name,
                        description: obj.description,
                        assumptions: obj.assumptions,
                        guarantees: obj.guarantees
                    }
                }
            )

        });

        $.each(JSON.parse(ops_json), function (index, obj) {

            nodes.push(
                {
                    data: {
                        id: obj.id,
                        type: obj.type
                    }
                }
            )

        });

        $.each(JSON.parse(edges_json), function (index, obj) {

            edges.push(
                {
                    data: {
                        source: obj.source,
                        target: obj.target,
                        type: obj.type
                    }
                }
            )

        });


        $(".modal-close").click(function () {
            $(".modal").removeClass("is-active");
        });
        $(".modal-custom-close").click(function () {
            $(".modal").removeClass("is-active");
        });

        render_cgt(nodes, edges)

    }

    $('.refinement_element').hide();
    $('.mapping_element').hide();
    $('.comp_conj_element').hide();

    $(function () {
        $('input[type="radio"]').click(function () {
            if ($(this).is(':checked')) {
                if ($(this).val() == "composition") {
                    $('.comp_conj_element').show();
                    $('.refinement_element').hide();
                    $('.mapping_element').hide();
                }
                if ($(this).val() == "conjunction") {
                    $('.comp_conj_element').show();
                    $('.refinement_element').hide();
                    $('.mapping_element').hide();
                }
                if ($(this).val() == "refinement") {
                    $('.comp_conj_element').hide();
                    $('.refinement_element').show();
                    $('.mapping_element').hide();
                }
                if ($(this).val() == "mapping") {
                    $('.comp_conj_element').hide();
                    $('.refinement_element').hide();
                    $('.mapping_element').show();
                }
            }
        });
    });


    function c_notify(title, content, toast_type) {
        $.toast({
            heading: title,
            text: content,
            showHideTransition: 'slide',
            icon: toast_type
        });
    }


    function c_alert(type, content) {
        notie.confirm({
            type: 2,
            text: '<div class="title">' + type + '</div>' +
                '<div align="left" class="content is-family-monospace">' + content + '</div>',
            submitText: 'OK'
        })


    }


    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // // Event handler for new connections.
    socket.on('connect', function () {
        c_notify("Connected", "connected to the backend", "success");

        c_notify("Loading examples");

        socket.emit('cgt_example');

    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('notification', function (message) {
        c_notify(message["title"], message["content"], message["type"])
    });

    socket.on('alert', function (message) {
        c_alert(message["title"], message["content"])
    });

    socket.on('log', function (message) {
        $('#console_content').append('<br>' + $('<div/>').text(message.content).html());
    });

    socket.on('goal_list', function ([goals, ops, edges]) {
        show_goals(goals, ops, edges)
    });


    // Interval function that clustering message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function () {
        start_time = (new Date).getTime();
        socket.emit('my_ping');
    }, 1000);

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.
    socket.on('my_pong', function () {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

    $('#insert_goals_text_button').click(function (event) {
        socket.emit('goals_text', {data: $('#textarea_insert_goals').val()});
        toggle_insert_goal_div();
    });

    $('#submit_links_goals_button').click(function (event) {
        var msg = {};
        var op_sel = $('input[name=cgt_operation_radio]:checked', '#radio_operations').val();

        if (op_sel === "composition") {
            msg["operation"] = "composition";

            event.preventDefault();
            var goals_list = $("#goal_list_linking_checkbox input:checkbox:checked").map(function () {
                return $(this).val();
            }).get();

            msg["goals"] = goals_list;
            msg["name"] = $('#new_goal_name').val();
            msg["description"] = $('#new_goal_description').val();

        }
        if (op_sel === "conjunction") {
            msg["operation"] = "conjunction";

            event.preventDefault();
            var goals_list = $("#goal_list_linking_checkbox input:checkbox:checked").map(function () {
                return $(this).val();
            }).get();

            msg["goals"] = goals_list;
            msg["name"] = $('#new_goal_name').val();
            msg["description"] = $('#new_goal_description').val();
        }
        if (op_sel === "refinement") {
            msg["operation"] = "refinement";
            msg["abstract"] = $("#options_of_goals_1").val();
            msg["refined"] = $("#options_of_goals_2").val();
        }
        if (op_sel === "mapping") {
            msg["operation"] = "mapping";
            msg["goal"] = $("#options_of_goals").val();
            msg["library"] = $("#library_select").val();
        }
        socket.emit('goals_link', msg);
        toggle_link_goals_div();
    });

});



