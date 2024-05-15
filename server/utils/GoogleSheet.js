const { google } = require("googleapis");
const authorize = require("../config/sheets");
const Assessment = require("../models/Assessement");
const axios = require("axios");

const generateRandomInteger = (min, max) => {
  if (min > max) {
    throw new Error("Minimum value cannot be greater than maximum value.");
  }
  const randomDecimal = Math.random();

  // Multiply the random number by the range (max - min + 1) and floor the result
  const randomInteger = Math.floor(randomDecimal * (max - min + 1)) + min;

  return randomInteger;
};

const extractSheetId = (sheetLink) => {
  let spreadSheetID = sheetLink.split("/d/");
  spreadSheetID = spreadSheetID[1].split("/edit");
  spreadSheetID = spreadSheetID[0];

  return spreadSheetID;
};

// Returns a 2d array of arrays containing answers, 0th index is the email
const extractAnswers = (response) => {
  let answers = [];

  for (let i = 0; i < response?.length; i++) {
    const ans = response[i].answers;
    let temp = [];

    for (let j = 0; j < ans?.length; j++) {
      console.log(ans[j].textAnswers);
      temp.push(ans[j].textAnswers.answers[0].value);
    }
    answers.push(temp);
  }
  return answers;
};

const extractRubricData = (data) => {
  let questions = [];

  let rubrics = {};

  data?.forEach((q) => {
    if (q[0] === "Questions[MAX_MARK]") {
      console.log(null);
    } else {
      if (q[0] !== "-") {
        if (rubrics["question"]) {
          questions.push(rubrics);
        }
        rubrics = {};
        rubrics["question"] = q[0];
        rubrics["criteria"] = [];
        rubrics["marks"] = [];
      }

      rubrics["criteria"].push(q[2]);
      rubrics["marks"].push(q[3]);
    }
  });

  if (rubrics["question"]) questions.push(rubrics);

  return questions;
};

const extractRawSheetData = async (auth, spreadSheetId, range) => {
  const sheets = google.sheets({ version: "v4", auth });
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId: spreadSheetId,
    range: "Sheet1",
  });
  // TODO: try sheet1 as range and then remove the first row
  console.log(res.data.values);

  return res.data.values;
};

const ExtractStudentSheetData = async (googleId, accessToken, sheetLink) => {
  const spreadSheetID = extractSheetId(sheetLink);
  const auth = await authorize(accessToken);

  const data = await extractRawSheetData(auth, spreadSheetID, "A2:B3");
  let emails = [];

  data?.forEach((element) => {
    if (element[0] === "Name") {
      console.log(null);
    } else {
      emails.push(element[1]);
    }
  });

  return emails;
};

const ExtractRubricSheetData = async (googleId, accessToken, sheetLink) => {
  const spreadSheetID = extractSheetId(sheetLink);
  const auth = await authorize(accessToken);

  const data = await extractRawSheetData(auth, spreadSheetID, "A2:D7");
  const extractedData = extractRubricData(data);

  return extractedData;
};

