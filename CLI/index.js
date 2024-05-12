#!/usr/bin/env node

import { program } from "commander";
import chalk from "chalk";
import inquirer from "inquirer";
import spawnCommand from "spawn-command";
import figlet from "figlet";
import axios from "axios";
import { LocalStorage } from "node-localstorage";
import jwt from "jsonwebtoken";
import { Assessment } from "./utils/Assessments.js";
import ora from "ora";

import { backendServer, llmServer } from "./utils/RunServer.js";

const localStorage = new LocalStorage("./scratch");

program
  .version("1.0.0")
  .description("Automated Grading System CLI")
  .argument("<assessment_name>", "Name of the Assessment")
  .argument("<rubric_sheet_link>", "Google sheet link for the rubrics")
  .argument("student_sheet_link", "Google sheet link of thee students")
  .argument(
    "<RAG_directory>",
    "Directory containing PDF files for the assessment"
  )
  .action(
    async (assessmentName, rubricSheetLink, studentSheetLink, RAGDirectory) => {
      const args = [assessmentName, rubricSheetLink, studentSheetLink, RAGDirectory];
      // Logo
      console.log(
        chalk.yellow(figlet.textSync("Skeptic", { horizontalLayout: "full" }))
      );

      try {
        // Google Authentication Process
        const authentication = await getAccessToken(args);
      } catch (err) {
        console.error(chalk.red(err.message));
        process.exit(1);
      }
    }
  );
program.parse(process.argv);

async function getAccessToken(args) {
  try {
    let token;
    // Prompt user to open login link in a browser (interaction assumed)
    console.log(chalk.green("Login to your Google Account First!"));
    console.log(chalk.green("Please open this link in a browser:"));
    console.log(chalk.redBright("http://localhost:8000/auth/google/callback"));

    inquirer
      .prompt([
        {
          type: "input",
          name: "key",
          message: "What is the Secret key after login?",
        },
      ])
      .then(async (answers) => {
        if (answers.key === "ohoo!") {
          token = await axios.get(
            "http://localhost:8000/auth/get_access_token"
          );
          const decoded = jwt.decode(token?.data, process.env.JWT_SECRET_KEY);
          localStorage.setItem("user", decoded);

          // Assessment Starts
          const assessment = await Assessment(decoded.user, args);
        } else {
          console.log("Hmm! Seems like you are not authenticated, BYE");
        }
      });
  } catch (error) {
    console.error(chalk.red("Error:", error.message));
    throw error; // Re-throw for handling in main action
  }
}
