# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ArgumentsRequired


class coss(Exchange):

    def describe(self):
        return self.deep_extend(super(coss, self).describe(), {
            'id': 'coss',
            'name': 'COSS',
            'countries': ['SG', 'NL'],
            'rateLimit': 1000,
            'version': 'v1',
            'certified': False,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/50328158-22e53c00-0503-11e9-825c-c5cfd79bfa74.jpg',
                'api': {
                    'trade': 'https://trade.coss.io/c/api/v1',
                    'engine': 'https://engine.coss.io/api/v1',
                    'public': 'https://trade.coss.io/c/api/v1',
                    'web': 'https://trade.coss.io/c',  # undocumented
                    'exchange': 'https://exchange.coss.io/api',
                },
                'www': 'https://www.coss.io',
                'doc': 'https://api.coss.io/v1/spec',
                'referral': 'https://www.coss.io/c/reg?r=OWCMHQVW2Q',
            },
            'has': {
                'fetchTrades': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchMarkets': True,
                'fetchCurrencies': True,
                'fetchBalance': True,
                'fetchOrderBook': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOrderTrades': True,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchOHLCV': True,
                'createOrder': True,
                'cancelOrder': True,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '1w': '1w',
            },
            'api': {
                'exchange': {
                    'get': [
                        'getmarketsummaries',
                    ],
                },
                'public': {
                    'get': [
                        'market-price',
                        'exchange-info',
                    ],
                },
                'web': {
                    'get': [
                        'coins/getinfo/all',  # undocumented
                        'order/symbols',  # undocumented
                        'coins/get_base_list',  # undocumented
                    ],
                },
                'engine': {
                    'get': [
                        'dp',
                        'ht',
                        'cs',
                    ],
                },
                'trade': {
                    'get': [
                        'ping',
                        'time',
                        'account/balances',
                        'account/details',
                    ],
                    'post': [
                        'order/add',
                        'order/details',
                        'order/list/open',
                        'order/list/completed',
                        'order/list/all',
                        'order/trade-detail',
                    ],
                    'delete': [
                        'order/cancel',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.0025,
                    'maker': 0.0,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {},
                    'deposit': {},
                },
            },
            'commonCurrencies': {
                'COS': 'COSS',
                'COSS': 'COSS.io',
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetExchangeInfo(params)
        #
        #     {       timezone:   "UTC",
        #           server_time:    1545171487108,
        #           rate_limits: [{    type: "REQUESTS",
        #                            interval: "MINUTE",
        #                               limit:  1000       }],
        #       base_currencies: [{currency_code: "BTC", minimum_total_order: "0.0001"},
        #                          {currency_code: "USDT", minimum_total_order: "1"},
        #                          {currency_code: "EUR", minimum_total_order: "1"}],
        #                 coins: [{       currency_code: "ADI",
        #                                            name: "Aditus",
        #                            minimum_order_amount: "0.00000001"},
        #                          ...
        #                          {       currency_code: "NPXSXEM",
        #                                            name: "PundiX-XEM",
        #                            minimum_order_amount: "0.00000001"  }                ],
        #               symbols: [{              symbol: "ADI_BTC",
        #                            amount_limit_decimal:  0,
        #                             price_limit_decimal:  8,
        #                                   allow_trading:  True      },
        #                          ...
        #                          {              symbol: "ETH_GUSD",
        #                            amount_limit_decimal:  5,
        #                             price_limit_decimal:  3,
        #                                   allow_trading:  True       }     ]               }
        #
        result = []
        markets = self.safe_value(response, 'symbols', [])
        baseCurrencies = self.safe_value(response, 'base_currencies', [])
        baseCurrenciesByIds = self.index_by(baseCurrencies, 'currency_code')
        currencies = self.safe_value(response, 'coins', [])
        currenciesByIds = self.index_by(currencies, 'currency_code')
        for i in range(0, len(markets)):
            market = markets[i]
            marketId = market['symbol']
            baseId, quoteId = marketId.split('_')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'amount_limit_decimal'),
                'price': self.safe_integer(market, 'price_limit_decimal'),
            }
            active = self.safe_value(market, 'allow_trading', False)
            baseCurrency = self.safe_value(baseCurrenciesByIds, baseId, {})
            minCost = self.safe_float(baseCurrency, 'minimum_total_order')
            currency = self.safe_value(currenciesByIds, baseId, {})
            defaultMinAmount = math.pow(10, -precision['amount'])
            minAmount = self.safe_float(currency, 'minimum_order_amount', defaultMinAmount)
            result.append({
                'symbol': symbol,
                'id': marketId,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': minAmount,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': minCost,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def fetch_currencies(self, params={}):
        response = self.webGetCoinsGetinfoAll(params)
        #
        #     [{                currency_code: "VET",
        #                                  name: "VeChain",
        #                             buy_limit:  0,
        #                            sell_limit:  0,
        #                                  usdt:  0,
        #                transaction_time_limit:  5,
        #                                status: "trade",
        #                         withdrawn_fee: "0.6",
        #              minimum_withdrawn_amount: "1.2",
        #                minimum_deposit_amount: "0.6",
        #                  minimum_order_amount: "0.00000001",
        #                        decimal_format: "0.########",
        #                            token_type:  null,  # "erc", "eos", "stellar", "tron", "ripple"...
        #                                buy_at:  0,
        #                               sell_at:  0,
        #                              min_rate:  0,
        #                              max_rate:  0,
        #                       allow_withdrawn:  False,
        #                         allow_deposit:  False,
        #         explorer_website_mainnet_link:  null,
        #         explorer_website_testnet_link:  null,
        #            deposit_block_confirmation: "6",
        #           withdraw_block_confirmation: "0",
        #                              icon_url: "https://s2.coinmarketcap.com/static/img/coins/32x32/3077.png",
        #                               is_fiat:  False,
        #                            allow_sell:  True,
        #                             allow_buy:  True                                                           }]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            currencyId = self.safe_string(currency, 'currency_code')
            code = self.safe_currency_code(currencyId)
            name = self.safe_string(currency, 'name')
            allowBuy = self.safe_value(currency, 'allow_buy')
            allowSell = self.safe_value(currency, 'allow_sell')
            allowWithdrawals = self.safe_value(currency, 'allow_withdrawn')
            allowDeposits = self.safe_value(currency, 'allow_deposit')
            active = allowBuy and allowSell and allowWithdrawals and allowDeposits
            fee = self.safe_float(currency, 'withdrawn_fee')
            type = self.safe_string(currency, 'token_type')
            #
            # decimal_format can be anything...
            #
            #     0.########
            #     #.########
            #     0.##
            #     ''(empty string)
            #     0.000000
            #     null(None)
            #     0.0000
            #     0.###
            #
            decimalFormat = self.safe_string(currency, 'decimal_format')
            precision = 8
            if decimalFormat is not None:
                parts = decimalFormat.split('.')
                numParts = len(parts)  # transpiler workaround for array lengths
                if numParts > 1:
                    if len(parts[1]) > 1:
                        precision = len(parts[1])
            result[code] = {
                'id': currencyId,
                'code': code,
                'info': currency,
                'name': name,
                'active': active,
                'fee': fee,
                'precision': precision,
                'type': type,
                'limits': {
                    'amount': {
                        'min': self.safe_float(currency, 'minimum_order_amount'),
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_float(currency, 'minimum_withdrawn_amount'),
                        'max': None,
                    },
                },
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.tradeGetAccountBalances(params)
        #
        #     [{currency_code: "ETH",
        #               address: "0x6820511d43111a941d3e187b9e36ec64af763bde",  # deposit address
        #                 total: "0.20399125",
        #             available: "0.20399125",
        #              in_order: "0",
        #                  memo:  null                                         },  # tag, if any
        #       {currency_code: "ICX",
        #               address: "",
        #                 total: "0",
        #             available: "0",
        #              in_order: "0",
        #                  memo:  null  }                                         ]
        #
        result = {}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            total = self.safe_float(balance, 'total')
            used = self.safe_float(balance, 'in_order')
            free = self.safe_float(balance, 'available')
            result[code] = {
                'total': total,
                'used': used,
                'free': free,
            }
        return self.parse_balance(result)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_integer(ohlcv, 0),   # timestamp
            self.safe_float(ohlcv, 1),  # Open
            self.safe_float(ohlcv, 2),  # High
            self.safe_float(ohlcv, 3),  # Low
            self.safe_float(ohlcv, 4),  # Close
            self.safe_float(ohlcv, 5),  # base Volume
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'tt': self.timeframes[timeframe],
        }
        response = self.engineGetCs(self.extend(request, params))
        #
        #     {      tt:   "1m",
        #         symbol:   "ETH_BTC",
        #       nextTime:    1545138960000,
        #         series: [[ 1545138960000,
        #                     "0.02705000",
        #                     "0.02705000",
        #                     "0.02705000",
        #                     "0.02705000",
        #                     "0.00000000"    ],
        #                   ...
        #                   [ 1545168900000,
        #                     "0.02684000",
        #                     "0.02684000",
        #                     "0.02684000",
        #                     "0.02684000",
        #                     "0.00000000"    ]  ],
        #          limit:    500                    }
        #
        return self.parse_ohlcvs(response['series'], market, timeframe, since, limit)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        request = {'symbol': marketId}
        # limit argument is not supported on COSS's end
        response = self.engineGetDp(self.extend(request, params))
        #
        #     {symbol:   "COSS_ETH",
        #         asks: [["0.00065200", "214.15000000"],
        #                 ["0.00065300", "645.45000000"],
        #                 ...
        #                 ["0.00076400", "380.00000000"],
        #                 ["0.00076900", "25.00000000"]     ],
        #        limit:    100,
        #         bids: [["0.00065100", "666.99000000"],
        #                 ["0.00065000", "1171.93000000"],
        #                 ...
        #                 ["0.00037700", "3300.00000000"],
        #                 ["0.00037600", "2010.82000000"]   ],
        #         time:    1545180569354                       }
        #
        timestamp = self.safe_integer(response, 'time')
        return self.parse_order_book(response, timestamp)

    def parse_ticker(self, ticker, market=None):
        #
        #      {MarketName: "COSS-ETH",
        #              High:  0.00066,
        #               Low:  0.000628,
        #        BaseVolume:  131.09652674,
        #              Last:  0.000636,
        #         TimeStamp: "2018-12-19T05:16:41.369Z",
        #            Volume:  206126.6143710692,
        #               Ask: "0.00063600",
        #               Bid: "0.00063400",
        #           PrevDay:  0.000636                   }
        #
        timestamp = self.parse8601(self.safe_string(ticker, 'TimeStamp'))
        symbol = None
        marketId = self.safe_string(ticker, 'MarketName')
        if marketId is not None:
            marketId = marketId.replace('-', '_')
        market = self.safe_value(self.markets_by_id, marketId, market)
        if market is None:
            if marketId is not None:
                baseId, quoteId = marketId.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if market is not None:
            symbol = market['symbol']
        previous = self.safe_float(ticker, 'PrevDay')
        last = self.safe_float(ticker, 'Last')
        change = None
        percentage = None
        if last is not None:
            if previous is not None:
                change = last - previous
                if previous > 0:
                    percentage = (change / previous) * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume'),
            'quoteVolume': self.safe_float(ticker, 'BaseVolume'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.exchangeGetGetmarketsummaries(params)
        #
        #     {success:    True,
        #       message:   "",
        #        result: [{MarketName: "COSS-ETH",
        #                          High:  0.00066,
        #                           Low:  0.000628,
        #                    BaseVolume:  131.09652674,
        #                          Last:  0.000636,
        #                     TimeStamp: "2018-12-19T05:16:41.369Z",
        #                        Volume:  206126.6143710692,
        #                           Ask: "0.00063600",
        #                           Bid: "0.00063400",
        #                       PrevDay:  0.000636                   },
        #                  ...
        #                  {MarketName: "XLM-BTC",
        #                          High:  0.0000309,
        #                           Low:  0.0000309,
        #                    BaseVolume:  0,
        #                          Last:  0.0000309,
        #                     TimeStamp: "2018-12-19T02:00:02.145Z",
        #                        Volume:  0,
        #                           Ask: "0.00003300",
        #                           Bid: "0.00003090",
        #                       PrevDay:  0.0000309                  }  ],
        #       volumes: [{CoinName: "ETH", Volume: 668.1928095999999},  # these are overall exchange volumes
        #                  {CoinName: "USD", Volume: 9942.58480324},
        #                  {CoinName: "BTC", Volume: 43.749184570000004},
        #                  {CoinName: "COSS", Volume: 909909.26644574},
        #                  {CoinName: "EUR", Volume: 0},
        #                  {CoinName: "TUSD", Volume: 2613.3395026999997},
        #                  {CoinName: "USDT", Volume: 1017152.07416519},
        #                  {CoinName: "GUSD", Volume: 1.80438},
        #                  {CoinName: "XRP", Volume: 15.95508},
        #                  {CoinName: "GBP", Volume: 0},
        #                  {CoinName: "USDC", Volume: 0}                   ],
        #             t:    1545196604371                                       }
        #
        tickers = self.safe_value(response, 'result', [])
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_ticker(self, symbol, params={}):
        tickers = self.fetch_tickers([symbol], params)
        return tickers[symbol]

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.engineGetHt(self.extend(request, params))
        #
        #     { symbol:   "COSS_ETH",
        #         limit:    100,
        #       history: [{          id:  481321,
        #                           price: "0.00065100",
        #                             qty: "272.92000000",
        #                    isBuyerMaker:  False,
        #                            time:  1545180845019  },
        #                  {          id:  481322,
        #                           price: "0.00065200",
        #                             qty: "1.90000000",
        #                    isBuyerMaker:  True,
        #                            time:  1545180847535},
        #                  ...
        #                  {          id:  481420,
        #                           price: "0.00065300",
        #                             qty: "2.00000000",
        #                    isBuyerMaker:  True,
        #                            time:  1545181167702}   ],
        #          time:    1545181171274                        }
        #
        return self.parse_trades(response['history'], market, since, limit)

    def parse_trade_fee(self, fee):
        if fee is None:
            return fee
        parts = fee.split(' ')
        numParts = len(parts)
        cost = parts[0]
        code = None
        if numParts > 1:
            code = self.safe_currency_code(parts[1])
        return {
            'cost': cost,
            'currency': code,
        }

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #      {          id:  481322,
        #               price: "0.00065200",
        #                 qty: "1.90000000",
        #        isBuyerMaker:  True,
        #                time:  1545180847535}
        #
        # fetchOrderTrades(private)
        #
        #     [{        hex_id:  null,
        #                 symbol: "COSS_ETH",
        #               order_id: "ad6f6b47-3def-4add-a5d5-2549a9df1593",
        #             order_side: "BUY",
        #                  price: "0.00065900",
        #               quantity: "10",
        #                    fee: "0.00700000 COSS",
        #         additional_fee: "0.00000461 ETH",
        #                  total: "0.00659000 ETH",
        #              timestamp:  1545152356075                          }]
        #
        id = self.safe_string(trade, 'id')
        timestamp = self.safe_integer(trade, 'time')
        orderId = self.safe_string(trade, 'order_id')
        side = self.safe_string_lower(trade, 'order_side')
        symbol = None
        marketId = self.safe_string(trade, 'symbol')
        if marketId is not None:
            market = self.safe_value(self.markets_by_id, marketId, market)
            if market is None:
                baseId, quoteId = marketId.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        elif market is not None:
            symbol = market['symbol']
        cost = None
        price = self.safe_float(trade, 'price')
        amount = self.safe_float_2(trade, 'qty', 'quantity')
        if amount is not None:
            if price is not None:
                cost = price * amount
        result = {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }
        fee = self.parse_trade_fee(self.safe_string(trade, 'fee'))
        if fee is not None:
            additionalFee = self.parse_trade_fee(self.safe_string(trade, 'additional_fee'))
            if additionalFee is None:
                result['fee'] = fee
            else:
                result['fees'] = [
                    fee,
                    additionalFee,
                ]
        return result

    def fetch_orders_by_type(self, type, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            # 'from_id': 'b2a2d379-f9b6-418b-9414-cbf8330b20d1',  # string(uuid), fetchOrders(all orders) only
            # 'page': 0,  # different pagination in fetchOpenOrders and fetchClosedOrders
            # 'limit': 50,  # optional, max = default = 50
            'symbol': market['id'],  # required
        }
        if limit is not None:
            request['limit'] = limit  # max = default = 50
        method = 'tradePostOrderList' + type
        response = getattr(self, method)(self.extend(request, params))
        #
        # fetchOrders, fetchClosedOrders
        #
        #     [{      hex_id: "5c192784330fe51149f556bb",
        #             order_id: "5e46e1b1-93d5-4656-9b43-a5635b08eae9",
        #           account_id: "a0c20128-b9e0-484e-9bc8-b8bb86340e5b",
        #         order_symbol: "COSS_ETH",
        #           order_side: "BUY",
        #               status: "filled",
        #           createTime:  1545152388019,
        #                 type: "limit",
        #         timeMatching:  0,
        #          order_price: "0.00065900",
        #           order_size: "10",
        #             executed: "10",
        #           stop_price: "0.00000000",
        #                  avg: "0.00065900",
        #                total: "0.00659000 ETH"                        }  ]
        #
        # fetchOpenOrders
        #
        #     {
        #         "total": 2,
        #         "list": [
        #             {
        #                 "order_id": "9e5ae4dd-3369-401d-81f5-dff985e1c4ty",
        #                 "account_id": "9e5ae4dd-3369-401d-81f5-dff985e1c4a6",
        #                 "order_symbol": "eth-btc",
        #                 "order_side": "BUY",
        #                 "status": "OPEN",
        #                 "createTime": 1538114348750,
        #                 "type": "limit",
        #                 "order_price": "0.12345678",
        #                 "order_size": "10.12345678",
        #                 "executed": "0",
        #                 "stop_price": "02.12345678",
        #                 "avg": "1.12345678",
        #                 "total": "2.12345678"
        #             }
        #         ]
        #     }
        #
        # the following code is to handle the above difference in response formats
        orders = None
        if isinstance(response, list):
            orders = response
        else:
            orders = self.safe_value(response, 'list', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_type('All', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_type('Completed', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_type('Open', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': id,
        }
        response = self.tradePostOrderDetails(self.extend(request, params))
        return self.parse_order(response)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {
            'order_id': id,
        }
        response = self.tradePostOrderTradeDetail(self.extend(request, params))
        #
        #     [{        hex_id:  null,
        #                 symbol: "COSS_ETH",
        #               order_id: "ad6f6b47-3def-4add-a5d5-2549a9df1593",
        #             order_side: "BUY",
        #                  price: "0.00065900",
        #               quantity: "10",
        #                    fee: "0.00700000 COSS",
        #         additional_fee: "0.00000461 ETH",
        #                  total: "0.00659000 ETH",
        #              timestamp:  1545152356075                          }]
        #
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        if status is None:
            return status
        statuses = {
            'OPEN': 'open',
            'CANCELLED': 'canceled',
            'FILLED': 'closed',
            'PARTIAL_FILL': 'closed',
            'CANCELLING': 'open',
        }
        return self.safe_string(statuses, status.upper(), status)

    def parse_order(self, order, market=None):
        #
        #       {      hex_id: "5c192784330fe51149f556bb",  # missing in fetchOpenOrders
        #             order_id: "5e46e1b1-93d5-4656-9b43-a5635b08eae9",
        #           account_id: "a0c20128-b9e0-484e-9bc8-b8bb86340e5b",
        #         order_symbol: "COSS_ETH",  # coss-eth in docs
        #           order_side: "BUY",
        #               status: "filled",
        #           createTime:  1545152388019,
        #                 type: "limit",
        #         timeMatching:  0,  # missing in fetchOpenOrders
        #          order_price: "0.00065900",
        #           order_size: "10",
        #             executed: "10",
        #           stop_price: "0.00000000",
        #                  avg: "0.00065900",
        #                total: "0.00659000 ETH"                        }
        #
        id = self.safe_string(order, 'order_id')
        symbol = None
        marketId = self.safe_string(order, 'order_symbol')
        if marketId is None:
            if market is not None:
                symbol = market['symbol']
        else:
            # a minor workaround for lowercase eth-btc symbols
            marketId = marketId.upper()
            marketId = marketId.replace('-', '_')
            market = self.safe_value(self.markets_by_id, marketId, market)
            if market is None:
                baseId, quoteId = marketId.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
            else:
                symbol = market['symbol']
        timestamp = self.safe_integer(order, 'createTime')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        price = self.safe_float(order, 'order_price')
        filled = self.safe_float(order, 'executed')
        type = self.safe_string(order, 'type')
        amount = self.safe_float(order, 'order_size')
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = amount - filled
        average = self.safe_float(order, 'avg')
        side = self.safe_string_lower(order, 'order_side')
        cost = self.safe_float(order, 'total')
        fee = None
        trades = None
        return {
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_symbol': market['id'],
            'order_size': self.amount_to_precision(symbol, amount),
            'order_side': side.upper(),
            'type': type,
        }
        if price is not None:
            request['order_price'] = self.price_to_precision(symbol, price)
        response = self.tradePostOrderAdd(self.extend(request, params))
        #
        #     {
        #         "order_id": "9e5ae4dd-3369-401d-81f5-dff985e1c4ty",
        #         "account_id": "9e5ae4dd-3369-401d-81f5-dff985e1c4a6",
        #         "order_symbol": "eth-btc",
        #         "order_side": "BUY",
        #         "status": "OPEN",
        #         "createTime": 1538114348750,
        #         "type": "limit",
        #         "order_price": "0.12345678",
        #         "order_size": "10.12345678",
        #         "executed": "0",
        #         "stop_price": "02.12345678",
        #         "avg": "1.12345678",
        #         "total": "2.12345678"
        #     }
        #
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'order_symbol': market['id'],
        }
        response = self.tradeDeleteOrderCancel(self.extend(request, params))
        #
        #     {order_symbol: "COSS_ETH",
        #           order_id: "30f2d698-39a0-4b9f-a3a6-a179542373bd",
        #         order_size:  0,
        #         account_id: "a0c20128-b9e0-484e-9bc8-b8bb86340e5b",
        #          timestamp:  1545202728814,
        #         recvWindow:  null                                   }
        #
        return self.parse_order(response)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        if api == 'trade':
            self.check_required_credentials()
            timestamp = self.nonce()
            query = self.extend({
                'timestamp': timestamp,  # required(int64)
                # 'recvWindow': 10000,  # optional(int32)
            }, params)
            request = None
            if method == 'GET':
                request = self.urlencode(query)
                url += '?' + request
            else:
                request = self.json(query)
                body = request
            headers = {
                'Signature': self.hmac(self.encode(request), self.encode(self.secret)),
                'Authorization': self.apiKey,
                'X-Requested-With': 'XMLHttpRequest',
            }
        else:
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