const createMarkSheet = async (
  accessToken,
  assessmentId,
  qa,
  extractedData
) => {
  try {
    // Create the sheet

    const auth = await authorize(accessToken);
    const sheets = google.sheets({ version: "v4", auth });

    let spreadsheetId, markSheetUrl;
    const assessmentData = await Assessment.findById(assessmentId);
    // console.log(assessmentData);

    if (assessmentData?.marksheetData) {
      console.log("Updating Marks Spread sheet!");
      if (!qa) {
        console.log("No Response From The Google Form Yet!");
        return;
      }

      const qs = qa.question;
      const ans = qa.answer;

      const mappedAnswers = [];
      ans.forEach((values, keys) => {
        const temp = [];

        qs.forEach((v, k) => {
          const answer = values.get(k);
          temp.push({ ques: v, ans: answer });
        });

        mappedAnswers.push(temp);
      });

      // console.log(mappedAnswers);

      // Google Sheet Headers [mail, marksq1, marksq2 ...., marksqn, total]
      const headers = [];
      headers.push("mail");

      for (let i = 1; i < qs.size; i++) {
        headers.push("mark_q" + i);
      }

      headers.push("total");

      // const rubricAnalysis = await criteria_based_grading(mappedAnswers, extractedData);
      const rubricAnalysis = []; // For testing without LLM
      console.log(rubricAnalysis);

      // Update
      spreadsheetId = assessmentData.marksheetData.data.spreadsheetId;

      // Add the Student Marks Data
      const sheetBody = {
        values: [headers, ...rubricAnalysis],
      };

      const sheetCreationResponse = await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: "Sheet1",
        valueInputOption: "RAW",
        resource: sheetBody,
      });

      console.log("Sheet updated successfully.");

      // Save Spread Sheet Data
      const obj = {
        data: sheetCreationResponse.data,
        url: sheetCreationResponse.request.responseURL,
      };

      markSheetUrl = sheetCreationResponse.request.responseURL;

      await Assessment.updateOne(
        {
          _id: assessmentData._id,
        },
        {
          $set: {
            marksheetData: obj,
          },
        }
      );

      // console.log(sheetCreationResponse.data);
    } else {
      console.log("Creating Marks Spread Sheet");
      const spreadsheet = await sheets.spreadsheets.create({
        resource: {
          properties: {
            title: "Mark Sheet" + assessmentId,
          },
        },
        fields: "spreadsheetId",
      });

      spreadsheetId = spreadsheet.data.spreadsheetId;
      const obj = {
        data: spreadsheet.data,
        url: spreadsheet.request.responseURL,
      };
      markSheetUrl = "https://docs.google.com/spreadsheets/d/" + spreadsheet.data.spreadsheetId;
      await Assessment.updateOne(
        {
          _id: assessmentData._id,
        },
        {
          $set: {
            marksheetData: obj,
          },
        }
      );

      console.log("Sheet created successfully.");
    }

    return markSheetUrl;
  } catch (error) {
    console.log("Error while creating sheet for marks: ", error);
  }
};

const criteria_based_grading = async (studentResponses, questions) => {
  const BASE_API_URL = "http://127.0.0.1:5000";
  const response = [];

  for (const [studentIndex, responses] of studentResponses.entries()) {
    let obtainedTotal = 0;
    // Map each student's responses
    const response_object = {};
    const data = [];

    responses.forEach((value, key) => {
      response_object[value.ques] = value.ans;
    });

    // Push the Mail
    const mail =
      response_object[
        "Please Enter Your Email. This will be used for grading or else your marks will be lost"
      ];
    data.push(mail);

    // Map each question for criteria
    for (const [questionIndex, question] of questions.entries()) {
      const ans = response_object[question.question];

      const criterias = question.criteria; // Array for the Criteria
      const marks = question.marks; // Array for the marks of each criteria
      const questionData = []; // Store data for this question

      // total = 0
      let questionTotal = 0;

      // Process each criteria asynchronously
      for (const [criteriaIndex, val] of criterias.entries()) {
        const max_mark = Math.floor(marks[criteriaIndex]);
        console.log("Maximum Mark: ", max_mark);
        const request = {
          solution: ans,
          criteria: val,
        };

        // Marking Processing Using the LLM
        const res = await axios.post(
          BASE_API_URL + "/rag_gemma_assessment",
          request
        );
        const llm_decision = res?.data;

        console.log("LLM Decision: ", llm_decision);

        let obtained_mark = 0;

        if (llm_decision === 1) {
          obtained_mark = Math.floor(max_mark);
        } else if (llm_decision === 0) {
          obtained_mark = 0;
        } else obtained_mark = Math.floor(max_mark / 2);

        console.log(`Criteria: ${val}, mark: ${obtained_mark}`);

        // Add obtained marks to the total marks for each question
        questionTotal += obtained_mark;
        questionData.push(obtained_mark); // Add obtained mark to question data
      }

      // All criteria processed, Sum the marks
      obtainedTotal += questionTotal;
      data.push(questionTotal); // Summation of all criteria marks for each question
    }
    // Add the total mark
    data.push(obtainedTotal);
    response.push(data);
  }
  console.log(response);
  return response;
};

module.exports = {
  ExtractStudentSheetData,
  ExtractRubricSheetData,
  createMarkSheet,
};
