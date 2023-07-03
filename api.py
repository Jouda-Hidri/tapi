from flask import Flask, Response
import csv
import io

app = Flask(__name__)

def generate_csv():
    with open('large_file.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            yield ','.join(row) + '\n'

@app.route('/', methods=['GET'])
def export_csv():
    response_headers = {
        'Content-Type': 'text/plain'
    }

    # Create an in-memory file-like object to store the CSV data
    csv_data = io.StringIO()

    # Write the CSV data to the in-memory file-like object
    csv_writer = csv.writer(csv_data)
    csv_writer.writerows(generate_csv())

    # Retrieve the CSV data as a string
    csv_string = csv_data.getvalue()

    return Response(csv_string, headers=response_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
