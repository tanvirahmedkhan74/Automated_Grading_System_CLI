import chalk from "chalk";
import inquirer from "inquirer";
import axios from "axios";
import FormData from "form-data";
import { LocalStorage } from "node-localstorage";
import fs from "fs/promises";
import path from "path";

export async function Assessment(user, args) {
  const formData = new FormData();
  formData.append("_id", "");
  formData.append("title", args[0] || "");
  formData.append("description", "");
  formData.append("rubricLink", args[1] || "");
  formData.append("studentInfoLink", args[2] || "");
  formData.append("startDate", "");
  formData.append("endDate", "");
  formData.append("update", "false");

  try {
    let directory = args[3];
    const parentdir = process.cwd();
    const absolute_dir = path.resolve(parentdir, directory);

    // Validate the directory existence and read access
    try {
      await fs.access(absolute_dir, fs.constants.F_OK | fs.constants.R_OK);
    } catch (err) {
      if (err.code === "ENOENT") {
        console.error(
          `Path "${absolute_dir}" does not exist or is not readable.`
        );
      } else {
        console.error(`Error accessing directory "${absolute_dir}":`, err);
      }
      return []; // Return an empty array on error
    }

    // Read the files for the directory
    const dirents = await fs.readdir(absolute_dir);
    console.log(absolute_dir);
    // Map all the files into the array and filter PDFs
    const files = await Promise.all(
      dirents.map(async (dirent) => {
        const filePath = path.join(absolute_dir, dirent);
        const stats = await fs.stat(filePath);
        if (stats.isFile() && path.extname(filePath).toLowerCase() === ".pdf") {
          return filePath;
        }
        return null;
      })
    );

    const filtered_files = files.filter(Boolean);
    console.log(filtered_files);

    for (let i = 0; i < filtered_files.length; i++) {
      formData.append("pdfs", filtered_files[i]);
    }

    try {
      const response = await axios.post(
        `http://localhost:8000/db/saveAssessment/${user.googleId}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log(
        chalk.green(
          `Assessment Created Successfully!\nMarksheet Link: ${response?.data.message}`
        )
      );
    } catch (error) {
      console.error(chalk.red("Error creating assessment:", error));
    }
  } catch (err) {
    console.log("Error uploading files!", err);
  }
}

async function getPdfFiles(directory) {
  // Get the absolute file path
  const parentdir = process.cwd();
  const absolute_dir = path.resolve(parentdir, directory);

  // Validate the directory existence and read access
  try {
    await fs.access(absolute_dir, fs.constants.F_OK | fs.constants.R_OK);
  } catch (err) {
    if (err.code === "ENOENT") {
      console.error(
        `Path "${absolute_dir}" does not exist or is not readable.`
      );
    } else {
      console.error(`Error accessing directory "${absolute_dir}":`, err);
    }
    return []; // Return an empty array on error
  }

  // Read the files for the directory
  const dirents = await fs.readdir(absolute_dir);

  // Map all the files into the array and filter PDFs
  const files = await Promise.all(
    dirents.map(async (dirent) => {
      const filePath = path.join(absolute_dir, dirent);
      const stats = await fs.stat(filePath);
      if (stats.isFile() && path.extname(filePath).toLowerCase() === ".pdf") {
        return filePath;
      }
      return null;
    })
  );

  return files.filter(Boolean); // Remove null values (excluded non-PDF items)
}

// @Deprecated Function
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
          const assessArr = [];

          // Iterating Each Assessment
          assessments.forEach((assessment, key) => {
            console.log(
              chalk.blue(
                key,
                ": ",
                assessment.title,
                "     ",
                assessment.marksheetData?.url
              )
            );
            keyArr.push(key);
            assessArr.push(assessment);
          });

          // Prompting for choosing an assessment
          inquirer
            .prompt([
              {
                type: "list",
                name: "action",
                message: chalk.cyan("Update an Assessment"),
                choices: keyArr,
              },
            ])
            .then((answer) => {
              // Update the assessment

              const assessment = assessArr[answer.action];
              if (assessment) {
                const formData = new FormData();
                formData.append("_id", assessment._id || "");
                formData.append("title", assessment.title || "");
                formData.append("description", assessment.description || "");
                formData.append("rubricLink", assessment.rubricLink || "");
                formData.append(
                  "studentInfoLink",
                  assessment.studentInfoLink || ""
                );
                formData.append(
                  "startDate",
                  assessment.startDate.substring(0, 10) || ""
                );
                formData.append(
                  "endDate",
                  assessment.endDate.substring(0, 10) || ""
                );
                formData.append("update", "true");

                // POST request for updating the assessnebt
                axios
                  .post(
                    `http://localhost:8000/db/saveAssessment/${user.googleId}`,
                    formData,
                    { headers: { "Content-Type": "multipart/form-data" } }
                  )
                  .then((response) => {
                    console.log(
                      chalk.green(
                        "Update Success! Check the sheet link after 10 minutes"
                      )
                    );
                    resolve(); // Resolve after processing
                  })
                  .catch((error) => {
                    console.error(
                      chalk.red("Error updating assessments:", error)
                    );
                    reject(error); // Reject on error
                  });
              }
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
