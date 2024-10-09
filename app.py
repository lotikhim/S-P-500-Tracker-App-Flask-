import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import pandas as pd
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello Python'

def read_csv_file_gainers(file_path):      
    gainers = pd.read_csv(file_path, skiprows=0)
    # Round the 'Close' column to 2 decimal places
    gainers['Close'] = gainers['Close'].round(2)
    gainers['Open'] = gainers['Open'].round(2)
    gainers['High'] = gainers['High'].round(2)
    gainers['Low'] = gainers['Low'].round(2)
    return gainers

def read_csv_file_losers(file_path):      
    losers = pd.read_csv(file_path, skiprows=0)
    # Round the 'Close' column to 2 decimal places
    losers['Close'] = losers['Close'].round(2)
    losers['Open'] = losers['Open'].round(2)
    losers['High'] = losers['High'].round(2)
    losers['Low'] = losers['Low'].round(2)
    return losers

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(user_name):
    conn = get_db_connection()
    accounts = conn.execute('SELECT id, user_name, pass_word FROM accounts WHERE user_name =?',
    (user_name,)).fetchone()
    conn.close()
    return accounts

def select_all(user_name):
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts WHERE user_name =?',
    (user_name,)).fetchall()
    conn.close()
    return accounts

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        return True
    else:
        return False

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        accounts = get_post(user_name)
        if not user_name:
            flash('user_name is required!')
        elif not pass_word:
            flash('pass_word is required!')        
        else:
            if accounts is None:
                flash('Account does not exist, please check and try again.')
                return render_template('index.html')
            elif pass_word == accounts['pass_word']:
                return redirect(url_for('homepage'))
            else:
                flash('Incorrect password, please check and try again.')
                return redirect(url_for('index'))

    return render_template('index.html')

def select_all(user_name):
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts WHERE user_name =?',
    (user_name,)).fetchall()
    conn.close()
    return accounts

def select_all(user_name):
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts WHERE user_name =?',
    (user_name,)).fetchall()
    conn.close()
    return accounts

