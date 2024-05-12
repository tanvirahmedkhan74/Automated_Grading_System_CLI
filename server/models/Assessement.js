const mongoose = require('mongoose');

const AssessmentSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
    },
    description: {
        type: String,
    },
    googleId: {
        type: String,
        required: true,
    },
    startDate: {
        type: Date,
    },
    endDate: {
        type: Date,
    },
    rubricLink: {
        type: String,
        required: true,
    },
    studentInfoLink: {
        type: String,
        required: true,
    },
    marksheetData: {
        type: Object,
        default: null,
    },
    googleFormData: {
        type: Object,
        default: null,
    },
    // Additional information collected from the Google Form
    studentFormData: {
        type: Object,
        default: {},
    },
    // Assessment results (score, feedback)
    googleFormQuestions: {
        type: Object,
        default: {},
    },
    pdfs: {
        type: Array,
        default: []
    }
});

module.exports = mongoose.model('Assessment', AssessmentSchema);
