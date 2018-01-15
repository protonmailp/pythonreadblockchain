var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'trace'
});


client.search({
  index: 'btc',
  type: 'info',
  body: {
      "query": {
        "query_string" : {
            "default_field" : "o",
            "query" : "1Q5XnSVEG7qv3idq8LhFYwmSaSgzwDYH49"
        }
    }
  }
}).then(function (resp) {
    var hits = resp.hits.hits;
}, function (err) {
    console.trace(err.message);
});


// 1976a914cb4339639d59a2682838e51f7ab5ad17dad64f2a88ac00000000'}}]
// [{'_op_type': 'index', '_index': 'btc', '_type': 'info', '_id': 'f3a0ad3b0325b74919b8f24a797619a26fec7ea8ef67bea2fccbc99
// 674b2ab0a', '_source': {'h': 99998, 'r': '01000000010000000000000000000000000000000000000000000000000000000000000000ffff
// ffff07044c86041b011cffffffff0100f2052a01000000434104aeaf4f686ba2b4ef3a3562ecd6246ef04f6c1bf758d306049559069fb6fb82adff7a
// 4ca27d87a10840160afa5bc1cc8a85a6645edf508d7dd962c7d7cf6f04f4ac00000000'}}, {'_op_type': 'index', '_index': 'btc', '_type
// ': 'info', '_id': '110ed92f558a1e3a94976ddea5c32f030670b5c58c3cc4d857ac14d7a1547a90', '_source': {'h': 99999, 'r': '0100




// const bs58 = require('bs58')

// const address = "15MSooy82ecYTGuJHBEEnnqeqQiGBRQRxR"
// const bytes = bs58.decode(address)
// console.log(bytes.toString('hex').slice(2,42))

//002b7076803fa702e250d9fcbc8c09b7d6216de6f9be366d1b



//0100000003da1640372bdea05c265e55f8e4a1907777b706ff479142472932ab35cdcb829b010000006a4730440220541119dd52916bdfe9eaa006bbe1c31fa5ac1446b9d661bc1fd2cf409cbbd6e302205771182cf16cebb8afb5f23138a984abd9970b8137e40d1b49e1367385ada8d60121028e86b9ba5e778b2bde64a34f1ecb16657822c985837958ce81e1c98809031978ffffffffca004439e281bbf4f9caf530a412c7945f8116a4f183349908c00ccd79363240020000006a473044022066cd350e1d99b4a3de25936f8d9bad1d437151d662f432f4620006d87918817802207e05c784cf49cc791bec6cbaa09effbcaf9b9542daefc6c833c7566eebdff796012102177aa649b8ef1ad44ba40343b02fd2e95291fff00c478265b533ff1ede082ce6ffffffff9dcc195f587136de90b37dc2c1f5168dc794ac8cd2b28c02c7433ba2ebdde98b020000006b483045022100d243a5aeabf27841a1a2cd51e9bb4e03ae46ba38a30b22a66c99b94e62d9d7de022011a68abace8d919c3e9e32e64cb18bdb793419434ccdcf0814d808e79186c3fe0121029e852dd9fa5225cd8ea8e16eae9b70233779ada25bb539db8cec0e39c3a33c7affffffff02c0270900000000001976a9142fbe5d723860c9dbc294faa75e1652153e9ab16788accf1c0000000000001976a914b7ae9d1f63fd6afdaa82de561d435516a29f75ac88ac00000000
