# Import required modules from Flask and Python standard library
from flask import Flask, render_template, abort, request, redirect
import csv
import os  # Used to check if the CSV file already exists

# Initialize the Flask app
app = Flask(__name__)

# List of HTML pages that are allowed to be rendered dynamically
ALLOWED_PAGES = ['index.html', 'about.html', 'works.html', 'work.html', 'contact.html', 'thankyou.html']


# Route for the homepage (/) and explicitly for /index.html
@app.route('/')
@app.route('/index.html')
def home():
    # Renders the index.html file from the templates directory
    return render_template('index.html')


# Dynamic route to render other allowed pages
@app.route('/<string:page_name>')
def page(page_name):
    # If the requested page is in the allowed list, render it
    if page_name in ALLOWED_PAGES:
        return render_template(page_name)
    else:
        # Otherwise return a 404 error page
        abort(404)


# Function to write form data to a plain text file (optional/logging)
def write_to_file(data):
    with open('database.txt', 'a') as file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        # Append the data as formatted text
        file.write(f"\nEmail: {email},\nSubject: {subject},\nMessage: {message}\n")


# Function to write form data to a CSV file with headers
def write_to_csv(data):
    # Check if CSV file already exists to determine if we need to write headers
    file_exists = os.path.isfile('database.csv')

    # Open the CSV file in append mode with newline handling and Excel-friendly UTF-8 encoding
    with open('database.csv', mode='a', newline='', encoding='utf-8-sig') as database:
        writer = csv.writer(database)

        # Write headers only if the file is new
        if not file_exists:
            writer.writerow(['Email', 'Subject', 'Message'])

        # Write the actual form data
        writer.writerow([
            data.get('email', '').strip(),
            data.get('subject', '').strip(),
            data.get('message', '').replace('\n', ' ').replace('\r', '').strip()
        ])


# Route to handle form submissions
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            # Convert the submitted form data to a dictionary
            data = request.form.to_dict()

            # Save the data to a CSV file
            write_to_csv(data)

            # Redirect the user to the thank you page
            return redirect('/thankyou.html')
        except Exception as e:
            # In case of any failure, log error and show a fallback message
            print(f"Error saving data: {e}")
            return 'Did not save to database.'
    else:
        # If form was accessed via GET instead of POST
        return 'Something went wrong. Try again!'


# Start the Flask development server when this file is run directly
if __name__ == "__main__":
    app.run()  # Enable debug mode for automatic reload and better error messages
