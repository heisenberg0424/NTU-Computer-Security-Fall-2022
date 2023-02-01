const express = require('express');

const app = express();
app.use(express.urlencoded({ extended: false }));

const BOT_HOST = process.env.BOT_HOST || 'localhost';
const BOT_PORT = process.env.BOT_PORT || 8080;

app.get("/", function (req, res) {
    res.sendFile(__dirname + '/views/index.html')
});

app.get("/render", function (req, res) {
    res.sendFile(__dirname + '/views/render.html')
});

const net = require('net');

app.post("/report", function (req, res) {
    const { url } = req.body;
    if (typeof url !== 'string') return res.send("Invalid URL");

    if (!url || !RegExp('^https?://.*$').test(url)) {
        return res.status(400).send('Invalid URL');
    }
    try {
        const client = net.connect(BOT_PORT, BOT_HOST, () => {
            client.write(url)
        })

    		let response = '';
        client.on('data', data => {
            response = data.toString()
            client.end()
        })

        client.on('end', () => res.send(response))
    } catch (e) {
        console.log(e)
        res.status(500).send('Something is wrong...')
    }
});

app.listen(80);
