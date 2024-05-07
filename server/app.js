const path = require('path');
const express = require("express");
const dotenv = require("dotenv");
const connectDB = require('./config/db');
const exphbs = require('express-handlebars');
const morgan = require('morgan');
const passport = require('passport');
const session = require('express-session');
const cors = require('cors');
const bodyParser = require('body-parser');

// Load Config
dotenv.config({ path: "./config/config.env" });

// passport config
require('./config/passport')(passport);

// Connect to DB
connectDB();

const app = express();

// For Cross Platform Http req
app.use(cors());

// Recieving data as JSON for POST
app.use(bodyParser.json());

// Logger on Console
if(process.env.NODE_ENV === "development"){
    app.use(morgan('dev'));
}

// handlebars
app.engine('.hbs', exphbs.engine({defaultLayout: 'main', extname: '.hbs'}));
app.set('view engine', '.hbs');

// express sessions
app.use(session({
    secret: 'Grade Senpai',
    resave: false,
    saveUninitialized: false
}))

// passport middlewares
app.use(passport.initialize());
app.use(passport.session());

// Routes
app.use('/', require('./routes/index'));
app.use('/auth', require('./routes/auth'));
app.use('/db', require('./routes/db'));

// CLI Login Redirect URI
app.get("/cli_login_200", (req, res) => {
  res.sendFile(path.join(__dirname, "cli_login_success.html"));
});
// Static Folder
app.use(express.static(path.join(__dirname, 'public')));

// Express Server Port
const PORT = process.env.PORT || 5000;

app.listen(
  PORT,
  console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`)
);
