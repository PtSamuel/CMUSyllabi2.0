const express = require('express');
const api_router = express.Router();
// import * as db from './db.js';
const { find_course, find } = require('./db');

api_router.get('/test', (req, res) => {
	res.json({ course: 15213 });
});

api_router.get('/find_course', (req, res) => {
	const params = Object.keys(req.query);
	console.log(`Parameters: ${params}`);
	const { course_number } = req.query;
	find_course(course_number, (result) => { res.json(result); });
});

api_router.get('/find', (req, res) => {
	const { course_title, department, semester, limit, page } = req.query;
	find(course_title, department, semester, limit, page, (result) => { res.json(result); });
});

module.exports = api_router;

