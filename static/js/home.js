$(function () {
    var hero = $('#hero');
    var navbar = $('#navbar');
    var intro = $('#intro');
    var introNav = $('#intro-nav');
    var algorithms = $('#algorithms');
    var algorithmsNav = $('#algorithms-nav');
    var features = $('#features');
    var featuresNav = $('#features-nav');
    var pricing = $('#pricing');
    var pricingNav = $('#pricing-nav');
    var top = navbar.position().top;
    $(window).scroll(function () {
        var windowpos = $(window).scrollTop();
        console.log(windowpos)
        var introTop = intro.position().top + 935;
        var algorithmsTop = algorithms.position().top + 930;
        console.log(algorithmsTop)
        var featuresTop = features.position().top + 950;
        var pricingTop = pricing.position().top + 900;
        console.log(pricingTop)

        // if win >= navbar and not already a sticky
        if (windowpos >= top && !navbar.hasClass("navbar-fixed-top")) {
            hero.addClass("navbar-fixed-top");
            navbar.addClass("navbar-fixed-top");

            // if win <= navbar and is a sticky
        } else if (windowpos <= top && navbar.hasClass("navbar-fixed-top")) {
            hero.removeClass("navbar-fixed-top");
            navbar.removeClass("navbar-fixed-top");
        }

        if (introTop > windowpos) {
            introNav.removeClass('active');
            algorithmsNav.removeClass('active');
            featuresNav.removeClass('active');
            pricingNav.removeClass('active');
            return;
        }
        if (introTop < windowpos && windowpos < algorithmsTop) {
            introNav.addClass('active');
            algorithmsNav.removeClass('active');
            featuresNav.removeClass('active');
            pricingNav.removeClass('active');
            return;
        }
        if (algorithmsTop < windowpos && windowpos < featuresTop) {
            introNav.removeClass('active');
            algorithmsNav.addClass('active');
            featuresNav.removeClass('active');
            pricingNav.removeClass('active');
            return;
        }
        if (featuresTop < windowpos && windowpos < pricingTop) {
            introNav.removeClass('active');
            algorithmsNav.removeClass('active');
            featuresNav.addClass('active');
            pricingNav.removeClass('active');
            return;
        }
        if (pricingTop < windowpos) {
            introNav.removeClass('active');
            algorithmsNav.removeClass('active');
            featuresNav.removeClass('active');
            pricingNav.addClass('active');
        }
    });

    const slider = document.getElementById('slider');

    noUiSlider.create(slider, {
        start: 6,
        steps: 1,
        range: {
            'min': [3],
            'max': [24]
        }
    });


    const sliderValue = document.getElementById('slider-value');
    const sliderValuePrice = document.getElementById('slider-value-price');

    slider.noUiSlider.on('update', function (values) {
        let value = parseInt(values[0])
        sliderValue.innerHTML = value + " months";
        sliderValuePrice.innerHTML = 15 * value;
        if (value > 5) {
            sliderValuePrice.innerHTML = Math.ceil((15 * value * 0.9) / 5) * 5;
        }
    });

    $('.slick-responsive').slick({
        dots: false,
        accessibility: false,
        arrows: false,
        draggable: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 0,
        speed: 3500,
        cssEase: 'linear',
        infinite: true,
        focusOnSelect: false,
        pauseOnHover: false,
        pauseOnFocus: false,
        pauseOnDotsHover: false,
        touchMove: false,
        swipe: false,
        swipeToSlide: false,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
        ]
    });
});
