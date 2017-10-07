'use strict';

var request = require('request');

const ApiAiApp = require('actions-on-google').ApiAiApp;
const BUILD_BOT = 'input.build';
const SET_SPLIT = 'input.setSplit';
const OUT_SPLIT = 'input.outputSplit';
const SET_PURCH = 'input.setPurchase';
const OUT_PURCH = 'input.outputPurchase';
const FAST_FORWARD = 'input.fastForward';
const CURRENT_PRICE = 'input.currentPrices';
const WALLET = 'input.wallet';
const PORTFOLIO = 'input.portfolio';
const RESET = 'input.reset';
const CONFIRM = 'input.confirm';

const BOT_URL = ' ';

exports.autom8 = (req, res) => {
    const app = new ApiAiApp({ request: req, response: res });
    function build(app) {
        let buildDate = app.getArgument('date');
        app.tell('Okay, we deployed your new service starting ' + buildDate);
        var options = {
            method: 'POST',
            url: BOT_URL + 'build',
            qs: { date: buildDate },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        
        request(options, function (err, res, body) {
            console.log(json);
        })
    }

    function setSplit(app) {
        let splitCoin = app.getArgument('Coin');
        let splitPercent = app.getArgument('percentage');
        var options = {
            method: 'POST',
            url: BOT_URL + 'set-split',
            qs: {
                coin: splitCoin,
                percent: splitPercent
            },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            console.log(json);
        })
    }

    function outputSplit(app) {
        let splitCoin = app.getArgument('Coin');
        var options = {
            method: 'GET',
            url: BOT_URL + 'get-split',
            qs: { coin: splitCoin },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            let json = JSON.parse(body);
            console.log(json);
        })
    }

    function setPurchase(app) {
        let purchaseCoin = app.getArgument('Coin');
        let purchasePercent = app.getArgument('percentage');
        var options = {
            method: 'POST',
            url: BOT_URL + 'set-purchase-limit',
            qs: {
                coin: purchaseCoin,
                percent: purchasePercent
            },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            console.log(json);
        })
    }

    function outputPurchase(app) {
        let purchaseCoin = app.getArgument('Coin');
        var options = {
            method: 'GET',
            url: BOT_URL + 'get-purchase-limit',
            qs: { coin: purchaseCoin },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            let json = JSON.parse(body);
            console.log(json);
        })
    }

    function fastForward(app) {
        let length = app.getArgument('number-integer');
        let measure = app.getArgument('dateMeadurement');
        var options = {
            method: 'POST',
            url: BOT_URL + 'fast-forward',
            qs: {
                integer: length,
                duration: measure
            },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            console.log(json);
        })
    }

    function currentPrice(app) {
        let priceCoin = app.getArgument('Coin');
        var options = {
            method: 'GET',
            url: BOT_URL + 'current-prices',
            qs: { coin: priceCoin },
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            let json = JSON.parse(body);
            console.log(json);
        })
    }

    function outWallet(app) {
        var options = {
            method: 'GET',
            url: BOT_URL + 'out-put-wallet',
            qs: {},
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            let json = JSON.parse(body);
            console.log(json);
        })
    }

    function outPortfolio(app) {
        var options = {
            method: 'GET',
            url: BOT_URL + 'out-put-portfolio',
            qs: {},
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            let json = JSON.parse(body);
            console.log(json);
        })
    }

    function resetBot(app) {
        app.ask('Are you sure you want to delete everything');
    }

    function confirmReset(app) {
        app.tell('Alright, resetting everything');
        var options = {
            method: 'POST',
            url: BOT_URL + 'reset',
            qs: {},
            headers:
           {
               'token': '',
               'cache-control': 'no-cache'
           }
        }
        request(options, function (err, res, body) {
            console.log(json);
        })
    }

    let actionMap = new Map();
    actionMap.set(BUILD_BOT, build);
    actionMap.set(SET_SPLIT, setSplit);
    actionMap.set(OUT_SPLIT, outputSplit);
    actionMap.set(SET_PURCH, setPurchase);
    actionMap.set(OUT_PURCH, outputPurchase);
    actionMap.set(FAST_FORWARD, fastForward);
    actionMap.set(CURRENT_PRICE, currentPrice);
    actionMap.set(WALLET, outWallet);
    actionMap.set(PORTFOLIO, outPortfolio);
    actionMap.set(RESET, resetBot);
    actionMap.set(CONFIRM, confirmReset);
    app.handleRequest(actionMap);
}