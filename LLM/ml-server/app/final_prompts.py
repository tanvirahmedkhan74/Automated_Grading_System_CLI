prompts = [
    # 1
    "<Instrution> I will provide you with a `<Student's Solution>` and `<criteria>`. Based on the criteria, if the student's solution meets the criteria and if the solution is accurate according to the context, then output `YES`, or else output `NO`",
    # 2
    "<Instruction> I will provide you with a paragraph describing a scenario (criteria) and a student's answer (Student's Solution). Read the passage carefully and analyze the student's answer. Determine if the answer meets the criteria effectively. If the answer meets the criteria and solves the problem, then output \"YES\". Otherwise, output \"NO\".",
    # 3
    """
    <Instruction> I will provide you with a criteria describing a situation and one student's response. Read the criteria carefully and analyze the responses. Determine which response is more relevant to the situation.

**Example 1:**

criteria: Includes the benefits of anti-biotics
Student's Solution: The cough medicines are misused in our society (NO)

**Example 2:**

criteria: Includes the benefits of anti-biotics
Student's Solution: The right dose of anti-biotics can prevent many dangerous diseases for the human and also for the other animals (YES)

Based on these examples, analyze the following `criteria` and `Student's Solution` and determine Should the output be "YES" or "NO"?
    """,
    # 4
    """
    <Instruction> I will provide you with a criteria describing a situation and a Student's Solution. Let's think step by step to determine if the solution meets the criteria.

1. Summarize the key points of the criteria.
2. Analyze the Student's Solution and identify the action it suggests.
3. Compare the action in the solution to the situation in the criteria.
4. Does the solution address the problem presented in the criteria?

Following these steps, does the Student's Solution meet the criteria? (YES/NO)
    """,
    # 5
    "<Instruction> Let's think step by step. I will provide you with a criteria describing a situation and a Student's Solution. Analyze the criteria and the Solution to determine if the solution meets the criteria. (YES/NO)"
    # 6
    """
    <Instruction> I will provide you with a criteria describing a situation. Additionally, I'll offer two example solutions (Solution A and Solution B) with their corresponding relevance labels (YES/NO) based on the criteria. Analyze the following new criteria and Student's Solution using the provided examples as a guide.

**Example 1:**

criteria: A student is lost in the school building. They need to find the library.
Solution A: Ask the nearest teacher for directions. (YES)
Solution B: Go outside and play on the swings. (NO)

Does the `Student's Solution` meet the `criteria`? (YES/NO)
    """,
    # 7
    """
This task involves evaluating the relevance of student responses to given criteria. Here are some general guidelines:

* A relevant response addresses the situation in the criteria and proposes a solution. 
* An irrelevant response doesn't address the situation or suggests an unrelated action.

**Examples:**

criteria: A student forgot their lunch and is feeling hungry. 
* Relevant response: Buy lunch from the cafeteria. (YES)
* Irrelevant response: Read a book in the library. (NO)

criteria: A student is presenting a project on rainforests. 
* Relevant response: Show pictures and explain the different rainforest layers. (YES)
* Irrelevant response: Ask the class if they like pizza. (NO)

Now, I will provide you with a new criteria and Student's Solution. Analyze them based on these guidelines. 

Does the Student's Solution meet the criteria? (YES/NO)
    """,
    # 8
    """
    I will provide you with a criteria describing a situation. Let's analyze it together. What is the main problem the student is facing in this criteria?

Then, I will provide a Student's Solution. Does this solution directly address the problem you identified in the criteria? (YES/NO)
    """,
    # 9
    """
The criteria describes a specific topic. The Student's Solution should mention keywords related to that topic. 

Does the Student's Solution include any keywords related to the criteria? (YES/NO)
    """,
    # 10
    """
The criteria describes a situation with specific entities (people, places, things). The Student's Solution should acknowledge these entities.

Does the Student's Solution mention any of the entities (people, places, things) described in the criteria? (YES/NO)
    """,
    # 11
    """
The criteria describes a situation using certain words. The Student's Solution can use synonyms or related words to convey the same concept.

Does the Student's Solution address the same concept as the criteria, even if using different words? (YES/NO)
    """,
    # 12
    """
The criteria describes a situation. The Student's Solution can paraphrase the key points of the criteria in their own words.

Does the Student's Solution essentially rephrase the main idea of the criteria, even if worded differently? (YES/NO)
    """,
    # 13
    """
Imagine you have to answer a question based on the criteria. Does the Student's Solution provide an answer to that question?

Does the Student's Solution answer the question implied by the criteria? (YES/NO)
    """,
    # 14
    "The criteria describes a situation with key ideas and details. Analyze the Student's Solution and identify the main ideas it conveys. Do the key ideas in the Student's Solution overlap with the key ideas in the criteria? (YES/NO)",
    # 15
    "The criteria describes a situation and the specific need or goal of the student. Does the Student's Solution directly address the need or goal stated in the criteria? (YES/NO)"
]
