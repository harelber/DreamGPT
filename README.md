# Dreaming with ChatGPT

This repo follows the paper "Dreaming with ChatGPT: Unraveling the Challenges of LLMs Dream Generation"

To run the code, install the requirements file:

```
pip install -r requirements.txt
```

The files are organizes as follows:

1. The **fetch_data** script allows one to generate dreams with the models this project obtianed.
To obtain one, please consult:
[API key help](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

2. The **Data** folder holds that data we used. The results files hold the models we stoped analyzing after the Dream Generation Analysis.
The models_usable_data.csv holds that data we annotated and fully analyzed.

3. The **chis** folder holds the chi-square analysis folder. The two subfolders hold the specific tests: **flower** for the genderized-flower test, and **lang** for the langauge-factor test.

4. The **success_rates** folder holds the analysis for all psychological attributes+the bias analysis of the "He" pronoun.

All csv data is provided in the respective folders.







