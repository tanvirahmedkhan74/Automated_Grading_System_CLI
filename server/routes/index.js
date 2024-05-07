const express = require('express');
const router = express.Router();

// @des     Login Page
// @route   GET /

router.get('/', (req, res) => {
    res.send('Login');
})

// @des     Dashboard Page
// @route   GET /dashboard

router.get('/dashboard', (req, res) => {
    res.send('Dashboard');
})

module.exports = router;