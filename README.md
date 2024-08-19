# Maths_with_LLM
## A Kaggle Competition by DataTalksClub
 In this competition, participants need to solve high school mathematics problems with LLMs.

The problems originate from ЕГЭ, a high school mathematics exam in Russia.

Each problem has been translated to English using GPT-4, and additionally we provide the original Russian texts for reference.

The goal of the competition is to solve these problems with or without LLMs. Solving the problems by hand is not permitted.

## Evaluation

Submissions are evaluated on the accuracy of the predicted answers. Accuracy is defined as the proportion of correct predictions out of the total number of problems in the test set. The higher the accuracy, the better your model performs.

## Submission Guidelines

The file must be a CSV file.
The file should contain exactly two columns: problem_id and answer.
Each problem_id should match the IDs provided in the test set.
Each answer should be the predicted solution to the corresponding problem.
Ensure that there are no missing or extra rows, as this will result in a submission error.
Evaluation Metric
The primary evaluation metric for this competition is accuracy, calculated as:

Accuracy = Number of Correct Predictions / Total Number of Problems

Your submission will be compared to the ground truth answers provided in the test set. The submission with the highest accuracy will be considered the winner.

## To run the script
"""To run this script make sure to install the necessary packages; pip install -qU langchain-openai langchain.
Then call the function prepare_prompts_and_get_answers(). This function takes in the following arguments:
- number of workers (e.g, 6),
- a dataframe with keys, problem_id (question id) and problem_text (question)
- a prefered model (e.g, "gpt-4o-mini")
and returns a dataframe containing answers to questions from the input data.
"""
