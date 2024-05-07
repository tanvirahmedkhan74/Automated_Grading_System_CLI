import chalk from "chalk";
import inquirer from "inquirer";
import axios from "axios";
import { LocalStorage } from "node-localstorage";

export function Assessment(user) {
  // const user = localStorage.getItem('user'); // Assuming user data is stored in localStorage
  // if (!user) {
  //   console.error(chalk.red("Error: User data not found. Please authenticate first."));
  //   return;
  // }

  return inquirer.prompt([
    {
      type: "list",
      name: "action",
      message: chalk.cyan("What do you want to do?"),
      choices: ["Create New Assessment", "Fetch Existing", "Exit"],
    },
  ]).then((answer) => {
    switch (answer.action) {
      case "Create New Assessment":
        return createAssessment(user.accessToken);
      case "Fetch Existing":
        return fetchExistingAssessments(user);
      case "Exit":
        console.log(chalk.redBright("Good Bye!"));
        return Promise.resolve(); // Resolve with no value for Exit
      default:
        console.error(chalk.red("Invalid option. Please choose 0 or 1."));
        return Promise.reject(new Error("Invalid user choice")); // Handle error
    }
  });
}

function createAssessment(token) {
  // Implement logic to inquire about title, links, directory, etc.
  // ... your code to get assessment details ...

  return new Promise((resolve) => {
    console.log(chalk.green("New Assessment created successfully!")); // Replace with actual creation logic
    resolve();
  });
}

function fetchExistingAssessments(user) {
  return new Promise((resolve, reject) => {
    axios
      .get(`http://localhost:8000/db/getAssessments/${user.googleId}`)
      .then((response) => {
        const assessments = response.data;
        if (assessments.length === 0) {
          console.log(chalk.yellow("No existing assessments found."));
        } else {
          console.log(chalk.magenta("Your Existing Assessments:"));

          // Storing Key and Assessments
          const keyArr = [];
          const assessArr = []

          // Iterating Each Assessment
          assessments.forEach((assessment, key) => {
            console.log(chalk.blue(key,": ",assessment.title, "     ", assessment.marksheetData?.url));
            keyArr.push(key);
            assessArr.push(assessment);
        });
        
        // Prompting for choosing an assessment
        inquirer.prompt([
            {
              type: "list",
              name: "action",
              message: chalk.cyan("Update an Assessment"),
              choices: keyArr,
            },
          ]).then((answer) => {
            console.log(assessArr[answer.action]);
          });
          
        }
        resolve(); // Resolve after processing
      })
      .catch((error) => {
        console.error(chalk.red("Error fetching assessments:", error.message));
        reject(error); // Reject on error
      });
  });
}
