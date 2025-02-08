const express = require('express');
const api_router = express.Router();

api_router.get('/test', (req, res) => {
	res.json({ course: 15213 });
});

api_router.get('/find_course', (req, res) => {
	const params = Object.keys(req.query);
	console.log(`Parameters: ${params}`);
	const { course_number } = req.query;
	res.json({ course_number: course_number });
});

module.exports = api_router;

