$(function () {
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
        cssEase:'linear',
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
