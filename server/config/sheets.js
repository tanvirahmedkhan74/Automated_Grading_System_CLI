const { google } = require('googleapis');

// Authorization oauth2client object for accessing the Google API's

const authorize = async (accessToken) => {
    const oauth2Client = new google.auth.OAuth2(
        process.env.GOOGLE_CLIENT_ID,
        process.env.GOOGLE_CLIENT_SECRET
    );

    oauth2Client.setCredentials({
        access_token: accessToken
    });

    return oauth2Client;
}

module.exports = authorize;
