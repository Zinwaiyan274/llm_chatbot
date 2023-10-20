from pandasai import SmartDataframe
from langchain.llms import OpenAI
import pandas as pd
# import json
# import cachetools
from flask import Flask, jsonify, request
from cachetools import LRUCache  # Import cachetools for caching

# Load data and initialize SmartDataframe
df = pd.read_excel('A.L.I2.xlsx')

# Create a cache using cachetools
cache = LRUCache(maxsize=1000)  # You can adjust the cache size as needed

# Create a dictionary containing the API token
model_kwargs = {
    "api_token": "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"
}

# Initialize the OpenAI object with model_kwargs
llm = OpenAI(model_kwargs=model_kwargs)
langchain_sdf = SmartDataframe(df, config={"llm": llm})


app = Flask(__name__)

@app.route('/chatbot', methods=['POST', 'GET'])
def main():
    data = request.json
    query = data.get('query')
    
    try:
       

        # langchain_sdf = SmartDataframe(df, config={"llm": llm})
        query = "show me the apt that has both swimming pool and gym"
        output = ((langchain_sdf.chat(f" pls output me with pandas dataframe, 0 means theere is no [column name]  1 means that Apartments has [columns name].... {query} ")))
        
        # Convert the output to JSON format
        # output_json = output.to_json(orient='records')  # Convert to JSON array
        
        # Return the JSON response
        return jsonify({"output": output})
        
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9494, debug=True)