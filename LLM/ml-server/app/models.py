from transformers import AutoTokenizer, pipeline, BitsAndBytesConfig

import json, re
from .training_data import data
from .Prompts_1 import prompts
from .final_prompts import prompts as final_prompt


class Assessment:
    def __init__(self, model_name, AutoModel, task):
        self.local_model_directory = "/home/tanvir/Academics/NSU/CSE299/Automated_Grading_System/LLM/Model/" + model_name
        self.token = "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"

        self.model_name = model_name
        self.AutoModel = AutoModel
        self.task = task

        self.save_model()

        # set the model and tokenizer
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        self.model = AutoModel.from_pretrained(self.local_model_directory, token=self.token)
        self.tokenizer = AutoTokenizer.from_pretrained(self.local_model_directory, token=self.token,
                                                       quantization_config=quantization_config)

        return

    def save_model(self):
        # load model from huggingFace
        model = self.AutoModel.from_pretrained(self.model_name, token=self.token)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)

        # save the model
        model.save_pretrained(self.local_model_directory)
        tokenizer.save_pretrained(self.local_model_directory)

    def rubric_assessment(self, criteria: str, answer: str):
        prompt = "Assess the 'Context' on a scale from 0 to 10 according to the 'Criteria' provided, in a json format with only key 'rating'."

        qa_input = f"Criteria: {criteria}, Context: {answer}, Gemma's Task: {prompt}"
        input_ids = self.tokenizer(qa_input, return_tensors="pt")

        outputs = self.model.generate(**input_ids, max_new_tokens=500)

        res = self.tokenizer.decode(outputs[0])

        # clean output
        json_out = res.split("\n\n")[1]
        json_out = json_out.split("<")[0]

        # Clean Result
        res = json_out
        print(res)
        # Remove non-numeric characters and extract the first integer
        match = re.search(r"\d+", res)
        if match:
            first_integer = int(match.group())
        else:
            first_integer = None

        return first_integer

    def gemma_rubric_assessment(self, criteria: str, answer: str, prompt: str):

        qa_input = f"Criteria: {criteria}, Context: {answer}, Gemma's Task: {prompt}"
        input_ids = self.tokenizer(qa_input, return_tensors="pt")

        outputs = self.model.generate(**input_ids, max_new_tokens=500)

        res = self.tokenizer.decode(outputs[0])

        # clean output
        json_out = res.split("\n\n")[1]
        json_out = json_out.split("<")[0]
        # if json_out:
        #     json_final = json.loads(json_out)
        #     return json_final
        # else:
        #     return json_out
        return json_out

    def gemma_rubric_assessment_cot(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(**input_ids, max_new_tokens=300)

        res = self.tokenizer.decode(outputs[0])

        # clean result
        output = res.split("Output")[-1]

        # Mark the ranking
        rankings = ["mastery", "proficiency", "competence", "no pass", "not submitted"]

        final_ranking = "null"

        for rank in rankings:
            if rank in output.lower():
                final_ranking = rank
                break

        return final_ranking

    def gemma_rubric_assessment_rag(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(**input_ids, max_new_tokens=1000)

        res = self.tokenizer.decode(outputs[0])

        return res

    def gemma_rubric_assessment_test_w7(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(**input_ids, max_new_tokens=500)

        res = self.tokenizer.decode(outputs[0])
        # clean result
        output = res.split("Output")[-1]
        explanation = output.split("Explanation")
        ans = ''
        exp = ''

        if len(explanation) > 1:
            ans = explanation[0]
            exp = explanation[1]

            start_index = ans.find(':') + 2  # Find the start index of the result value
            end_index = ans.find('\n')  # Find the end index of the result value
            ans = ans[start_index:end_index].strip()  # Extract the result value
        else:
            ans = output

        return ans, exp

    def gemma_rag_assessment(self, criteria, solution, relevant_context):
        """Evaluates the student's solution using Retrieval-Augmented Generation (RAG) with BERT-2b-it.

        Args:
            criteria: The criteria text for the RAG system (one or two sentences).
            solution: The student's solution text.
            relevant_context: The Relevant Sentences for RAG

        Returns:
            A string indicating whether the solution fulfills the criteria or not (e.g., "YES" or "NO").
        """

        # Join relevant context text for the prompt
        joined_relevant_context = "\n".join(relevant_context)

        p = """<**Instruction**> I will provide you with a `<Student's Solution>`, `<criteria>`, and relevant context snippets in `<Context>`. Your task is to evaluate the solution based on the following steps:
        
1. **Contextual Verification:** Analyze the provided context and assess the factual accuracy and validity of the information it presents. Look for inconsistencies or contradictions within the context itself.
2. **Solution-Context Alignment:** Evaluate how well the student's solution aligns with the verified context. Does the solution accurately describe functionalities or concepts mentioned in the context? Are there any conflicts between the solution and the factual information gleaned from the context?
3. **Criteria Fulfillment:** Based on your understanding of the verified context, assess if the student's solution meets the specified criteria. Does the solution address all aspects of the criteria, or are there any missing elements?

**Output:** Based on the evaluation steps above, generate a response of either '<**Output**> YES' or '<**Output**> NO'.
"""
        prompt = f"{p}\n <criteria>: {criteria} \n <Student's Solution>: {solution}. \n<Context> : {joined_relevant_context}"

        result = self.gemma_rubric_assessment_rag(prompt)

        # Output Formatting
        output = result.split("Output")[-1]

        text = output.upper()  # Convert text to uppercase for case-insensitive search
        if "YES" in text:
            return 1
        elif "NO" in text:
            return 0
        else:
            return -1

    def generate_report_w2(self):
        prompts = [
            "Assess the 'Context' on a scale from 0 to 10 according to the 'Criteria' provided, in a json format with only key 'rating'.",
            "Rate the 'Context' between 0 and 10 based on the 'Criteria' outlined, in a json format with only key 'rating'.",
            "Evaluate the 'Context' with a rating from 0 to 10 as per the 'Criteria' given, in a json format with only key 'rating'.",
            "Provide a rating of the 'Context' from 0 to 10 in alignment with the 'Criteria' specified, in a json format with only key 'rating'.",
            "Judge the 'Context' on a scale of 0 to 10 considering the 'Criteria' presented, in a json format with only key 'rating'.",
            "Appraise the 'Context' using the 'Criteria' given, with a rating from 0 to 10, in a json format with only key 'rating'.",
            "Determine the 'Context' score from 0 to 10 based on the 'Criteria' provided, in a json format with only key 'rating'.",
            "Assign a score of 0 to 10 to the 'Context' according to the 'Criteria' detailed, in a json format with only key 'rating'.",
            "Examine the 'Context' and rate it between 0 and 10, following the 'Criteria' outlined, in a json format with only key 'rating'.",
            "Provide a rating between 0 and 10 for the 'Context' based on the 'Criteria' provided, in a json format with only key 'rating'.",
            "Analyze the 'Context' and provide a rating from 0 to 10 based on the 'Criteria' provided, in a json format with only key 'rating'.",
            "Review the 'Context' against the 'Criteria' provided and rate it on a scale of 0 to 10, in a json format with only key 'rating'.",
            "Gauge the 'Context' based on the 'Criteria' provided, assigning a rating from 0 to 10, in a json format with only key 'rating'.",
            "Examine the 'Context' as per the 'Criteria' provided and provide a rating between 0 and 10, in a json format with only key 'rating'.",
            "Rate the 'Context' from 0 to 10 considering the 'Criteria' outlined for assessment, in a json format with only key 'rating'.",
            "Evaluate the 'Context' and assign a score from 0 to 10 based on the 'Criteria' provided, in a json format with only key 'rating'.",
            "Rate the 'Context' based on the 'Criteria' provided, assigning a score between 0 and 10, in a json format with only key 'rating'.",
            "Assess the 'Context' with a rating from 0 to 10, considering the 'Criteria' provided, in a json format with only key 'rating'.",
            "Determine the 'Context' score based on the 'Criteria' provided, rating it from 0 to 10, in a json format with only key 'rating'.",
            "Score the 'Context' from 0 to 10, considering the 'Criteria' provided for evaluation, in a json format with only key 'rating'."
        ]

        final_result = []
        ques_count = 0
        prompt_count = 0
        for prp in prompts:
            results = []
            mark_result = []
            prompt_count += 1
            curr_prompt = prp
            for obj in data:
                curr_ques = 'NOPE'
                if obj['question']:
                    curr_ques = obj['question']
                ques_count += 1
                levels = obj['levels']

                for level in levels:
                    curr_criteria = level['criteria']
                    curr_answer = level['answer']
                    curr_level = level['level']
                    curr_mark = level['mark']

                    # answer = curr_answer.replace('\n', '').strip()
                    cleaned_answer = re.sub('\s+', ' ', curr_answer).strip()

                    llm_result = self.gemma_rubric_assessment(criteria=curr_criteria, answer=cleaned_answer,
                                                              prompt=curr_prompt)

                    json_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'prompt': curr_prompt,
                        'question': curr_ques,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'answer': cleaned_answer,
                        'mark': curr_mark,
                        'result': llm_result
                    }

                    json_mark_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'result': llm_result
                    }

                    results.append(json_out)
                    mark_result.append(json_mark_out)

                    print(json_mark_out)

                # Save results to a JSON file ''''''"""""""""
            json_file_name = f"report{prompt_count}.json"
            json_file_name_2 = f"mark_report{prompt_count}.json"

            with open(json_file_name, 'w') as outfile:
                json.dump(results, outfile, indent=4)  # Add indentation for readability

            with open(json_file_name_2, 'w') as outfile:
                json.dump(mark_result, outfile, indent=4)  # Add indentation for readability

            ques_count = 0
            final_result.append(results)
        return final_result

    def generate_report_w3(self):
        final_result = []
        ques_count = 0
        prompt_count = 0
        for prp in prompts:
            results = []
            mark_result = []
            prompt_count += 1
            curr_prompt = prp
            for obj in data:
                curr_ques = 'NOPE'
                if obj['question']:
                    curr_ques = obj['question']
                ques_count += 1
                levels = obj['levels']

                for level in levels:
                    curr_criteria = level['criteria']
                    curr_answer = level['answer']
                    curr_level = level['level']
                    curr_mark = level['mark']

                    # answer = curr_answer.replace('\n', '').strip()
                    cleaned_answer = re.sub('\s+', ' ', curr_answer).strip()

                    queue = f"{curr_prompt} \n <Criteria>: {curr_criteria} \n<Student's Solution>: {curr_answer}"
                    llm_result = self.gemma_rubric_assessment_cot(queue)

                    json_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'prompt': curr_prompt,
                        'question': curr_ques,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'answer': cleaned_answer,
                        'mark': curr_mark,
                        'result': llm_result
                    }

                    json_mark_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'result': llm_result
                    }

                    results.append(json_out)
                    mark_result.append(json_mark_out)

                    print(json_mark_out)

                # Save results to a JSON file ''''''"""""""""
            json_file_name = f"report{prompt_count}.json"
            json_file_name_2 = f"mark_report{prompt_count}.json"

            with open(json_file_name, 'w') as outfile:
                json.dump(results, outfile, indent=4)  # Add indentation for readability

            with open(json_file_name_2, 'w') as outfile:
                json.dump(mark_result, outfile, indent=4)  # Add indentation for readability

            ques_count = 0
            final_result.append(results)
        return final_result

    def generate_report_w7(self):
        final_result = []
        ques_count = 0
        prompt_count = 0
        for prp in final_prompt:
            results = []
            mark_result = []
            prompt_count += 1
            curr_prompt = prp
            for obj in data:
                curr_ques = 'NOPE'
                if obj['question']:
                    curr_ques = obj['question']
                ques_count += 1
                levels = obj['levels']

                for level in levels:
                    curr_criteria = level['criteria']
                    curr_answer = level['answer']
                    curr_level = level['level']
                    curr_mark = level['mark']

                    # answer = curr_answer.replace('\n', '').strip()
                    cleaned_answer = re.sub('\s+', ' ', curr_answer).strip()

                    queue = f"{curr_prompt} \n <criteria>: {curr_criteria} \n<Student's Solution>: {curr_answer}.\n Start your generated answer with the word `<**Output**>`"
                    llm_result, llm_explanation = self.gemma_rubric_assessment_test_w7(queue)

                    json_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'prompt': curr_prompt,
                        'question': curr_ques,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'answer': cleaned_answer,
                        'mark': curr_mark,
                        'result': llm_result,
                        'explanation': llm_explanation
                    }

                    json_mark_out = {
                        'prompt_no': prompt_count,
                        'question_no': ques_count,
                        'level': curr_level,
                        'criteria': curr_criteria,
                        'result': llm_result
                    }

                    results.append(json_out)
                    mark_result.append(json_mark_out)

                    print(json_mark_out)

                # Save results to a JSON file ''''''"""""""""
            json_file_name = f"report{prompt_count}.json"
            json_file_name_2 = f"mark_report{prompt_count}.json"

            with open(json_file_name, 'w') as outfile:
                json.dump(results, outfile, indent=4)  # Add indentation for readability

            with open(json_file_name_2, 'w') as outfile:
                json.dump(mark_result, outfile, indent=4)  # Add indentation for readability

            ques_count = 0
            final_result.append(results)
        return final_result
