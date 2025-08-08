from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, Response, send_file
import sqlite3
import os
import json
from datetime import datetime
import secrets
import hashlib
import pandas as pd
import pmdarima as pm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from io import BytesIO
import base64
import requests
import serpapi
import numpy as np

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

client = serpapi.Client(api_key="9699988abab9e1a713e0b06357416307d9e616a59838a08931adeb7e47aa8627")

# Configure template and static folders
app.template_folder = 'templates'
app.static_folder = 'static'

# Database configuration
DATABASE = 'finora.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            company TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            newsletter BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified BOOLEAN DEFAULT 0
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS demo_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            company_size TEXT NOT NULL,
            industry TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User sessions table (optional - for better session management)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash


@app.route('/')
def home():
    """Main landing page"""
    return render_template('home.html')

@app.route('/demo')
def demo():
    """Demo request page"""
    return render_template('demo.html')

@app.route('/login')
def login():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Signup page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/optimize')
def optimize():
    return render_template('optimize.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page (requires login)"""
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    
    # Get user information from database
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    conn.close()
    
    if not user:
        session.clear()
        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=user)

# API Routes
@app.route('/api/demo-request', methods=['POST'])
def submit_demo_request():
    """Handle demo request form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'company', 'jobTitle', 'companySize', 'industry']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Save to database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO demo_requests 
            (first_name, last_name, email, phone, company, job_title, company_size, industry, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['firstName'],
            data['lastName'],
            data['email'],
            data.get('phone', ''),
            data['company'],
            data['jobTitle'],
            data['companySize'],
            data['industry'],
            data.get('message', '')
        ))
        conn.commit()
        conn.close()
        
        print(f"New demo request from {data['firstName']} {data['lastName']} at {data['company']}")
        
        return jsonify({
            'success': True, 
            'message': 'Demo request submitted successfully! Our team will contact you within 24 hours.'
        })
        
    except Exception as e:
        print(f"Error processing demo request: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle login form submission"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Find user in database
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Create session
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_name'] = f"{user['first_name']} {user['last_name']}"
        
        if remember:
            session.permanent = True
        
        print(f"User {email} logged in successfully")
        
        return jsonify({
            'success': True, 
            'message': 'Login successful!',
            'redirect': url_for('dashboard')
        })
    
    except Exception as e:
        print(f"Error processing login: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Handle signup form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'company', 'password', 'confirmPassword']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Check if passwords match
        if data['password'] != data['confirmPassword']:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
        
        # Check if terms are accepted
        if not data.get('terms'):
            return jsonify({'success': False, 'message': 'Please accept the Terms of Service'}), 400
        
        # Check if user already exists
        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT id FROM users WHERE email = ?', (data['email'],)
        ).fetchone()
        
        if existing_user:
            conn.close()
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Hash password
        password_hash = hash_password(data['password'])
        
        # Create new user
        cursor = conn.execute('''
            INSERT INTO users 
            (first_name, last_name, email, company, password_hash, newsletter, verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['firstName'],
            data['lastName'],
            data['email'],
            data['company'],
            password_hash,
            1 if data.get('newsletter') else 0,
            0  # Email verification can be implemented later
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"New user registered: {data['email']} (ID: {user_id})")
        
        return jsonify({
            'success': True, 
            'message': 'Account created successfully! You can now log in.',
            'redirect': url_for('login')
        })
        
    except Exception as e:
        print(f"Error processing signup: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Handle user logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/user-stats')
def user_stats():
    """Get user statistics for dashboard"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    # Get user info
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    # Mock statistics (in production, fetch real data from database)
    stats = {
        'totalProducts': 1247,
        'activeOptimizations': 89,
        'revenueIncrease': 23.5,
        'competitorsTracked': 15,
        'priceUpdates': 342,
        'avgResponseTime': '1.2s'
    }
    
    return jsonify({'success': True, 'data': stats})

