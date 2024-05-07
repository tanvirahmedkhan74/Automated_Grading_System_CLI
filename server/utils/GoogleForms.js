const { google } = require('googleapis');
const authorize = require('../config/sheets');
const Assessment = require('../models/Assessement');

const createItemRequests = (question, loc) => {
    const update = 
        {
            createItem: {
              item: {
                title: question,
                description: 'Answer Briefly',
                questionItem:{
                    question: {
                        textQuestion:{
                            paragraph: true
                        }
                    }
                }
              },
              location: {
                index: loc,
              },
            },
        };
    return update;
}
//  @desc   Create Google Form For the Students
//  @params Google auth token, question [], Assessment Data, batch update ? true : false
const createGoogleForm = async (accessToken, questions, formInfo, batch) => {
    const auth = await authorize(accessToken);
    const google_forms = google.forms({ version: 'v1', auth: auth });

    let formDatas;
    let requests = []
    const questionItems = [];

    const update =
        {
            updateFormInfo: {
              info: {
                description:
                  formInfo.description
              },
              updateMask: 'description',
            },
        };

    requests.push(update);
    
    // Add the question for email
    const identifying_question = createItemRequests("Please Enter Your Email. This will be used for grading or else your marks will be lost", 0);
    requests.push(identifying_question);

    questions.forEach((q) => {
        let idx = 1;
       const req = createItemRequests(q.question, idx);
       idx += 1;

       requests.push(req);
    });

    const newForm = {
        info: {
            title: formInfo.title,
            documentTitle: formInfo.title
        },
    };

    try {
        const assess = await Assessment.findOne({_id: formInfo?._id});
        
        if(assess.googleFormData?.formId){
            formDatas = assess.googleFormData;
            console.log('Already Form Available');
        }else{
            console.log('Creating New Google Form');

            const res = await google_forms.forms.create({
                requestBody: newForm,
            });

            formDatas = res.data;

            if(batch){
                const batchUpdateResponse = await google_forms.forms.batchUpdate({
                    formId: formDatas.formId,
                    requestBody: {requests}
                })
            
                console.log(batchUpdateResponse);
            }
        }
    } catch (error) {
        console.log('Error while creating Google Form: ', error);
    }

    // console.log(requests);
    return formDatas;

};

const getGoogleFormResponse = async (formId, accessToken) => {
    const auth = await authorize(accessToken);
    const google_forms = google.forms({ version: 'v1', auth: auth });

    try {
        const res = await google_forms.forms.responses.list({
            formId: formId
        })
        return res.data;
    } catch (error) {
        console.log('Error while retrieving Google Form Response: ', error);
    }
}

const saveAnswerResponse = async (formResponse, assessmentId, formId, accessToken) => {
    // Save Response to DB
    const res = await formResponse?.responses;
        
    // Get Form Content
    const auth = await authorize(accessToken);
    const google_form = google.forms({version: 'v1', auth: auth});

    const ques = await google_form.forms.get({formId: formId});

    try{
        // Update Assessment with studentFormData
        const response = await Assessment.updateOne({
            _id: assessmentId,
          }, {
            $set: {
              studentFormData: res,
              googleFormQuestions: ques.data.items
            }
          });
        
          return response;
    }catch(error){
        console.log('Error while Saving Google Forms Answer Data: ', error);
    }
}

// Param        - Id of the assessment
// Return       - Object of two Map object
const mappedQuestionAnswers = async (assessmentId, goMap) => {
    if(!goMap) return;

    try {
        // Fetch Assessment data from DB
        const data = await Assessment.find({_id: assessmentId});
        
        if(data[0].googleFormQuestions){
            const questions = data[0].googleFormQuestions;
            const answers = data[0].studentFormData;

            const questionMap = new Map();
            
            // [Question id ==> title]
            questions?.forEach((item, key) => {
                questionMap.set(item.questionItem.question.questionId, item.title);
            })

            const answerMap = new Map();
            answers?.forEach(answerObject => {
                const responseId = answerObject.responseId;
                const individualAnswers = answerObject.answers;

                const temp_map = new Map();
                Object.keys(individualAnswers).forEach(questionId => {
                    const questionValue = individualAnswers[questionId].questionId;
                    const answerValue = individualAnswers[questionId].textAnswers.answers[0].value;
                    temp_map.set(questionValue, answerValue);
                });
                answerMap.set(responseId, temp_map);
            });

            // console.log(answerMap);

            // console.log(questionMap);

            return {question: questionMap, answer: answerMap}
        }
        
    } catch (error) {
        console.log(error);
    }
}

module.exports = { createGoogleForm, getGoogleFormResponse, saveAnswerResponse, mappedQuestionAnswers };