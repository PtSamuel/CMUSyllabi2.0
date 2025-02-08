const express = require('express');
const api_router = express.Router();

api_router.get('/test', (req, res) => {
	res.json({ course: 15213 });
});

module.exports = api_router;

