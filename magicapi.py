import flask
import requests
import json
from flask import jsonify



while True :
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    # Gets data for defined coins from CREX24 (address have to be changed to add new coins)
    crexapi = "https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_ALPS,BTC_CRS]"
    crexresp = requests.get(crexapi)
    crexdata = crexresp.text
    crexparsed = json.loads(crexdata)

    # Gets Coinstock.me coin data
    csapi = "https://coinstock.me//api/v2/tickers.json"
    csresp = requests.get(csapi)
    csdata = csresp.text
    csparsed = json.loads(csdata)

    tlrfloat = float(csparsed["tlrbtc"]["ticker"]["last"])
    rpwnfloat = float(csparsed["rpwnbtc"]["ticker"]["last"])

    # Gets Graviex coin data
    grvapi = "https://graviex.net//api/v2/tickers.json"
    grvresp = requests.get(grvapi)
    grvdata = grvresp.text
    grvparsed = json.loads(grvdata)
    vtlfloat = float(grvparsed["vtlbtc"]["ticker"]["last"])

    # Gets Cryptobridge API data
    cbapi = "https://api.crypto-bridge.org/api/v1/ticker"
    cbresp = requests.get(cbapi)
    cbdata = cbresp.text
    cbparsed = json.loads(cbdata)

    # Parses Gincoin price data
    for i in cbparsed:
        if i['id'] == 'GIN_BTC':
            cbginprice = (i)['last']
            cbginfloat = float(cbginprice)
            break
    # Parses Manocoin price data
    for i in cbparsed:
        if i['id'] == 'MANO_BTC':
            cbmanoprice = (i)['last']
            cbmanofloat = float(cbmanoprice)
            break
    #Parses MCT+ price data
    for i in cbparsed:
        if i['id'] == 'MCT_BTC':
            cbmctprice = (i)['last']
            cbmctfloat = float(cbmctprice)
            break

    # Scrapes CREX24 data
    for i in crexparsed['Tickers']:
        if i['PairName'] == "BTC_ALPS":
            alpsprice = (i)['Last']
            alpsvolumetext = (i)['BaseVolume']
            alpsvolume = float(alpsvolumetext)
            alpsfloat = float(alpsprice)
            break
    for i in crexparsed['Tickers']:
        if i['PairName'] == "BTC_CRS":
            crsprice = (i)['Last']
            crsvolumetext = (i)['BaseVolume']
            crsvolume = float(crsvolumetext)
            crsfloat = float(crsprice)
            break

    # Gets nethash for the listed coins
    ginnethashresp = requests.get( "https://explorer.gincoin.io/api/getnetworkhashps" )
    if ginnethashresp.status_code == 200:
        ginnethash = float(ginnethashresp.text)
    else:
        ginnethash = 0

    manonethashresp = requests.get( "http://explorer.manocoin.org/api/getnetworkhashps" )
    if manonethashresp.status_code == 200:
        manonethash = float(manonethashresp.text)
    else:
        manonethash = 0

    alpsnethashresp = requests.get("http://explorer.alpenschilling.cash/api/getnetworkhashps")
    if alpsnethashresp.status_code == 200:
        alpsnethash = float(alpsnethashresp.text)
    else:
        alpsnethash = 0

    crsnethashresp = requests.get("https://criptoreal.info/api/getnetworkhashps")
    if crsnethashresp.status_code == 200:
        crsnethash = float(crsnethashresp.text)
    else:
        crsnethash = 0

    mctnethashresp = requests.get("https://explorer.mct.plus/api/getnetworkhashps")
    if mctnethashresp.status_code == 200:
        mctnethash = float(mctnethashresp.text)
    else:
        mctnethash = 0

    tlrnethashresp = requests.get("https://explorer.mct.plus/api/getnetworkhashps")
    if tlrnethashresp.status_code == 200:
        tlrnethash = float(tlrnethashresp.text)
    else:
        tlrnethash = 0

    vtlnethashresp = requests.get("https://explorer.vertical.ovh/api/getnetworkhashps")
    if vtlnethashresp.status_code == 200:
        vtlnethash = float(vtlnethashresp.text)
    else:
        vtlnethash = 0

    rpwnnethashresp = requests.get("http://explorer.respawn.rocks:3001/api/getnetworkhashps")
    if rpwnnethashresp.status_code == 200:
        rpwnnethash = float(rpwnnethashresp.text)
    else:
        rpwnnethash = 0

    # Creates list data

    nethashps = [
        {'id': 0,
         'coin': "GIN",
         'nethash': ginnethash,
         'last': cbginfloat},
        {'id': 1,
         'coin': "MANO",
         'nethash': manonethash,
         'last': cbmanofloat},
        {'id': 2,
         'coin': "ALPS",
         'nethash': alpsnethash,
         'last': alpsfloat},
        {'id': 3,
         'coin': "CRS",
         'nethash': crsnethash,
         'last': crsfloat},
        {'id': 4,
         'coin': "MCT",
         'nethash': mctnethash,
         'last': cbmctfloat},
        {'id': 5,
         'coin': "TLR",
         'nethash': tlrnethash,
         'last': tlrfloat},
        {'id': 6,
        'coin': "VTL",
        'nethash': vtlnethash,
        'last': vtlfloat},
        {'id': 7,
         'coin': "RPWN",
         'nethash': rpwnnethash,
         'last': rpwnfloat},
    ]

    @app.route('/', methods=['GET'])
    def home():
        return "Welcome to Trollmann's API server! Stay gentle and don't overload me!"


    @app.route('/nethash', methods=['GET', 'POST'])
    def nethash():
        return jsonify(nethashps)


    app.run()
    time.sleep(300)
