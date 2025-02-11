from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

# Function to reformat the recipe data
def reformat_recipe_data(file_path):
    df = pd.read_csv(file_path)
    df.dropna(how='all', axis=1, inplace=True)
    
    reformatted_data = []
    for index, row in df.iterrows():
        item_id = row['ItemID']
        recipe_name = row['ItemName']

        for i in range(3, len(row), 3):
            if i + 2 < len(row):
                raw_material = row.iloc[i]
                qty = row.iloc[i + 1]
                unit = row.iloc[i + 2]

                if pd.notna(raw_material):
                    reformatted_data.append([item_id, recipe_name, raw_material, qty, unit])

    reformatted_df = pd.DataFrame(reformatted_data, columns=['ItemID', 'Recipe Name', 'Raw Material', 'Qty', 'Unit'])
    return reformatted_df

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = "uploaded_file.xlsx"
    file.save(file_path)

    reformatted_df = reformat_recipe_data(file_path)
    output_filename = "processed_file.xlsx"
    reformatted_df.to_excel(output_filename, index=False)

    return send_file(output_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask is running!"

if __name__ == "__main__":
    app.run(debug=True)
