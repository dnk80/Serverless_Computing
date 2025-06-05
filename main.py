from flask import Flask, render_template, request as flask_request
from google.cloud import bigquery

app = Flask(__name__, template_folder='.')  # template in root

client = bigquery.Client()
PROJECT_ID = client.project
DATASET_ID = 'GASKET'

@app.route('/', methods=['GET', 'POST'])
def index():
    table_names = get_table_names()
    selected_table = None
    records = []

    if flask_request.method == 'POST':
        selected_table = flask_request.form.get('table')
        if selected_table:
            records = get_mpn_analog(selected_table)

    return render_template('index.html', tables=table_names, selected=selected_table, records=records)

def get_table_names():
    tables = client.list_tables(f"{PROJECT_ID}.{DATASET_ID}")
    return [t.table_id for t in tables]

def get_mpn_analog(table_name):
    query = f"""
        SELECT MPN, ANALOG, DESCRIPTION
        FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}`
        LIMIT 100
    """
    query_job = client.query(query)
    return list(query_job.result())

# ✅ Entry point for Google Cloud Functions (no functions-framework needed)
def main(request):
    return app(request.environ, start_response=lambda status, headers: None)
