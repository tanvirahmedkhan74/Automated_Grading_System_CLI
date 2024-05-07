const { google } = require("googleapis");
const authorize = require("../config/sheets");

//  @desc   Create and send Google Form Link To the Student's Mail
//  @params Google auth token, List of mails, Uri of the google form
const SendFormLinkMail = async (accessToken, mails, uri) => {

    const auth = await authorize(accessToken);
    // Create Gmail client
    const gmail = google.gmail({ version: "v1", auth });

    const emailContent = [
        `To: ${mails.join(',')}`,
        "Content-type: text/html;charset=iso-8859-1",
        "MIME-Version: 1.0",
        "Subject: Google Form Quiz Link",
        "",
        `Hi! Here is your Link for the quiz on Google Form. Please Finish it before the deadline! 
            uri: ${uri}
        `,
    ];

    // Pre process the mail data
    const email = emailContent.join('\r\n').trim();
    const base64Email = Buffer.from(email).toString('base64');

    try {
        const response = await gmail.users.messages.send({
            userId: 'me',
            requestBody: {
              raw: base64Email
            }
        });

        if(response) console.log('Mail send success: ', response);
    } catch (error) {
        console.log('Error while sending mail: ', error)
    }
};

module.exports = SendFormLinkMail;