def select_all_by_email(email):
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts WHERE email =?',
    (email,)).fetchall()
    conn.close()
    return accounts

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        email = request.form['email']
        if validate_email(email) is True:
            if not user_name:
                flash('user_name is required!')
            elif not pass_word:
                flash('pass_word is required!')
            elif not email:
                flash('Email is required!')
            else:
                conn = get_db_connection()
                accounts = select_all(user_name)      #check existing user name?
                accounts_email = select_all_by_email(email)  #check existing email?
                if not accounts:  # check if accounts list is empty
                    if not accounts_email:  # check if accounts_email list is empty
                        conn.execute('INSERT INTO accounts (user_name, pass_word, email) VALUES (?,?,?)',
                        (user_name,pass_word,email))
                        conn.commit()
                        conn.close()
                        return redirect(url_for('index'))
                    else:
                        flash('Email already registered account, please use another one.')
                        return render_template('signup.html')
                else:
                    flash('User Name already being used, please use another user name.')
                    return render_template('signup.html')
                    
        else:
            flash('Please input a correct email and try again.')
            return render_template('signup.html')
    return render_template('signup.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        email = request.form['email']
        accounts = get_post(user_name)
        if not user_name:
            flash('user_name is required!')
        elif not pass_word:
            flash('pass_word is required!')
        elif not email:
            flash('email is required!')
        else:
            if accounts is None:
                flash('Account name is wrong, please check and try again.')
                return redirect(url_for('homepage'))
            conn = get_db_connection()
            conn.execute('UPDATE accounts SET pass_word =?, email =? WHERE user_name = ?',
                        (pass_word, email, user_name))
            conn.commit()
            conn.close()
            return redirect(url_for('homepage'))
    return render_template('account.html')

@app.route('/edit/<string:user_name>/', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        email = request.form['email']
        accounts = get_post(user_name)
        if not user_name:
            flash('user_name is required!')
        elif not pass_word:
            flash('pass_word is required!')
        elif not email:
            flash('email is required!')
        else:
            if accounts is None:
                flash('Account does not exist, please check and try again.')
                return redirect(url_for('homepage'))
            conn = get_db_connection()
            conn.execute('UPDATE accounts SET pass_word =?, email =? WHERE user_name = ?',
                        (pass_word, email, user_name))
            conn.commit()
            conn.close()
            return redirect(url_for('homepage'))
    return render_template('edit.html', accounts=accounts)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/homepage')
def homepage():
    gainers = read_csv_file_gainers('gainers.csv')
    losers = read_csv_file_losers('losers.csv')
    return render_template('homepage.html', gainers= gainers,losers=losers)


@app.route('/god', methods=['GET','POST'])
def god():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts ORDER BY created desc').fetchall()
    conn.close()
    if request.method == 'POST':
        user_name = request.form['user_name']
        pass_word = request.form['pass_word']
        email = request.form['email']
        accounts = get_post(user_name)
        if not user_name:
            flash('user_name is required!')
        elif not pass_word:
            flash('pass_word is required!')
        elif not email:
            flash('email is required!')
        else:
            if accounts is None:
                flash('Account name is wrong, please check and try again.')
                return redirect(url_for('god'))
            conn = get_db_connection()
            conn.execute('UPDATE accounts SET pass_word =?, email =? WHERE user_name = ?',
                        (pass_word, email, user_name))
            conn.commit()
            conn.close()
            return redirect(url_for('god'))
    return render_template('god.html', accounts=accounts)

@app.route('/delete', methods=['POST'])
def delete():
    user_name = request.form.get('user_name')
    if user_name is None:
        flash('No user name provided!')
        return redirect(url_for('god'))
    accounts = get_post(user_name)
    if accounts is None:
        flash('Account does not exist, please check and try again.')
        return redirect(url_for('god'))
    conn = get_db_connection()
    conn.execute('DELETE from accounts WHERE user_name = ?', (user_name,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user_name))
    return redirect(url_for('god'))

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


pages = {
    'AOS': ' A. O. Smith Corporation',
    'ABT': ' Abbott Laboratories',
    'ABBV': ' AbbVie Inc.',
    'ACN': ' Accenture plc',
    'ADBE': ' Adobe Inc.',
    'AMD': ' Advanced Micro Devices, Inc.',
    'AES': ' The AES Corporation',
    'AFL': ' Aflac Incorporated',
    'A': ' Agilent Technologies, Inc.',
    'APD': ' Air Products and Chemicals, Inc.',
    'ABNB': ' Airbnb, Inc.',
    'AKAM': ' Akamai Technologies, Inc.',
    'ALB': ' Albemarle Corporation',
    'ARE': ' Alexandria Real Estate Equities, Inc.',
    'ALGN': ' Align Technology, Inc.',
    'ALLE': ' Allegion plc',
    'LNT': ' Alliant Energy Corporation',
    'ALL': ' The Allstate Corporation',
    'GOOGL': ' Alphabet Inc.',
    'GOOG': ' Alphabet Inc.',
    'MO': ' Altria Group, Inc.',
    'AMZN': ' Amazon.com, Inc.',
    'AMCR': ' Amcor plc',
    'AEE': ' Ameren Corporation',
    'AAL': ' American Airlines Group Inc.',
    'AEP': ' American Electric Power Company, Inc.',
    'AXP': ' American Express Company',
    'AIG': ' American International Group, Inc.',
    'AMT': ' American Tower Corporation',
    'AWK': ' American Water Works Company, Inc.',
    'AMP': ' Ameriprise Financial, Inc.',
    'AME': ' AMETEK, Inc.',
    'AMGN': ' Amgen Inc.',
    'APH': ' Amphenol Corporation',
    'ADI': ' Analog Devices, Inc.',
    'ANSS': ' ANSYS, Inc.',
    'AON': ' Aon plc',
    'APA': ' APA Corporation',
    'AAPL': ' Apple Inc.',
    'AMAT': ' Applied Materials, Inc.',
    'APTV': ' Aptiv PLC',
    'ACGL': ' Arch Capital Group Ltd.',
    'ADM': ' Archer-Daniels-Midland Company',
    'ANET': ' Arista Networks, Inc.',
    'AJG': ' Arthur J. Gallagher & Co.',
    'AIZ': ' Assurant, Inc.',
    'T': ' AT&T Inc.',
    'ATO': ' Atmos Energy Corporation',
    'ADSK': ' Autodesk, Inc.'
    
}

@app.route('/<query>')
def result_page(query):
    # Display the result page
    page = pages.get(query)
    return render_template('result.html', page=page)

@app.route('/error_404')
def error_404():
    # Display the 404 error page
    return render_template('404.html'), 404 

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    # Check if the page exists in the dictionary
    if query in pages:
        return redirect(url_for('stock_page', ticker=query))
    else:
        return redirect(url_for('error_404'))
    
@app.route("/stock/<ticker>")
def stock_page(ticker):
    # Perform validation to check if the ticker is valid
    valid_tickers= ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK']
    if ticker in valid_tickers:
        df = pd.read_csv('info.csv')
       # Filter the DataFrame based on the ticker value
        filtered_df = df[df['Ticker'] == ticker]
        # Fill NaN values with 'NA'
        filtered_df.fillna('NA', inplace=True)
        link = filtered_df["Website"].iloc[0]
        longname = filtered_df["Long Name"].iloc[0]
        filtered_df.drop(['Website', 'Long Name'], axis=1, inplace=True)
        # Convert the filtered DataFrame to a list of dictionaries
        data = filtered_df.to_dict('records')
        # If ticker is valid, render the stock template
        news_df = pd.read_csv('news.csv')
        filtered_news_df = news_df[news_df['Ticker'] == ticker]
        # Convert each row to a dictionary and store them in a list
        news_dicts = filtered_news_df.to_dict(orient='records')
        return render_template("stock.html", ticker=ticker,data=data,link=link,longname=longname,news_dicts=news_dicts)
    else:
        # If ticker is invalid, render an error template
        return render_template("404.html", message="Invalid ticker")

