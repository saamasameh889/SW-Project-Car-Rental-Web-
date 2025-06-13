from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime
from flask import jsonify
import bcrypt
import time

app = Flask(__name__, static_folder='assets')
app.secret_key = '#Key0123456789#'  

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
app.config['MYSQL_DB'] = 'elfinal'

mysql = MySQL(app)

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info('Running the index.html page...')
    session.pop('_flashes', None)
    return render_template('index.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info('Running the login.html page...')
    return render_template('login.html')

# Route for login
@app.route('/auth', methods=['POST'])
def auth():
    app.logger.info('Inside the auth block')
    email = request.form['email']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    user = cur.fetchone()
    
    if user:
        # Ensure password is correct by checking hash
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            if user[4] == 'User':
                return redirect(url_for('index'))  # Redirect to home page after login
            if user[4] == 'Owner':
                return redirect(url_for('manage_cars'))  # Redirect to manage cars page if user is an owner
        else:
            flash('Invalid password, please try again.', 'danger')
    else:
        flash('No user found with that email.', 'danger')

    app.logger.info('End of login module')
    return redirect(url_for('login'))  # Redirect back to the login page if login fails

# Route for register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('Running the register.html page...')
    return render_template('register.html')

# Route for registerVerification
@app.route('/registerVerification', methods=['POST'])
def registerVerification():
    app.logger.info('Start the registerVerification block')
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        flash('Email already registered. Please log in.', 'danger')
        return redirect(url_for('login'))
    
    # Insert new user into the database
    cur.execute("INSERT INTO Users (Name, Email, Password, UserType) VALUES (%s, %s, %s, %s)", (full_name, email, hashed_password, user_type))
    mysql.connection.commit()

    # Fetch the newly created user
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    new_user = cur.fetchone()

    if new_user:  # Ensure the new user was added successfully
        session['user_id'] = new_user[0]  # Set the user session
        flash('Registration successful! Redirecting to the home page...', 'success')
        time.sleep(3)
        app.logger.info('End of register module')
        return redirect(url_for('index'))  # Redirect to home page after successful registration
    else:
        flash('Registration failed. Please try again later.', 'danger')
        time.sleep(3)
        app.logger.error('Failed to fetch newly registered user')

        if new_user[4] == 'User':
                return redirect(url_for('index'))  # Redirect to home page after login
        if new_user[4] == 'Owner':
                return redirect(url_for('manage_cars'))  # Redirect to manage cars page if user is an owner

        return redirect(url_for('index'))  # Redirect back to auth page if registration fails
    

@app.route('/view-more', methods=['GET'])
def view_more_cars():
    app.logger.info('Accessing the "View More" page...')

    try:
        cur = mysql.connection.cursor()

        # Fetch all cars without filtering
        cur.execute("SELECT * FROM Cars WHERE OwnerID IS NOT NULL")
        cars = cur.fetchall()

        app.logger.info(f"Fetched Cars: {cars}")  # Log for debugging

        if not cars:
            flash('No cars available at the moment.', 'info')

        # Render the cars.html template with all cars
        return render_template('cars.html', cars=cars)

    except Exception as e:
        app.logger.error(f"Error fetching cars: {str(e)}")
        flash("An error occurred. Please try again later.", "danger")
        return redirect(url_for('index'))

@app.route('/cars', methods=['GET'])
def cars():
    search_query = request.args.get('search', '').strip()  # Get search query (if any)
    try:
        cur = mysql.connection.cursor()
        
        if search_query:
            # Fetch cars that match the search query
            cur.execute("""
                SELECT * FROM Cars
                WHERE (Name LIKE %s OR Fuel_Type LIKE %s) AND OwnerID IS NOT NULL
            """, (f"%{search_query}%", f"%{search_query}%"))
        else:
            # Fetch all cars
            cur.execute("SELECT * FROM Cars WHERE OwnerID IS NOT NULL")

        cars = cur.fetchall()
        return render_template('cars.html', cars=cars, search_query=search_query)

    except Exception as e:
        app.logger.error(f"Error fetching cars: {str(e)}")
        flash("An error occurred while fetching car data.", "danger")
        return redirect(url_for('index'))

@app.route('/rent', methods=['POST'])
def rent():
    if 'user_id' not in session:
        flash('You must be logged in to rent a car.', 'danger')
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    user_id = session['user_id']
    car_id = request.form['car_id']
    rental_start_date = request.form['rental_start_date']
    rental_end_date = request.form['rental_end_date']
    phone = request.form['phone']

    # Check date validity
    if rental_end_date <= rental_start_date:
        flash('Rental end date must be later than the start date.', 'danger')
        return redirect(url_for('cars'))  # If invalid dates, redirect to cars page

    try:
        cur = mysql.connection.cursor()
        
        # Check if the car is available for the given dates
        cur.execute("""
            SELECT * FROM Rentals
            WHERE CarID = %s AND (
                (RentalStartDate <= %s AND RentalEndDate >= %s) OR
                (RentalStartDate <= %s AND RentalEndDate >= %s) OR
                (RentalStartDate >= %s AND RentalEndDate <= %s)
            )
        """, (car_id, rental_start_date, rental_start_date, rental_end_date, rental_end_date, rental_start_date, rental_end_date))
        
        conflicting_rental = cur.fetchone()

        if conflicting_rental:
            flash('Sorry, the car is not available for the selected dates.', 'danger')
            return redirect(url_for('cars'))  # Redirect to cars page if the car is not available

        # If available, insert the rental into the Rentals table
        cur.execute("""
            INSERT INTO Rentals (UserID, CarID, RentalStartDate, RentalEndDate)
            VALUES (%s, %s, %s, %s)
        """, (user_id, car_id, rental_start_date, rental_end_date))
        mysql.connection.commit()

        flash(f'Reservation done! We will contact you at {phone}.', 'success')  # Success message
        return redirect(url_for('cars'))  # Redirect to cars page after successful reservation

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')  # Display error message
        return redirect(url_for('cars'))  # Redirect back to cars page
    
# Route to view offers (discounted cars)
@app.route('/offers', methods=['GET'])
def offers_page():
    search_query = request.args.get('search', '')  # Get the search query if present
    try:
        cur = mysql.connection.cursor()
        
        # Fetch cars with active offers
        if search_query:
            cur.execute("""
                SELECT * FROM Cars
                WHERE Offers LIKE %s AND OwnerID IS NOT NULL
            """, (f"%{search_query}%",))
        else:
            cur.execute("SELECT * FROM Cars WHERE Offers IS NOT NULL AND OwnerID IS NOT NULL")

        cars = cur.fetchall()

        if not cars:
            flash('No offers available at the moment.', 'info')

        return render_template('offers.html', cars=cars, search_query=search_query)

    except Exception as e:
        app.logger.error(f"Error fetching offers: {str(e)}")
        flash("An error occurred while fetching car offers.", "danger")
        return redirect(url_for('index'))


@app.route('/manage_cars')
def manage_cars():
    return render_template('manage_cars.html')

# #######################################################################################################
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if 'user_id' not in session:
        flash('You must be logged in to add a car.', 'danger')
        return redirect(url_for('login'))
    app.logger.info('Start the Add_Car block')
    car_name = request.form['carName']
    car_year = request.form['carYear']
    fuel_type = request.form['fuelType']
    price_per_day = request.form['pricePerDay']
        
    cur = mysql.connection.cursor()
    
    # Insert new car into the database
    cur.execute("INSERT INTO cars (Name, Year, Fuel_Type, Price_Per_Day,OwnerID) VALUES (%s, %s, %s, %s, %s)", (car_name, car_year, fuel_type, price_per_day, session['user_id']))
    mysql.connection.commit()
    app.logger.info(session['user_id'])
    cur.execute("SELECT Carid, Name, Year, Fuel_Type, Price_Per_Day FROM cars WHERE OwnerID = %s", (session['user_id'],))
    cars = cur.fetchall()
    cur.close()
    app.logger.info(f"Retrieved cars: {cars}")

    return render_template('manage_cars.html', OwnerCars=cars)
# #######################################################################################################

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        flash('You must be logged in to add a car.', 'danger')
        return redirect(url_for('login'))
    # Delete the item from the database
    app.logger.info('Start the Delete_Car block')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE CarID = %s", (item_id,))
    mysql.connection.commit()
    return redirect(url_for('manage_cars'))

reviews = []

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    new_review = {
        'id': len(reviews) + 1,
        'user_id': data['user_id'],
        'car_id': data['car_id'],
        'review_text': data['review_text'],
        'rating': data['rating'],
        'created_at': datetime.now().isoformat()
    }
    reviews.append(new_review)
    return jsonify({'message': 'Review added successfully!', 'review': new_review}), 201

@app.route('/reviews/<int:car_id>', methods=['GET'])
def get_reviews(car_id):
    car_reviews = [r for r in reviews if r['car_id'] == car_id]
    return jsonify(car_reviews), 200

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/favorites')
def view_favorites():
    # Assuming you're storing favorites in a session or database
    favorites = session.get('favorites', [])  # This is just an example
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    app.run(debug=True)
