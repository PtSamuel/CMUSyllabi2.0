const express = require('express');
const app = express();
const api_router = require('./api');
const PORT = 443;

app.use(express.json());

app.use((req, res, next) => { 
	console.log(`Receiving request: ${req.method} ${req.url}`); 
	next();
})

app.get('/', (req, res) => {  res.send('Hello!'); });

app.use('/api', api_router);
app.get('/test', (req, res) => { res.send('World!'); });

app.listen(PORT, () => { console.log('Server is running.'); });
