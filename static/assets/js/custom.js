$(document).ready(function() {
    // Initialize owl
    localStorage.clear()
    localStorage.setItem('first', false);

    if ($.isFunction('owlCarousel')) {
        $('.owl-carousel').owlCarousel({
            items: 3,
            // loop: true,
            dots: true,
            nav: true,
            autoplay: false,
            margin: 30,
            mouseDrag: false,
            responsive: {
                0: {
                    items: 1,
                    nav: false,
                    autoHeight: true
                },
                600: {
                    items: 2,
                },
                1000: {
                    items: 3,
                }
            }
        });
    }

    // if section provided for menu page, scroll to that section
    var menu_section = getUrlParameter('section');
    if (menu_section) {
        var section = $('.menu-section[section="' + menu_section + '"]');
        if (section.length) {
            var offset = (parseInt($('body').attr('spacer')) * 1);

            var mobile_offset = 0;
            if ($('body').width() <= 900) {
                mobile_offset = offset * 4;
            }

            $('html, body').animate({
                scrollTop: section.offset().top - offset - mobile_offset
            }, {
                duration: 500,
                complete: function() {
                    animateCSS(section, 'pulse');
                },
            });
        }
    }
    if ($.isFunction('owlCarousel')) {

        // Initialize gallery
        $('.section-gallery').owlCarousel({
            items: 2,
            dots: false,
            margin: 15,
            loop: true,
            responsive: {
                // breakpoint from 0 up
                0: {
                    items: 1,
                },
                // breakpoint from 768 up
                900: {
                    items: 2,
                }
            }
        });
    }

    // change gallery slider
    $(document).on('click', '.section-album .change-slide', function(e) {
        e.preventDefault();

        var trigger = $(this);
        var owl = trigger.parent().find('.section-gallery');

        owl.owlCarousel();

        if (trigger.hasClass('next')) {
            owl.trigger('next.owl.carousel');
        } else {
            owl.trigger('prev.owl.carousel');
        }
    });

    // change main slider
    $(document).on('click', '.intro-slider-wrapper .change-slide', function(e) {
        e.preventDefault();

        var owl = $('.intro-slider');

        owl.owlCarousel();

        owl.trigger('stop.owl.autoplay');
        if ($(this).hasClass('next')) {
            owl.trigger('next.owl.carousel', [1000]);
        } else {
            owl.trigger('prev.owl.carousel', [1000]);
        }
        owl.trigger('play.owl.autoplay');
    });

    // menu navigation
    $(document).on('click', '.menu-nav a', function(e) {
        e.preventDefault();

        var section = $('.menu-section[section="' + $(this).attr('section') + '"]');
        var offset = parseInt($('body').attr('spacer'));

        var mobile_offset = 0;
        if ($('body').width() <= 900) {
            mobile_offset = offset * 4;
        }

        $('html, body').animate({
            scrollTop: section.offset().top - offset - mobile_offset
        }, {
            duration: 500,
            complete: function() {
                animateCSS(section, 'shake');
            },
        });
    });

    // site navigation toggle
    $(document).on('click', '.mobile-menu-toggle', function(e) {
        e.preventDefault();

        var menu = $('.sidebar');

        menu.toggleClass('active');
    });
});

function animateCSS(element, animationName, callback) {
    const node = element[0];
    node.classList.add('animated', animationName)

    function handleAnimationEnd() {
        node.classList.remove('animated', animationName)
        node.removeEventListener('animationend', handleAnimationEnd)

        if (typeof callback === 'function') callback()
    }

    node.addEventListener('animationend', handleAnimationEnd)
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};

function changeUser(name, image, id) {
    let data = localStorage.getItem('first');
    if ($(`#${id}`).hasClass('black')) {
        return true
    }
    if (data === 'true') {
        if (localStorage.getItem('user1') == id) {
            return true
        }
        if (localStorage.getItem('user2')) {
            document.getElementById(localStorage.getItem('user2')).classList.replace('black', 'char-img')
            localStorage.setItem('user2', id)
        } else {
            localStorage.setItem('user2', id)
        }
        document.getElementById('nameUser2').innerText = name
        document.getElementById('user2').style.backgroundImage = `url(${image})`
        document.getElementById(id).classList.replace('char-img', 'black')
    }
    if (data === 'false') {
        if (localStorage.getItem('user1')) {
            document.getElementById(localStorage.getItem('user1')).classList.replace('black', 'char-img')
            localStorage.setItem('user1', id)
        } else {
            localStorage.setItem('user1', id)
        }
        document.getElementById('nameUser').innerText = name
        document.getElementById('user1').style.backgroundImage = `url(${image})`
        document.getElementById(id).classList.replace('char-img', 'black')
    }
}

function change() {
    document.getElementById('selection').innerText = 'Sélectionner le joueur 2'
    document.getElementById('validate1').style.opacity = 0;
    document.getElementById('validate2').style.opacity = 1;
    document.getElementById(`button${localStorage.getItem('user1')}`).innerText = 'Joueur 1'
    document.getElementById(`button${localStorage.getItem('user1')}`).style.opacity = 1;

    localStorage.setItem('first', true);
}

function goToNext() {
    let user1 = localStorage.getItem('user1');
    let user2 = localStorage.getItem('user2');
    location.href = `/choice_cat/${user1}/${user2}/`
}