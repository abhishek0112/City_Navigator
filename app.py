import logging
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)

# Function to connect to the database
def get_db_connection():
    try:
        conn = sqlite3.connect('city_navigator.db')
        conn.row_factory = sqlite3.Row
        logger.info("Database connected successfully")
        return conn
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")
        return None

@app.route('/')
def index():
    logger.info("Index route accessed")
    return render_template('index.html')

@app.route('/bus')
def bus():
    current_location = request.args.get('location')
    current_destination = request.args.get('destination')
    logger.info(f"Bus route accessed with location: {current_location} and destination: {current_destination}")
    if current_location and current_destination:
        buses = get_bus_details(current_location, current_destination)
        return render_template('bus_details.html', buses=buses)
    else:
        logger.warning("Location or destination parameter is missing")
        return "Location parameter is missing", 400

@app.route('/railway')
def railway():
    current_location = request.args.get('location')
    current_time = request.args.get('time')
    current_destination = request.args.get('destination')
    logger.info(f"Railway route accessed with location: {current_location}, time: {current_time}, and destination: {current_destination}")
    if current_location and current_time and current_destination:
        trains = get_railway_details(current_location, current_time, current_destination)
        return render_template('railway_details.html', trains=trains)
    else:
        logger.warning("Time or destination parameter is missing")
        return "Time parameter is missing", 400

def get_bus_details(location, destination):
    conn = get_db_connection()
    if conn:
        try:
            query = 'SELECT * FROM buses WHERE location = ? AND destination = ?'
            buses = conn.execute(query, (location, destination)).fetchall()
            logger.info(f"Fetched {len(buses)} bus records for location: {location} and destination: {destination}")
            return buses
        except sqlite3.Error as e:
            logger.error(f"An error occurred while fetching bus details: {e}")
            return []
        finally:
            conn.close()
    return []

def get_railway_details(location, time, destination):
    conn = get_db_connection()
    if conn:
        try:
            query = 'SELECT * FROM trains WHERE location = ? AND time >= ? AND destination = ?'
            trains = conn.execute(query, (location, time, destination)).fetchall()
            logger.info(f"Fetched {len(trains)} train records for location: {location}, time: {time}, and destination: {destination}")
            return trains
        except sqlite3.Error as e:
            logger.error(f"An error occurred while fetching railway details: {e}")
            return []
        finally:
            conn.close()
    return []

if __name__ == '__main__':
    app.run(debug=True)
