const express = require('express');
const api_router = express.Router();
// import * as db from './db.js';
const { find_course } = require('./db');

api_router.get('/test', (req, res) => {
	res.json({ course: 15213 });
});

api_router.get('/find_course', (req, res) => {
	const params = Object.keys(req.query);
	console.log(`Parameters: ${params}`);
	const { course_number } = req.query;
	// res.json({ course_number: course_number });
	find_course(course_number, (result) => { res.json(result); });
	// const json = find_course(course_number);
	// console.log(json);
	// res.json(json);
});

module.exports = api_router;

