/*
Store all Javascript functions for the member area here
*/

/*
Ready Function:

Make all images clickable
Check if user has accepted the privacy policy
*/
cookieCheck = false;
currentPage = 0;
TICKER_AMOUNT_CURRENCIES = 30;
var node_list = [];
var market_ticker_node_list = [];

$(document).ready(function () {

});

function run_on_load(){
    //if (cookieCheck)
    //    privacyPolicy();

    $(window).on('load', function() {
        $('.toast').toast({ 'autohide': false } );
        $('.toast').toast('show');

        setTimeout(function () {

        }, 2000);
    });

    //update_masonry();
};

function update_currency_values() {
    $('.content-list-block-tw').each(function(){
        var cp_id = $(this).find('.cp_id').first()[0].innerHTML;
        var current_value_container = $(this).find('.current_value span');
        var ath_container = $(this).find('.ath span');
        var atl_container = $(this).find('.atl span');
        var market_cap_container = $(this).find('.market_cap p');
        var _24h_volume_container = $(this).find('.24h_volume p');
        var circ_supply_container = $(this).find('.circ_supply p');
        var _24h_change_container = $(this).find('.24h_change p')
        var _7d_change_container = $(this).find('.7d_change p');
        var ranking_container = $(this).find('.rank_container');

        // Market Info
        //var get_url = get_api_url('get_crypto_currency_market_quotes?id=' + cmc_id);
        var get_url = 'https://api.coinpaprika.com/v1/ticker/' + cp_id;

        $.getJSON(get_url, function(data) {
            if (data.price_usd > 1)
                current_value_container.html('$ ' + parseFloat(data.price_usd).toFixed(2));
            else
                current_value_container.html('$ ' + parseFloat(data.price_usd).toFixed(5));
            market_cap_container.html('$ ' + abbreviateNumber(data.market_cap_usd));
            circ_supply_container.html(data.circulating_supply);
            _24h_volume_container.html(abbreviateNumber(data.volume_24h_usd));
            ranking_container.html(data.rank);
            if (data.percent_change_24h >= 0) {
                _24h_change_container.html("<span class='text-success'>+" + data.percent_change_24h + " %</span>")
            } else {
                _24h_change_container.html("<span class='text-danger'>" + data.percent_change_24h + " %</span>")
            }
            if (data.percent_change_7d >= 0) {
                _7d_change_container.html("<span class='text-success'>+" + data.percent_change_7d + " %</span>")
            } else {
                _7d_change_container.html("<span class='text-danger'>" + data.percent_change_7d + " %</span>")
            }
        });


     });
}

function get_currency_info() {
    $('.content-list-block-tw').each(function(){
        // Currency Info
        var cp_id = $(this).find('.cp_id').first()[0].innerHTML;
        var title_container = $(this).find('#token-name');
        var description_container = $(this).find('.tw-description');
        var token_image_container = $(this).find('.tw-image img').first();
        var link_container = $(this).find('.tw-links').first();

        /*if (window.location.hostname == '127.0.0.1')
            var get_url = window.location.protocol + '//' + window.location.hostname + ':8000/member/api/get_crypto_currency_info?id=' + cmc_id;
        else
            var get_url = window.location.protocol + '//' + window.location.hostname + '/member/api/get_crypto_currency_info?id=' + cmc_id;*/

        //var get_url = get_api_url('get_crypto_currency_info?id=' + cmc_id);
        var get_url = 'https://api.coinpaprika.com/v1/coins/' + cp_id;

        $.getJSON(get_url, function(data) {
            //token_image_container.attr('src', data.logo);
            title_container.html(data.symbol);
            description_container.html(data.description);

            var links = '<div class="row">';

            if (data.links_extended.length > 0) {
                for (var i = 0; i < data.links_extended.length; i++) {
                    var add = true;
                    var link_type = '';
                    switch (data.links_extended[i].type) {
                        case 'reddit':
                            link_type = 'Reddit:';
                            break;
                        case 'explorer':
                            link_type = 'Blockchain Explorer:';
                            break;
                        case 'source_code':
                            link_type = 'Source Code:';
                            break;
                        case 'website':
                            link_type = 'Website:';
                            break;
                        case 'blog':
                            link_type = 'Blog:';
                            break;
                        case 'facebook':
                            link_type = 'Facebook:';
                            break;
                        case 'message_board':
                            link_type = 'Message Board:';
                            break;
                        case 'twitter':
                            link_type = 'Twitter:';
                            break;
                        case 'wallet':
                            link_type = 'Wallet:';
                            break;
                        case 'youtube':
                            link_type = 'YouTube:';
                            break;
                        case 'announcement':
                            link_type = 'Announcement';
                            break;
                        case 'discord':
                            link_type = 'Discord';
                            break;
                        case 'slack':
                            link_type = 'Slack';
                            break;
                        case 'telegram':
                            link_type = 'Telegram';
                            break;
                        case 'chat':
                            link_type += 'Chat';
                            break;
                        default:
                            add = false;
                            break;
                    }

                    if (add) {
                        links += '<div class="col-3"><p><b>' + link_type + '</b>';
                        links += '<br><a target="_blank" href="' + data.links_extended[i].url + '">' + data.links_extended[i].url + '</a>';

                        links += '</p></div><br>';
                    }
                }
            }
            link_container.append(links + '</div>')
        });
    });
}

