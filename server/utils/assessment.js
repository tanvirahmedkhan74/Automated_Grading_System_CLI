const { ExtractStudentSheetData, ExtractRubricSheetData, createMarkSheet } = require('./GoogleSheet');
const { createGoogleForm, getGoogleFormResponse, saveAnswerResponse, mappedQuestionAnswers } = require('./GoogleForms');
const Assessment = require('../models/Assessement');
const SendFormLinkMail = require('./Gmail');

//  @desc   Create Assessment and Form Link
//  @params googel Id, Google auth accesss token, DB object for the current assessment
const createAssessment = async (googleId, accessToken, assessmentData) =>  {
    // Extract Sheet Links
    const studentData = await ExtractStudentSheetData(googleId, accessToken, assessmentData.studentInfoLink);
    const rubricData = await ExtractRubricSheetData(googleId, accessToken, assessmentData.rubricLink); 
    const googleForm = await createGoogleForm(accessToken, rubricData, assessmentData, true);
    try{
        // Update Assessment with googleFormData
        const response = await Assessment.updateOne({
            _id: assessmentData._id,
          }, {
            $set: {
              googleFormData: googleForm,
            }
        });

        // Send Mail {Commenting it for not spamming with mail while in dev}
        const formUri = googleForm.responderUri;
        const sendMail = await SendFormLinkMail(accessToken, studentData, formUri);
        // const googleFormResponses = await getGoogleFormResponse(googleForm.formId, accessToken);
        // const answerResponse = await saveAnswerResponse(googleFormResponses, assessmentData._id, googleForm.formId, accessToken);
        const question_answers = await mappedQuestionAnswers(assessmentData._id, false);
        const markSheet = await createMarkSheet(accessToken, assessmentData._id);

        console.log(markSheet);
        return markSheet;
    }catch(error){
        console.log('Error while Saving New Google Form Data: ', error);
    }
}

//  @desc   Update Assessment and Form Link
//  @params googel Id, Google auth accesss token, DB object for the current assessment
const updateAssessment = async (googleId, accessToken, assessmentData) =>  {
  // Extract Sheet Links
  const studentData = await ExtractStudentSheetData(googleId, accessToken, assessmentData.studentInfoLink);
  const rubricData = await ExtractRubricSheetData(googleId, accessToken, assessmentData.rubricLink); 
  const googleForm = await createGoogleForm(accessToken, rubricData, assessmentData, false);

  try{
      // Update Assessment with googleFormData
      const response = await Assessment.updateOne({
          _id: assessmentData._id,
        }, {
          $set: {
            googleFormData: googleForm,
          }
        });

      // Send Mail {Commenting it for not spamming with mail while in dev}
      const formUri = googleForm.responderUri;
      // const sendMail = await SendFormLinkMail(accessToken, studentData, formUri);
      const googleFormResponses = await getGoogleFormResponse(googleForm.formId, accessToken);
      const answerResponse = await saveAnswerResponse(googleFormResponses, assessmentData._id, googleForm.formId, accessToken);
      const question_answers = await mappedQuestionAnswers(assessmentData._id, true);
      const markSheet = await createMarkSheet(accessToken, assessmentData._id, question_answers, rubricData);

      console.log(markSheet);
  }catch(error){
      console.log('Error while Saving New Google Form Data: ', error);
  }
}

module.exports = {createAssessment, updateAssessment};