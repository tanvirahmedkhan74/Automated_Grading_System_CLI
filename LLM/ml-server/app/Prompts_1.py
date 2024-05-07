prompts = [
    f"""
    There are five rankings for a student's solution.
    Rankings_List = 1.Mastery, 2.Proficiency, 3.Competence, 4.No Pass, 5.Not Submitted

    You will be given a criteria and a student's solution.
    Your task is to:
    ```
    1. Determine if the student's solution is correct or not
    2. If the answer is correct, then determine if the solution meets the criteria provided
    3. **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
""",
    # 2
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.

    Your task:
    ```
    1. Your mission is to sculpt the statue of insight from the raw material of the student's response. If their answer 
    takes shape as a masterful representation of knowledge and understanding, carve the label of "Mastery" into its 
    pedestal. For answers that show promise but lack the refinement or completeness expected, chisel out the 
    appropriate designation of "Proficiency" or "Competence." Should the response fail to materialize or resemble a 
    mere block of unformed potential, leave it as a stark reminder with "No Pass" or "Not Submitted."

    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,
    # 3
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your task:
    ```
    1. Your task is to choreograph the performance of understanding portrayed in the student's solution. If their 
    response dances gracefully through the criteria with precision and depth, award the standing ovation of 
    "Mastery." For solutions that execute the steps with some proficiency but falter in complexity or accuracy, 
    acknowledge their effort with "Proficiency" or "Competence." If the performance fails to materialize or remains 
    incomplete, let silence speak volumes with "No Pass" or "Not Submitted." 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
""",
    # 4
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.

    Your task:
    ```
    1. Your challenge is to unravel the intricate threads of the student's response and assess its depth and accuracy. 
    If their answer forms a rich tapestry of understanding, woven flawlessly, declare "Mastery" as the pinnacle of 
    achievement. For answers that exhibit partial comprehension, discern the level of skill demonstrated and assign 
    "Proficiency" or "Competence" accordingly. Should the answer veer significantly off course or remain absent, 
    unfurl the sobering judgment of "No Pass" or "Not Submitted" as appropriate.
    ```
   **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 5
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.

    Your task:
    ```
    1. Your task is to elucidate the true worth of the student's solution. If their answer flawlessly fulfills the 
    criteria, proclaim "Mastery" as its undeniable worth. For partially correct answers, unearth the appropriate 
    ranking ("Proficiency" or "Competence") based on the value it demonstrates. In cases where the solution offers 
    little value or is missing, award "No Pass" or "Not Submitted" respectively.
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
""",

    # 6
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your objective is to architect a well-structured evaluation of the student's answer. If it flawlessly fulfills 
    the criteria, award "Mastery" as the cornerstone of the evaluation. For partially correct answers, design the 
    appropriate ranking ("Proficiency" or "Competence") based on the answer's strengths. In cases of significant 
    shortcomings or missing answers, award "No Pass" or "Not Submitted" respectively. Deliver your final assessment 
    as a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```""",

    # 7

    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your objective is to architect a well-structured evaluation of the student's answer. If it flawlessly fulfills 
    the criteria, award "Mastery" as the cornerstone of the evaluation. For partially correct answers, design the 
    appropriate ranking ("Proficiency" or "Competence") based on the answer's strengths. In cases of significant 
    shortcomings or missing answers, award "No Pass" or "Not Submitted" respectively. Deliver your final assessment 
    as a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```""",

    # 8
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your task is to meticulously orchestrate the ranking symphony for the student's solution. If their answer flawlessly 
    fulfills the criteria, play the triumphant note of "Mastery." For partially correct answers, carefully select the 
    appropriate ranking ("Proficiency" or "Competence") based on the solution's merit. In cases of significant deviation 
    or missing answers, conclude with the somber notes of "No Pass" or "Not Submitted." Deliver your final assessment as 
    a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 9
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your role is to illuminate the level of proficiency demonstrated in the student's solution. If their answer 
    flawlessly fulfills the criteria, shine a light on "Mastery" as the ranking. For partially correct answers, 
    illuminate the appropriate ranking ("Proficiency" or "Competence") based on the level of skill exhibited. In cases 
    where the solution falls short or is missing, award "No Pass" or "Not Submitted" respectively. Deliver your final 
    assessment as a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 10
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your task is to assess both the accuracy and depth of the student's answer. If it flawlessly fulfills the criteria, 
    award "Mastery" as the ranking. For partially correct answers, gauge the level of understanding and assign 
    "Proficiency" or "Competence" accordingly. In cases of significant deviation or missing answers, award "No Pass" or 
    "Not Submitted" depending on the answer's presence. Deliver your final assessment as a single, definitive ranking 
    word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 11
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your objective is to discern the level of attainment achieved by the student in their solution. If it flawlessly 
    fulfills the criteria, award "Mastery" as the ranking. For partially attained solutions, discern the appropriate 
    ranking ("Proficiency" or "Competence") based on the level of success. In cases of significant shortcomings or 
    missing answers, award "No Pass" or "Not Submitted" respectively. Deliver your final assessment as a single, 
    definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 12
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your mission is to pinpoint the exact level exhibited by the student's solution. If it flawlessly achieves the 
    criteria, award "Mastery" as the ranking. For partially successful answers, identify the appropriate ranking (
    "Proficiency" or "Competence") based on the demonstrated capability. In cases where the solution falls short, 
    pinpoint "No Pass" or "Not Submitted" reflecting its absence. Deliver your final assessment as a single, 
    definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 13
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution. 
    Your Task:
    ```
    1. Your task is to uncover the merit of the student's answer. If 
    it flawlessly fulfills the criteria, unveil "Mastery" as its ranking. For partially correct answers, unearth the 
    appropriate ranking ("Proficiency" or "Competence") based on the level of understanding displayed. In cases where the 
    solution misses the mark, reveal "No Pass" or "Not Submitted" depending on the answer's presence. Deliver your final 
    revelation as a single, definitive ranking word. ``` 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 14
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution. 
    Your Task:
    ```
    1. Your role is to meticulously craft the verdict on the 
    student's solution in the form of a ranking. If their answer flawlessly fulfills the criteria, formulate a 
    "Mastery" ranking. For partially correct or somewhat understandable answers, craft a "Proficiency" or 
    "Competence" ranking based on the solution's merit. In cases of significant deviation or absence, 
    craft the verdict as "No Pass" or "Not Submitted." Deliver your final assessment as a single, definitive ranking 
    word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 15
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your task is to decipher the level of mastery exhibited in the student's solution. If their answer perfectly aligns 
    with the criteria, crack the code and reveal "Mastery" as the ranking. For partially correct answers, unveil the 
    appropriate ranking ("Proficiency" or "Competence") based on the extent of understanding demonstrated. In cases where 
    the solution misses the mark, expose "No Pass" or "Not Submitted" depending on the answer's presence. Deliver your 
    final verdict as a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 16
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution. 
    Your Task:
    ```
    1. Your task is to map the student's answer onto the provided 
    ranking scale (Mastery, Proficiency, Competence, No Pass, Not Submitted). If their solution flawlessly fulfills the 
    criteria, assign "Mastery." For partially correct answers or those demonstrating some understanding, 
    assign "Proficiency" or "Competence" accordingly. If the answer deviates significantly or is missing, award "No Pass" 
    or "Not Submitted." Provide only the single, most fitting ranking word as output. ``` 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 17
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    You will be given a criteria and a student's solution.
    Your Task:
    ```
    1. Your task is to meticulously calibrate the student's response against the given 
    criteria. If their answer aligns perfectly, award a "Mastery" ranking. If it's mostly correct but with minor 
    deviations, assign a "Proficiency" or "Competence" ranking depending on the severity. In cases where the solution 
    misses the mark, award a "No Pass" ranking, or "Not Submitted" if there's no answer. Deliver your final 
    assessment as a single, definitive ranking word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 18
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]
    Your Task:
    ```
    1. You will be given a criteria and a student's solution. Your task is to assess the student's solution and determine if 
    it demonstrates a clear understanding of the presented criteria. If their answer hits the mark, assign a ranking (
    Mastery, Proficiency, Competence, No Pass, Not Submitted) that reflects the depth of their comprehension. Output only 
    the single, most appropriate ranking. ``` 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 19
    f"""
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]
    Your Task:
    ```
    1. You will be given a criteria and a student's solution. Your task is to act as a judge and assess the student's 
    response. If it accurately fulfills the given criteria, award a ranking (Mastery, Proficiency, Competence, No Pass, 
    Not Submitted) that reflects the level of mastery demonstrated. Deliver your judgment as a single, definitive word. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,

    # 20

    f""" 
    There are five rankings for a student's solution.
    Rankings_List = [Mastery, Proficiency, Competence, No Pass, Not Submitted]

    Your Task:
    ```
    1. Your task is to meticulously evaluate the student's solution and determine its accuracy. If their answer 
    aligns with the criteria, assign a suitable ranking (Mastery, Proficiency, Competence, No Pass, Not Submitted) 
    reflecting the quality of their work. Provide only the single most appropriate ranking as output. 
    ```
    **Output a single ranking word** based on the Rankings_List for the student's solution.
    ```

    Your Output Format:
    ```
    Deliver your final assessment as a single, definitive ranking word.
    ```
    Your constraints:
    ``` 
    You can only generate one word as the '**Output**', and that word must be one of the definitive ranking word from the Rankings_List
    ```
    """,
]