@app.route('/api/user-profile')
def user_profile():
    """Get user profile information"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, first_name, last_name, email, company, newsletter, created_at FROM users WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    return jsonify({
        'success': True, 
        'data': {
            'id': user['id'],
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'email': user['email'],
            'company': user['company'],
            'newsletter': bool(user['newsletter']),
            'memberSince': user['created_at']
        }
    })

# Admin routes (for development/testing)
@app.route('/admin/users')
def admin_users():
    """View all users (development only)"""
    if not app.debug:
        return "Not available in production", 403
    
    conn = get_db_connection()
    users = conn.execute(
        'SELECT id, first_name, last_name, email, company, created_at FROM users ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/demo-requests')
def admin_demo_requests():
    """View all demo requests (development only)"""
    if not app.debug:
        return "Not available in production", 403
    
    conn = get_db_connection()
    requests = conn.execute(
        'SELECT * FROM demo_requests ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    return render_template('admin_demo_requests.html', requests=requests)


@app.route('/optimize', methods=['GET', 'POST'])
def optimize_prices():
    if 'user_id' not in session:
        flash('Please log in to access price optimization.', 'error')
        return redirect(url_for('login'))

    sales_csv_path = 'data/amazon_sales.csv'  # Update with your actual CSV path
    df = pd.read_csv(sales_csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Get search inputs
    selected_category = request.form.get('category') or request.args.get('category') or None
    product_name_query = request.form.get('product_name') or request.args.get('product_name') or None

    if not selected_category and not product_name_query:
        flash('Please enter a product category or product name for optimization.', 'warning')
        return render_template('optimize.html', optimized_data=None,
                               selected_category="", product_name_query="")

    # Filter dataframe on inputs
    filtered_df = df.copy()
    if selected_category:
        filtered_df = filtered_df[filtered_df['Category'].str.lower() == selected_category.lower()]
    if product_name_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(product_name_query, case=False, na=False)]

    if filtered_df.empty:
        flash('No sales data found for your search criteria.', 'error')
        return render_template('optimize.html', optimized_data=None,
                               selected_category=selected_category or "", product_name_query=product_name_query or "")

    # Aggregate data for time series
    if product_name_query:
        # Forecast at product level — pick first matching product
        agg_col = 'Product'
        sales_agg = filtered_df.groupby(['Date', 'Product']).agg({'Total Sales': 'sum', 'Price': 'mean'}).reset_index()
        product_to_forecast = sales_agg['Product'].iloc[0]
        ts_data = sales_agg[sales_agg['Product'] == product_to_forecast]
        ts = ts_data.set_index('Date').sort_index()['Total Sales'].asfreq('D').fillna(0)
        display_name = product_to_forecast
        current_price = ts_data['Price'].mean()
    else:
        # Forecast at category level
        agg_col = 'Category'
        sales_agg = filtered_df.groupby(['Date', 'Category']).agg({'Total Sales': 'sum', 'Price': 'mean'}).reset_index()
        ts_data = sales_agg
        ts = ts_data.set_index('Date').sort_index()['Total Sales'].asfreq('D').fillna(0)
        display_name = selected_category.capitalize()
        current_price = ts_data['Price'].mean()

    # Fit pmdarima model
    model = pm.auto_arima(
        ts,
        seasonal=True,
        m=7,
        stepwise=True,
        suppress_warnings=True,
        error_action='ignore'
    )

    # Forecast next 30 days
    n_periods = 30
    forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
    forecast_index = pd.date_range(start=ts.index[-1] + pd.Timedelta(days=1), periods=n_periods, freq='D')

    # Simple elasticity price adjustment
    historical_avg = ts.mean()
    forecast_avg = forecast.mean()
    elasticity_factor = 0.03 if forecast_avg > historical_avg else -0.05
    optimized_price = round(current_price * (1 + elasticity_factor), 2) if not pd.isna(current_price) else None

    # Prepare optimized_data for template (no plot on this page)
    optimized_data = {
        'name': display_name,
        'current_price': round(current_price, 2) if not pd.isna(current_price) else None,
        'optimized_price': optimized_price,
        'forecast_next_30_days': forecast.tolist()
    }

    return render_template(
        'optimize.html',
        optimized_data=optimized_data,
        selected_category=selected_category or "",
        product_name_query=product_name_query or ""
    )


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if 'user_id' not in session:
        flash('Please log in to view analytics.', 'error')
        return redirect(url_for('login'))

    # For analytics, use GET or POST parameters similarly to /optimize
    selected_category = request.form.get('category') or request.args.get('category') or None
    product_name_query = request.form.get('product_name') or request.args.get('product_name') or None

    if not selected_category and not product_name_query:
        flash('Please enter a product category or product name to view analytics.', 'warning')
        return render_template('analytics.html', plot_image=None, title="", selected_category="", product_name_query="")

    sales_csv_path = 'data/amazon_sales.csv'  # Update with your actual CSV path
    df = pd.read_csv(sales_csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter as in optimize
    filtered_df = df.copy()
    if selected_category:
        filtered_df = filtered_df[filtered_df['Category'].str.lower() == selected_category.lower()]
    if product_name_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(product_name_query, case=False, na=False)]

    if filtered_df.empty:
        flash('No data found for the specified product/category.', 'error')
        return render_template('analytics.html', plot_image=None, title="", selected_category=selected_category or "", product_name_query=product_name_query or "")

    if product_name_query:
        title = f"Analytics for Product: {product_name_query}"
    else:
        title = f"Analytics for Category: {selected_category}"

    # Aggregate sales by date
    sales_agg = filtered_df.groupby('Date')['Total Sales'].sum().reset_index()
    ts = sales_agg.set_index('Date').sort_index()['Total Sales'].asfreq('D').fillna(0)

    # Plot the sales time series
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ts.index, ts.values, label='Sales')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Sales')
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode()
    plt.close(fig)

    return render_template(
        'analytics.html',
        plot_image=image_base64,
        title=title,
        selected_category=selected_category or "",
        product_name_query=product_name_query or ""
    )

@app.route('/competitor-analysis', methods=['GET', 'POST'])
def competitor_analysis():
    if 'user_id' not in session:
        flash('Please log in to access competitor analysis.', 'error')
        return redirect(url_for('login'))

    query = request.form.get('product') or request.args.get('product') or ''
    if not query:
        flash("Please enter a product name to search competitor prices.", "warning")
        return render_template('competitor_analysis.html', products=[], query=query)

    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": client.api_key,
    }

    try:
        results = client.search(params)  # returns SerpResults object

        # Access shopping results list safely
        shopping_results = results.get("shopping_results", [])

        products = []
        for item in shopping_results:
            product_name = item.get("title")
            price_raw = item.get("extracted_price")
            price = None

            if price_raw is not None:
                if isinstance(price_raw, str):
                    cleaned_price = price_raw.replace('$', '').replace(',', '').strip()
                    try:
                        price = float(cleaned_price)
                    except ValueError:
                        price = None
                elif isinstance(price_raw, (int, float)):
                    price = float(price_raw)

            link = item.get("link")
            source = item.get("source") or "Unknown"
            products.append({
                "product_name": product_name,
                "price": price,
                "link": link,
                "source": source
            })

        # Sort products by price ascending
        products = sorted([p for p in products if p['price'] is not None], key=lambda x: x['price'])

        if not products:
            flash(f"No competitor data found for \"{query}\".", "warning")

    except Exception as e:
        flash(f"Error fetching competitor data: {str(e)}", "error")
        products = []

    return render_template('competitor_analysis.html', products=products, query=query)

def get_competitor_products(product_name):
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": client.api_key,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com"
    }
    results = client.search(params)
    shopping_results = results.get("shopping_results", [])
    products = []
    for item in shopping_results:
        price_raw = item.get("extracted_price")
        price = None
        if price_raw:
            if isinstance(price_raw, str):
                try:
                    price = float(price_raw.replace("$", "").replace(",", "").strip())
                except:
                    price = None
            elif isinstance(price_raw, (float, int)):
                price = float(price_raw)
        products.append({
            "product_name": item.get("title"),
            "price": price,
            "link": item.get("link"),
            "source": item.get("source") or "Unknown"
        })
    return sorted([p for p in products if p['price'] is not None], key=lambda x: x['price'])

@app.route('/full-report', methods=['GET'])
def full_report():
    if 'user_id' not in session:
        flash('Please log in to access reports.', 'error')
        return redirect(url_for('login'))

    query = request.args.get('product', '').strip()
    category = request.args.get('category', '').strip()

    if not query and not category:
        flash('Please provide a product name or category to generate the report.', 'warning')
        return redirect(url_for('dashboard'))

    try:
        # Get competitor prices only if product name is given
        competitor_products = get_competitor_products(query) if query else []

        # Load sales CSV
        sales_csv_path = os.path.join('data', 'amazon_sales.csv')
        df = pd.read_csv(sales_csv_path)
        df['Date'] = pd.to_datetime(df['Date'])

        # Filter sales data
        filtered_df = df.copy()
        if category:
            filtered_df = filtered_df[filtered_df['Category'].str.lower() == category.lower()]
        if query:
            filtered_df = filtered_df[filtered_df['Product'].str.contains(query, case=False, na=False)]

        # Price optimization data
        optimized_data = None
        if not filtered_df.empty:
            if query:
                sales_agg = filtered_df.groupby(['Date', 'Product']).agg({'Total Sales':'sum', 'Price':'mean'}).reset_index()
                product_to_forecast = sales_agg['Product'].iloc[0]
                ts_data = sales_agg[sales_agg['Product'] == product_to_forecast]
                ts = ts_data.set_index('Date').sort_index()['Total Sales'].asfreq('D').fillna(0)
                current_price = ts_data['Price'].mean()
                report_name = product_to_forecast
            else:
                sales_agg = filtered_df.groupby(['Date', 'Category']).agg({'Total Sales':'sum', 'Price':'mean'}).reset_index()
                ts_data = sales_agg
                ts = ts_data.set_index('Date').sort_index()['Total Sales'].asfreq('D').fillna(0)
                current_price = ts_data['Price'].mean()
                report_name = category.capitalize()

            model = pm.auto_arima(
                ts,
                seasonal=True,
                m=7,
                stepwise=True,
                suppress_warnings=True,
                error_action='ignore'
            )
            forecast, conf_int = model.predict(n_periods=30, return_conf_int=True)

            elasticity_factor = 0.03 if forecast.mean() > ts.mean() else -0.05
            optimized_price = round(current_price * (1 + elasticity_factor), 2) if current_price and not np.isnan(current_price) else None

            optimized_data = {
                'Name': report_name,
                'Current Price': round(current_price, 2) if current_price and not np.isnan(current_price) else None,
                'Optimized Price': optimized_price,
                'Forecasted Sales Next 30 Days': forecast.tolist()
            }

        # Sales analytics aggregation
        sales_agg = filtered_df.groupby('Date')['Total Sales'].sum().reset_index()

        # Generate Excel report with multiple sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

            # Optional: output filtered sales data for reference
            filtered_df.to_excel(writer, index=False, sheet_name='Filtered Sales Data')

            # Competitor Prices sheet
            if competitor_products:
                df_comp = pd.DataFrame(competitor_products)[['product_name','price','source','link']]
                df_comp.columns = ['Product Name', 'Price (USD)', 'Source', 'Link']
                df_comp.to_excel(writer, index=False, sheet_name='Competitor Prices')

            # Price Optimization sheet
            if optimized_data:
                df_opt = pd.DataFrame({
                    'Metric': ['Product/Category', 'Current Price', 'Optimized Price'],
                    'Value': [optimized_data['Name'], optimized_data['Current Price'], optimized_data['Optimized Price']]
                })
                df_opt.to_excel(writer, index=False, sheet_name='Price Optimization')

                # Sales Forecast sheet
                forecast_df = pd.DataFrame({
                    'Day': range(1,31),
                    'Forecasted Sales': optimized_data['Forecasted Sales Next 30 Days']
                })
                forecast_df.to_excel(writer, index=False, sheet_name='Sales Forecast (30d)')

            # Sales Analytics sheet
            if not sales_agg.empty:
                sales_agg.to_excel(writer, index=False, sheet_name='Sales Analytics')

        output.seek(0)

        filename = f"full_pricing_report_{(query or category).replace(' ', '_') or 'report'}.xlsx"

        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        flash(f"Failed to generate report: {e}", 'error')
        return redirect(url_for('dashboard'))

@app.route('/full-report-form')
def full_report_form():
    if 'user_id' not in session:
        flash('Please log in to access reports.', 'error')
        return redirect(url_for('login'))
    return render_template('full_report.html')

@app.route('/shopify', methods=["GET", "POST"])
def shopify():
    return render_template('shopify.html')

def shopify_api():
    url = 'https://your-calculator-api.com/calculate'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'productId': 'gid://shopify/Product/123456789',
        'variantId': 'gid://shopify/ProductVariant/987654321',
        'basePrice': 49.99,
        'userInputs': {
            'quantity': 3,
            'location': 'IN',
            'membershipLevel': 'Gold'
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        df = pd.read_json(response.json())
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Create necessary directories
def create_directories():
    """Create required directories if they don't exist"""
    directories = ['templates', 'static/css', 'static/js', 'static/images']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == '__main__':
    # Create directories
    create_directories()
    
    # Initialize database
    init_database()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