var SI_SYMBOL = ["", "k", "M", "B", "T", "P", "E"];

function abbreviateNumber(number){

    // what tier? (determines SI symbol)
    var tier = Math.log10(number) / 3 | 0;

    // if zero, we don't need a suffix
    if(tier == 0) return number;

    // get suffix and determine scale
    var suffix = SI_SYMBOL[tier];
    var scale = Math.pow(10, tier * 3);

    // scale the number
    var scaled = number / scale;

    // format number and add suffix
    return scaled.toFixed(1) + suffix;
}

function update_masonry() {
    $('.grid').masonry({
        // set itemSelector so .grid-sizer is not used in layout
        itemSelector: '.grid-item',
        // use element for option
        columnWidth: '.grid-sizer',
        percentPosition: true
    });
}

function makeImagesClickable() {
    $('.clickable-img img').click(function () {
        window.open($(this).attr('src'), '_blank', 'status=0,location=0,menubar=0,toolbar=0');
    });
}

function privacyPolicy() {
    var cookieConsent = getCookie("cookieconsent");
    if (!cookieConsent) {
        $('#cookieConsentModal').modal('show');
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function calendar_dashboard(days_current_month, current_day, current_month_name) {
    var daylist = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var d = new Date();
    d.setDate(current_day);
    var curr_day = daylist[d.getDay()];

    var get_url = get_api_url('dashboard_events');

    $.getJSON(get_url, function(data) {
        for (var i = 0; i < days_current_month; i++) {
            /*
                Creating Table with Days
            */
            if (i % 7 == 0) {
                currentrow = document.createElement('tr');
            }
            var node = document.createElement('td');
            var node_a = document.createElement('a');
            if ((i+1) == current_day)
                node_a.className = 'dashboard-calendar-td font-weight-bold active';
            else
                node_a.className = 'dashboard-calendar-td font-weight-bold';
            node_a.id = 'event-' + (i+1) + '-tab';
            node_a.setAttribute('data-toggle', 'tab');
            node_a.setAttribute('href', '#event-' + (i+1));
            node_a.setAttribute('aria-controls', 'event-' + (i+1));
            node_a.setAttribute('aria-selected', 'false');
            var textnode = document.createTextNode(i+1);
            node_a.appendChild(textnode);

            node.appendChild(node_a);
            $(node_a).click(function(e){
                e.preventDefault();
                $('.dashboard-calendar-td').removeClass('active');
            });
            currentrow.appendChild(node);
            if (i % 7 == 0) {
                $('#dashboard-calendar').append(currentrow);
            }

            /*
                Creating Tab Panes for event info
            */
            var node = document.createElement('div');
            node.id = 'event-' + (i+1);
            node.setAttribute('role', 'tabpanel');
            node.setAttribute('aria-labelledby', 'event-' + (i+1) + '-tab');
            if ((i+1) == current_day)
                node.className = 'tab-pane fade event-info show active';
            else
                node.className = 'tab-pane fade event-info';
            var title_bar = document.createElement('div')
            title_bar.innerHTML = '<h3 class="title-font-size event-date">' + curr_day + ", " + current_month_name + ' ' + (i+1) + '</h3>';
            title_bar.innerHTML += '<div class="bg-secondary text-center mt-2 mb-2 p-1 font-weight-bold">Events</div>';
            node.append(title_bar);

            var text = '';
            for (var j = 0; j < data.length; j++) {
                if (data[j].day == (i+1)) {
                    /// event type === coin event: color-brown-background, location...: color-blue-background, provisn: color-green-background
                    text += '<div class="one-event"><div class="event-border-left ' + data[j].color_class + '"></div><div class="pb-3"><a target="_blank" href="' + data[j].event_url + '"><h5>' + data[j].title + '</h5></a>';
                    text += '<p>' + data[j].text + '</p>';
                    // text += '<span>' + data[j].date_of_event + '</span><br/>';
                    text += '<span>' + data[j].location + '</span>';
                    text += '</div></div>';
                }
            }
            var textnode = document.createElement('div');

            textnode.innerHTML = text;
            textnode.className = 'event-details';
            node.appendChild(textnode);
            $('#dashboard-events-info').append(node);
        }
    });

}

function get_dashboard_events() {
    var get_url = get_api_url('dashboard_events');
    $.getJSON(get_url, function(data) {
        return data;
    });
}

function handle_payment_page() {
    let params = new URLSearchParams(location.search);
    var order_id = params.get('order_id');

    var get_url = get_api_url('payment_status?order_id='+order_id);

    $.getJSON(get_url, function(data) {
        var status = '';
        if (data.status == 'created') {
            status = '<span class="text-warning">Awaiting Payment</span>';
        } else if (data.status == 'done') {
            status = '<span class="text-success">Completed</span>';
        } else if (data.status == 'pending') {
            status = '<span class="text-success">Payment pending...</span>';
        } else if (data == 'Not Authorized!') {
            status = "<span class='text-danger'>Not authorized</span>";
        }
        if (data.payment_received) {
            status = "<span class='text-success'>Payment Received, awaiting confirmation!</span>";
        }
        $('#payment-address-field').text(data.address);
        $('#payment-amount').text(data.amount);
        $('#currency').text(data.currency.toUpperCase());
        $('#payment-status').html(status);
    });
}

function copyToClipboard(elem) {
    // create hidden text element, if it doesn't already exist
    var targetId = "_hiddenCopyText_";
    var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
    var origSelectionStart, origSelectionEnd;
    if (isInput) {
        // can just use the original source element for the selection and copy
        target = elem;
        origSelectionStart = elem.selectionStart;
        origSelectionEnd = elem.selectionEnd;
    } else {
        // must use a temporary form element for the selection and copy
        target = document.getElementById(targetId);
        if (!target) {
            var target = document.createElement("textarea");
            target.style.position = "absolute";
            target.style.left = "-9999px";
            target.style.top = "0";
            target.id = targetId;
            document.body.appendChild(target);
        }
        target.textContent = elem.textContent;
    }
    // select the content
    var currentFocus = document.activeElement;
    target.focus();
    target.setSelectionRange(0, target.value.length);

    // copy the selection
    var succeed;
    try {
        succeed = document.execCommand("copy");
    } catch(e) {
        succeed = false;
    }
    // restore original focus
    if (currentFocus && typeof currentFocus.focus === "function") {
        currentFocus.focus();
    }

    if (isInput) {
        // restore prior selection
        elem.setSelectionRange(origSelectionStart, origSelectionEnd);
    } else {
        // clear temporary content
        target.textContent = "";
    }
    return succeed;
}

function GetSortOrder() {
    return function(a, b) {
        if (a.quotes.USD.market_cap < b.quotes.USD.market_cap) {
            return 1;
        } else if (a.quotes.USD.market_cap > b.quotes.USD.market_cap) {
            return -1;
        }
        return 0;
    }
}

function create_market_overview(data) {
    node_list = [];
    var market_view_table = $('#market-view-table');
    var flagOfOdd = true;
    for (var i = 0; i < 100; i++) {
        var node = document.createElement('tr');
        var coin_name = document.createElement('td');
        var market_cap = document.createElement('td');
        var value_container = document.createElement('td');
        var _7d_container = document.createElement('td');
        var _24h_container = document.createElement('td');
        var value_graph = document.createElement('td');

        var graph = document.createElement('img');
        $(graph).attr('src', 'https://graphs2.coinpaprika.com/currency/chart/' + data[i].id + '/7d/chart.svg');
        $(graph).attr('style', 'float: right; margin-right: 20px;');
        value_graph.append(graph);
        iconHTML = '<img src="https://raw.githubusercontent.com/atomiclabs/cryptocurrency-icons/master/32%402x/color/' + data[i].symbol.toLowerCase() + '%402x.png" class="cryptocurrency-icons">';

        coin_name.innerHTML = '<span style="margin-right: 10px"> ' + (i+1) + '</span>' + iconHTML + data[i].name;
        coin_name.className = 'market-view-coin-name'
        market_cap.innerHTML = abbreviateNumber(data[i].quotes.USD.market_cap.toFixed(2));
        market_cap.className = 'market-view-cap text-left'
        _7d_container.innerHTML = (data[i].quotes.USD.percent_change_7d.toFixed(2)) + ' %';
        _24h_container.innerHTML = (data[i].quotes.USD.percent_change_24h.toFixed(2)) + ' %';

        node.style.cssText = 'height:2rem;';
        if (!flagOfOdd)
            node.style.cssText = 'background-color: #202020';
        flagOfOdd = !flagOfOdd;

        node.className = 'market-view'
        value_container.className = 'market-view-value text-left'

        if (data[i].quotes.USD.price > 1) {
            value_container.innerHTML = (data[i].quotes.USD.price.toFixed(2) + ' $');
        } else {
            value_container.innerHTML = (data[i].quotes.USD.price.toFixed(5) + ' $');
        }

        if (data[i].quotes.USD.percent_change_24h >= 0) {
            _24h_container.className = 'market-view-24h text-success text-left';
        } else {
            _24h_container.className = 'market-view-24h text-danger text-left';
        }
        if (data[i].quotes.USD.percent_change_7d >= 0) {
            _7d_container.className = 'market-view-7d text-success text-left';
        } else {
            _7d_container.className = 'market-view-7d text-danger text-left';
        }
        node.appendChild(coin_name);
        node.appendChild(value_graph);
        node.appendChild(value_container);
        node.appendChild(market_cap);
        node.appendChild(_24h_container);
        node.appendChild(_7d_container);
        market_view_table.append(node);
        node_list.push(node)
    }
}

function create_ticker(data) {
    market_ticker_node_list = [];
    ticker = $('#market-ticker');
    // market
    var currency_block = document.createElement('ul');
    currency_block.id = 'webTicker';
    // market overview
    // var market_currency_block = document.createElement('ul');
    // market_currency_block.id = 'webTicker_market';
    for (var i = 0; i < TICKER_AMOUNT_CURRENCIES; i++) {
        // market
        var currency_block_a = document.createElement('li');
        $(currency_block_a).attr('style', 'margin-right: 1rem !important;');
        currency_icon = document.createElement('img');
        $(currency_icon).attr('src', 'https://raw.githubusercontent.com/atomiclabs/cryptocurrency-icons/master/32%402x/color/' + data[i].symbol.toLowerCase() + '%402x.png');
        $(currency_icon).attr('style', 'width: 25px; margin-top: -5px;');
        currency_block_a.append(currency_icon);
        currency_name_block = document.createElement('span');
        currency_name_block.innerHTML = data[i].name + '<span style="color: #989898;">(' + data[i].symbol + ')</span>';
        currency_name_block.className = 'curr_name market-view-ticker';
        currency_block_a.appendChild(currency_name_block);
        graph = document.createElement('img');
        $(graph).attr('src', 'https://graphs2.coinpaprika.com/currency/chart/' + data[i].id + '/7d/chart.svg');
        $(graph).attr('style', 'margin: -5px 5px 5px 5px; height:16px;');
        currency_block_a.append(graph);
        currency_value_block = document.createElement('span');
        if (data[i].quotes.USD.price > 1) {
            currency_value_block.innerHTML = ' ' + data[i].quotes.USD.price.toFixed(2) + '$';
        } else {
            currency_value_block.innerHTML = ' ' + data[i].quotes.USD.price.toFixed(5) + '$';
        }
        currency_value_block.className = 'ticker-curr-value market-view-ticker';
        currency_block_a.appendChild(currency_value_block);
        currency_7d_container = document.createElement('span');
        currency_7d_container.innerHTML = (data[i].quotes.USD.percent_change_7d.toFixed(2)) + ' %';
        if (data[i].quotes.USD.percent_change_7d >= 0) {
            currency_7d_container.className = 'market-view-ticker text-success text-left';
        } else {
            currency_7d_container.className = 'market-view-ticker text-danger text-left';
        }
        currency_block_a.append(currency_7d_container);
        currency_block_a.className = 'mr-5 market-ticker-text';
        currency_block.appendChild(currency_block_a);
        market_ticker_node_list.push(currency_block_a);
    }
    ticker.append(currency_block);
    // market_overview_ticker.append(market_currency_block);
    $('section.main-section').attr('style', 'margin-top: -82px;');
    $('.top-ticker').attr('style', 'margin-top: 55px;');
    $('#webTicker').webTicker({
        startEmpty: false
    });
    // $("#webTicker_market").webTicker();
}

function dashboard_market_overview() {
    // Market Info
    //var get_url = get_api_url('latest_listings');
    var get_url = 'https://api.coinpaprika.com/v1/tickers';

    $.getJSON(get_url, function(data) {
        data.sort(GetSortOrder());
        create_market_overview(data);
        create_ticker(data);
    });
}

function update_market_overview(data) {
    for (var i = 0; i < node_list.length; i++) {
        var coin_name_container = node_list[i].childNodes[0];
        var value_container = node_list[i].childNodes[2];
        var market_cap = node_list[i].childNodes[3];
        var _24h_container = node_list[i].childNodes[4];
        var _7d_container = node_list[i].childNodes[5];

        iconHTML = '<img src="https://raw.githubusercontent.com/atomiclabs/cryptocurrency-icons/master/32%402x/color/' + data[i].symbol.toLowerCase() + '%402x.png" class="cryptocurrency-icons">';
        coin_name_container.innerHTML = '<span style="margin-right: 10px"> ' + (i+1) + '</span>' + iconHTML + data[i].name;
        coin_name_container.className = 'market-view-coin-name'
        market_cap.innerHTML = abbreviateNumber(data[i].quotes.USD.market_cap.toFixed(2));
        market_cap.className = 'market-view-cap text-left'
        _7d_container.innerHTML = (data[i].quotes.USD.percent_change_7d.toFixed(2)) + ' %';
        _24h_container.innerHTML = (data[i].quotes.USD.percent_change_24h.toFixed(2)) + ' %';
        value_container.className = 'market-view-value text-left'

        if (data[i].quotes.USD.price > 1) {
            value_container.innerHTML = (data[i].quotes.USD.price.toFixed(2) + ' $');
        } else {
            value_container.innerHTML = (data[i].quotes.USD.price.toFixed(5) + ' $');
        }

        if (data[i].quotes.USD.percent_change_24h >= 0) {
            _24h_container.className = 'market-view-24h text-success text-left';
        } else {
            _24h_container.className = 'market-view-24h text-danger text-left';
        }
        if (data[i].quotes.USD.percent_change_7d >= 0) {
            _7d_container.className = 'market-view-7d text-success text-left';
        } else {
            _7d_container.className = 'market-view-7d text-danger text-left';
        }
    }
}

function update_market_ticker(data) {
    ticker = $('#market-ticker');
    market_overview_ticker = $("#market_overview_ticker");
    for (var i = 0; i < market_ticker_node_list.length; i++) {
        value_container = market_ticker_node_list[i];
        value_name = $(value_container).find('.curr_name')[0];
        value = $(value_container).find('.ticker-curr-value')[0];
        $.each(data, function(j, v) {
            if (v.name == value_name.innerHTML) {
                value_name.innerHTML = v.name;
                if (data[i].quotes.USD.price > 1) {
                    value.innerHTML = ' ' + v.quotes.USD.price.toFixed(2) + '$'
                } else {
                    value.innerHTML = ' ' + v.quotes.USD.price.toFixed(5) + '$'
                }
            }
        });
        //value_container.innerHTML = data[i].name + ' ' + data[i].quote.USD.price.toFixed(2) + ' $';
    }
}

function update_dashboard_market_overview() {
    // Market Info
    //var get_url = get_api_url('latest_listings');
    var get_url = 'https://api.coinpaprika.com/v1/tickers';

    $.getJSON(get_url, function(data) {
        data.sort(GetSortOrder());
        update_market_overview(data);
        update_market_ticker(data)
    });
}

function get_api_url(affix) {
    if (window.location.hostname == '127.0.0.1')
        var get_url = window.location.protocol + '//' + window.location.hostname + ':8000/member/api/' + affix;
    else
        var get_url = window.location.protocol + '//' + window.location.hostname + '/member/api/' + affix;
    return get_url
}
