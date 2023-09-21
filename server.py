import pandas as pd

# (dgm) ➜  cms gunicorn -w 2 -b 0.0.0.0:9820 server:app
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
df = pd.read_csv("POI_Categories.csv")
# df.info()
df = df.dropna()
# print(df["Cate"].value_counts())
df["sum"] = df["Cate"] + " " + df["Keyword"]
# print(df["sum"].tolist()[:10])

passage_embedding = model.encode(df["sum"].astype(str).tolist())
custom_order = ["Cate", "Keyword"]


import numpy as np


from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_table_data", methods=["POST"])
def get_table_data():
    search_text = request.get_json().get("searchText")

    query_embedding = model.encode(search_text)
    scores = util.dot_score(query_embedding, passage_embedding)
    idxs = np.array(np.argsort(scores[0]))[::-1][:12]
    # print(idxs)
    resp = df.iloc[idxs][custom_order].to_dict(orient="records")
    custom_dict_reordered = [{key: row[key] for key in custom_order} for row in resp]
    # print(resp)
    # print(custom_dict_reordered)

    # In a real application, you would fetch and process data here.
    # For this example, we'll use some hardcoded data.

    return jsonify(custom_dict_reordered)


@app.route("/predict/<text>", methods=["GET"])
def predict(text):
    # Process the received text (you can replace this with your logic)
    response_text = f"You sent: {text}"

    query_embedding = model.encode(text)
    scores = util.dot_score(query_embedding, passage_embedding)
    idxs = np.array(np.argsort(scores[0]))[::-1][:10]
    # print(idxs)
    resp = df.iloc[idxs][["name", "explanation_vietnamese"]]
    # print(resp)

    # Return the response as JSON
    # Render the DataFrame as an HTML table
    table_html = resp.to_html(classes="table table-bordered", index=False)

    # Create an HTML template with the table
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title> Aidan with 💜 </title>
    </head>
    <body>
        <h1>🐳 💜 🌸 </h1>
        {table_html}
    </body>
    </html>
    """

    return html_template


if __name__ == "__main__":
    app.run(debug=True, port=9820)
