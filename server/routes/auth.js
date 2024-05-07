const express = require("express");
const router = express.Router();
const passport = require("passport");
const jwt = require("jsonwebtoken");
const LocalStorage = require('node-localstorage').LocalStorage;
const localStorage = new LocalStorage('./scratch');

// @des     Google Authentication
// @route   GET /auth/google

router.get(
  "/google",
  passport.authenticate("google", {
    scope: [
      "email",
      "profile",
      "https://www.googleapis.com/auth/spreadsheets",
      "https://www.googleapis.com/auth/gmail.readonly",
      "https://www.googleapis.com/auth/gmail.send",
      "https://www.googleapis.com/auth/drive"
    ],
    accessType: "offline",
    prompt: "consent",
  })
);

// @des     Google Auth Callback
// @route   GET /auth/google/callback

router.get(
  "/google/callback",
  passport.authenticate("google", { failureRedirect: "/" }),
  (req, res) => {
    const token = jwt.sign({ user: req.user }, process.env.JWT_SECRET_KEY);
    localStorage.setItem('token', token);
    res.redirect(`http://localhost:8000/cli_login_200`);
  }
);

// @des     Logout of account
// @route   GET /auth/logout

router.get("/logout", (req, res) => {
  req.logout((err) => {
    if (err) {
      console.error(err);
      return res.status(500).send("Logout failed");
    }

    res.redirect(`${process.env.CLIENT_SIDE_URL}/login`);
  });
});

router.get("/get_access_token", (req, res) => {
  const token = localStorage.getItem('token');
  localStorage.clear();
  if(token){
    res.send(token);
  }else res.send(404);
});

module.exports = router;
