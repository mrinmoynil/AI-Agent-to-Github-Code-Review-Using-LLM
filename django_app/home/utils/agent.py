from groq import Groq
#import uuid
from .github import fetch_pr_files ,fetch_file_contents
import json



def analyze_single_file_llm(file_content, file_name):
    prompt = f"""
    Analyze the following code for:
    - Code style and formatting issues
    - Potential bugs or errors
    - Performance improvements
    - Best practices

    File: {file_name}
    Content:
    {file_content}

    Provide a detailed JSON output with the structure:
    {{
        "issues": [
            {{
                "type": "<style|bug|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
        ]
    }}
    ``json
    """

    client = Groq(
    api_key=""
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
            "role": "user",
            "content": prompt
        }
        ],
        response_format={
        "type": "json_object"
        }

    )
    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content
#print(analyze_code_llm(f, "models.py"))


def analyze_all_files(url, pr_number, github_token=None):
    #task_id = str(uuid.uuid4())

    analysis_results=[]

    try:
        print("agent all files working")
        files = fetch_pr_files(url, pr_number, github_token)
        for file in files:
            print("working new")
            file_name = file["filename"]
            raw_content = fetch_file_contents(url, file_name, github_token)
            analysis_result = analyze_single_file_llm(raw_content, file_name)
            #print(analysis_result)
            analysis_results.append(json.loads(analysis_result))
            #analysis_results.append(analysis_result)
        #return {"task_id": task_id,  "results": analysis_results}
        return analysis_results  # Return only the results
    except Exception as e:
        print(e)
        #return {"task_id": task_id,  "results":[]} 
        return{"results":[]}
        
