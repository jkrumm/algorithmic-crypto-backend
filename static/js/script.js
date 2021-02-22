(function () {
    var getUrlParameter = function getUrlParameter(sParam) {
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
    }

    console.log(getUrlParameter('symbol'))

    // var symbol = "BTCUSD"
    var symbol = getUrlParameter('symbol') === undefined ? "ETHUSD" : getUrlParameter('symbol')
    var interval = getUrlParameter('interval') === undefined ? 720 : getUrlParameter('interval')
    var action = getUrlParameter('action') === undefined ? "buy_sell" : getUrlParameter('action')
    var timespan = getUrlParameter('timespan') === undefined ? 0 : getUrlParameter('timespan')

    const changePath = () => {
        window.location.replace("/?symbol=" + symbol + "&interval=" + interval + "&action=" + action + "&timespan=" + timespan + "#signal_history");
    }

    $("#buy_sell").click(function () {
        action = "buy_sell"
        changePath();
    });
    $("#buy").click(function () {
        action = "buy"
        changePath();
    });
    $("#sell").click(function () {
        action = "sell"
        changePath();
    });

    $("#time_0").click(function () {
        timespan = 0
        changePath();
    });
    $("#time_1").click(function () {
        timespan = 365
        changePath();
    });
    $("#time_2").click(function () {
        timespan = 730
        changePath();
    });
    $("#time_5").click(function () {
        timespan = 1825
        changePath();
    });

    $("#BTCUSD_8H").click(function () {
        symbol = "BTCUSD"
        interval = 480
        changePath();
    });
    $("#BTCUSD_12H").click(function () {
        symbol = "BTCUSD"
        interval = 720
        changePath();
    });
    $("#BTCUSD_1D").click(function () {
        symbol = "BTCUSD"
        interval = 1
        changePath();
    });
    $("#ETHUSD_12H").click(function () {
        symbol = "ETHUSD"
        interval = 720
        changePath();
    });
    $("#ETHBTC_12H").click(function () {
        symbol = "ETHBTC"
        interval = 720
        changePath();
    });
    $("#LINKUSD_12H").click(function () {
        symbol = "LINKUSD"
        interval = 720
        changePath();
    });
    $("#LINKBTC_12H").click(function () {
        symbol = "LINKBTC"
        interval = 720
        changePath();
    });
    $("#XRPUSD_12H").click(function () {
        symbol = "XRPUSD"
        interval = 720
        changePath();
    });
    $("#LTCUSD_12H").click(function () {
        symbol = "LTCUSD"
        interval = 720
        changePath();
    });
    $("#ADAUSD_12H").click(function () {
        symbol = "ADAUSD"
        interval = 720
        changePath();
    });

}).call(this);
