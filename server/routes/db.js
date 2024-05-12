const mongoose = require("mongoose");
const express = require("express");
const router = express.Router();
const User = require("../models/User");
const Assessment = require("../models/Assessement");
const {
  ExtractStudentSheetData,
  ExtractRubricSheetData,
} = require("../utils/GoogleSheet");
const SendFormLinkMail = require("../utils/Gmail");
const { createGoogleForm } = require("../utils/GoogleForms");
const { createAssessment, updateAssessment } = require("../utils/assessment");
const upload = require("../config/multer");
const fs = require("fs/promises");
const pdf = require("pdf-parse");
const { v4: uuidv4 } = require('uuid');
const axios = require('axios');

const extractText = async (filePath) => {
  try {
    const dataBuffer = await fs.readFile(filePath);
    const data = await pdf(dataBuffer);
    
    console.log(data.text);
    return data.text;
  } catch (err) {
    console.error("Error extracting text:", err);
  }
};

// @desc    Get User Deails
// @route   GET /db/getUserById/

router.get("/getUserById/:userId", async (req, res) => {
  // From react, send a googleId and from mongodb send the details to the client side
  try {
    const id = req.params.userId;
    // console.log(id);
    const user = await User.findOne({ googleId: id });

    if (!user) {
      res.status(404).json({ message: "Invalid User Id" });
    } else {
      res.status(200).json(user);
    }
  } catch (error) {
    console.log("Error while retrieving single user: ", error);
  }
});

// @desc    Get User's Assessments
// @route   GET /db/getAssessments/

router.get("/getAssessments/:userId", async (req, res) => {
  try {
    const id = req.params.userId;
    const response = await Assessment.find({ googleId: id });

    if (response) {
      res.status(200).json(response);
    } else {
      res.status(200).json({ message: "No assessment Yet" });
    }
  } catch (error) {
    console.log("Error while retrieving Assessmens: ", error);
  }
});

// @desc    Save new Assessment
// @route   POST /db/saveAssessment/
router.post(
  "/saveAssessment/:userId",
  upload.array("pdfs", 99),
  async (req, res) => {
    // chroma run --path /home/tanvir/.local/bin

    try {
      const id = req.params.userId;

      // Get the Access Token
      const user = await User.findOne({
        googleId: id,
      });
      const accessToken = user.accessToken;

      // Update or Creation
      const assessmentData = req.body;

      console.log(assessmentData);
      const textContents = [];
      // Check For Files
      if (assessmentData?.pdfs) {
        // Create Text Items and send for saving
        const files = assessmentData?.pdfs; // Array of files
        console.log('Requested Files: ', files);

        for (const file of files) {
            const text = await extractText(file);
            textContents.push(text);
        }

        console.log(textContents);
        
        // Add Text Contents to the Vector Database
        const BASE_API_URL = 'http://127.0.0.1:5000';
        const request = {
          'context': textContents
        };
        try {
          const res = await axios.post(BASE_API_URL + "/add-embedded-data", request);
          console.log(res);
        } catch (error) {
          console.log("Error while storing vector embed, ", error)
        }

        console.log(textContents);
      }

      if (assessmentData.update !== 'false') {
        console.log("Updating");
        const response = await Assessment.updateOne(
          {
            _id: assessmentData._id,
          },
          {
            $set: {
              title: assessmentData.title,
              description: assessmentData.description,
              rubricLink: assessmentData.rubricLink,
              studentInfoLink: assessmentData.studentInfoLink,
              startDate: Date(assessmentData.startDate),
              endDate: assessmentData.endDate,
              googleId: id,
            },
            $push: {
              pdfs: { $each: textContents }
            }
          }
        );
        

        if (response) {
          res.status(200).json({ message: "Update Successful!" });
          const updateResponse = updateAssessment(
            id,
            accessToken,
            assessmentData
          );
        } else {
          res.status(200).json({ message: "Assessment creation failed" });
        }
      } else {
        console.log('Creating');
        const response = await Assessment.create({
          title: assessmentData.title,
          description: assessmentData.description,
          rubricLink: assessmentData.rubricLink,
          studentInfoLink: assessmentData.studentInfoLink,
          startDate: Date(assessmentData.startDate),
          endDate: assessmentData.endDate,
          googleId: id,
          pdfs: [...textContents]
        });

        if (response) {
          const data = await Assessment.findById(response._id);

          // res.status(200).json({ message: "Creation Successful" });
          const creationResponse = await createAssessment(id, accessToken, data);
          res.status(200).json({ message: creationResponse });
        } else {
          res.status(200).json({ message: "Assessment creation failed" });
        }
      }
    } catch (error) {
      console.log("Error while Assessment creation: ", error);
    }
  }
);
module.exports = router;
