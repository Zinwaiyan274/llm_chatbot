import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from pandasai.smart_dataframe import SmartDataframe
from langchain.llms import OpenAI

app = FastAPI()

# Load data and initialize SmartDataframe
df = pd.read_excel('A.L.I2.xlsx')

# Create a dictionary containing the API token
model_kwargs = {
    "api_key": "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"
}
llm = OpenAI(api_key="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")

langchain_sdf = SmartDataframe(df, config={"llm": llm})


class Query(BaseModel):
    query: str
    api_key: str


@app.post('/chatbot')
async def main(item: Query):
    if item.api_key != model_kwargs['api_key']:
        return {"error": "Invalid API key"}

    try:
        query = item.query
        langchain_sdf.chat(f" pls output me with pandas dataframe, 0 means there is no [column name], 1 means that Apartments have [column name].... {query}")

        # Access the underlying DataFrame
        converted_df = langchain_sdf.data

        # Convert the DataFrame to JSON
        converted_json = converted_df.to_json(orient='records')

        return {"output": converted_json}
    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9494)  # Remove the 'debug' argument