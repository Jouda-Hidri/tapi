from flask import Flask, Response
import csv
import io
import random
import string

app = Flask(__name__)

def generate_csv(file_size_mb):
    target_size_bytes = file_size_mb * 1024 * 1024

    # Create an in-memory file-like object to store the CSV data
    csv_data = io.StringIO()

    # Create a CSV writer
    csv_writer = csv.writer(csv_data)

    current_size_bytes = 0

    while current_size_bytes < target_size_bytes:
        # Generate a random row of data
        row = generate_random_row()

        # Write the row to the CSV file
        csv_writer.writerow(row)

        # Calculate the size of the written row in bytes
        row_size_bytes = len(','.join(row).encode('utf-8'))

        # Update the current size of the CSV data
        current_size_bytes += row_size_bytes

        # Reset the file-like object's position to the beginning
        csv_data.seek(0)

        # Yield the CSV data generated so far
        yield csv_data.getvalue()

        # Reset the file-like object to an empty state
        csv_data.seek(0)
        csv_data.truncate(0)

def generate_random_row():
    # Generate a random row of data (e.g., 10 columns with random strings)
    return [generate_random_string() for _ in range(10)]

def generate_random_string(length=10):
    # Generate a random string of the specified length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET'])
def export_csv():
    response_headers = {
        'Content-Type': 'text/plain'
    }

    # Specify the desired file size in megabytes
    file_size_mb = 200

    # Generate the CSV data
    csv_data_generator = generate_csv(file_size_mb)

    # Stream the generated CSV data as a response
    return Response(csv_data_generator, headers=response_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

