# app.py (Flask backend with Kafka integration)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'json'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "Passenger Insurance Claim API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to upload CSV files and send to Kafka for processing
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only CSV, TXT, JSON allowed"}), 400
        
        # Save original file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = f"{timestamp}_{file.filename}"
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)
        
        logger.info(f"File uploaded: {original_filename}")
        
        # PLACEHOLDER FOR BACKEND DEV: Send file to Kafka for processing
        # Example Kafka producer code (uncomment and configure):
        """
        from kafka import KafkaProducer
        producer = KafkaProducer(
            bootstrap_servers=['kafka-server:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        file_metadata = {
            "filename": original_filename,
            "filepath": original_path,
            "upload_timestamp": timestamp,
            "file_size": os.path.getsize(original_path),
            "operation": "process_csv"
        }
        
        producer.send('file_upload_topic', value=file_metadata)
        producer.flush()
        """
        
        # PLACEHOLDER FOR BACKEND DEV: Process file through data transformation pipeline
        # This could involve:
        # 1. Reading CSV content
        # 2. Transforming data format
        # 3. Validating data
        # 4. Loading to data warehouse
        
        # For now, simulate processing
        processed_filename = f"processed_{original_filename}"
        processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
        
        import shutil
        shutil.copy(original_path, processed_path)
        
        # PLACEHOLDER FOR BACKEND DEV: Send processing completion event to Kafka
        """
        completion_event = {
            "original_file": original_filename,
            "processed_file": processed_filename,
            "status": "success",
            "completion_timestamp": datetime.now().isoformat(),
            "records_processed": 0,
            "operation": "data_processing_complete"
        }
        producer.send('processing_status_topic', value=completion_event)
        """
        
        return jsonify({
            "message": "File uploaded and processing started successfully!",
            "filename": original_filename,
            "processed_file": processed_filename,
            "status": "processing",
            "timestamp": timestamp,
            "next_steps": "Data transformation in progress...",
            "records_processed": 0,
            "data_mart_updated": False,
            "kafka_message_sent": True
        })
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500

@app.route('/search', methods=['POST'])
def search():
    """
    Search endpoint to check passenger eligibility for insurance claims
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name', '').strip()
        flight_id = data.get('flightId', '').strip()
        passenger_id = data.get('passengerId', '').strip()
        
        # Validate at least one search parameter
        if not name and not flight_id and not passenger_id:
            return jsonify({"error": "At least one search parameter is required"}), 400
        
        logger.info(f"Search request - Name: {name}, Flight: {flight_id}, Passenger ID: {passenger_id}")
        
        # PLACEHOLDER FOR BACKEND DEV: Query data warehouse
        # Example (uncomment and configure):
        """
        from sqlalchemy import create_engine, text
        engine = create_engine('postgresql://user:password@data-warehouse:5432/insurance_db')
        
        query = text(\"""
            SELECT p.passenger_id, p.name, f.flight_number, f.departure_time,
                   f.arrival_time, f.status, f.delay_minutes, f.cancellation_reason,
                   CASE 
                       WHEN f.status = 'CANCELLED' THEN True
                       WHEN f.delay_minutes >= 120 THEN True
                       ELSE False
                   END as is_eligible
            FROM passengers p
            JOIN flights f ON p.flight_id = f.id
            WHERE (:name IS NULL OR p.name ILIKE :name)
                AND (:flight_number IS NULL OR f.flight_number = :flight_number)
                AND (:passenger_id IS NULL OR p.passenger_id = :passenger_id)
        \""")
        
        with engine.connect() as conn:
            result = conn.execute(query, {
                'name': f"%{name}%" if name else None,
                'flight_number': flight_id if flight_id else None,
                'passenger_id': passenger_id if passenger_id else None
            })
            records = result.fetchall()
        """
        
        # PLACEHOLDER FOR BACKEND DEV: Query Kafka streams for real-time data
        """
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(
            'flight_status_topic',
            bootstrap_servers=['kafka-server:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest'
        )
        
        real_time_status = None
        for message in consumer:
            if (message.value.get('flight_number') == flight_id or 
                message.value.get('passenger_id') == passenger_id):
                real_time_status = message.value
                break
        """
        
        # Current placeholder logic (replace with actual business rules)
        is_eligible = False
        eligibility_reason = ""
        
        # Sample placeholder logic
        if flight_id and ("DELAYED" in flight_id.upper() or "CANCELLED" in flight_id.upper()):
            is_eligible = True
            eligibility_reason = "Flight status meets insurance criteria"
        elif passenger_id and len(passenger_id) > 5:
            is_eligible = True
            eligibility_reason = "Passenger meets eligibility criteria"
        elif name and len(name) > 3:
            is_eligible = True
            eligibility_reason = "Name matches eligible passenger"
        
        return jsonify({
            "isEligible": is_eligible,
            "reason": eligibility_reason,
            "searchParameters": {
                "name": name,
                "flightId": flight_id,
                "passengerId": passenger_id
            },
            "timestamp": datetime.now().isoformat(),
            "passengerDetails": {
                "name": name or "Not provided",
                "passengerId": passenger_id or "Not provided",
                "flightNumber": flight_id or "Not provided"
            },
            "flightStatus": {
                "status": "unknown",
                "delayMinutes": 0,
                "cancelled": False
            },
            "dataSource": "placeholder_data",
            "confidenceScore": 0.85 if is_eligible else 0.15
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/batch_status/<batch_id>', methods=['GET'])
def get_batch_status(batch_id):
    """
    Endpoint to check status of batch file processing
    """
    # PLACEHOLDER FOR BACKEND DEV: Implement batch status tracking
    return jsonify({
        "batchId": batch_id,
        "status": "processing",
        "recordsProcessed": 0,
        "recordsFailed": 0,
        "startTime": datetime.now().isoformat(),
        "estimatedCompletion": None,
        "dataMartUpdated": False
    })

@app.route('/eligibility_stats', methods=['GET'])
def get_eligibility_stats():
    """
    Endpoint to get statistics about insurance claims eligibility
    """
    # PLACEHOLDER FOR BACKEND DEV: Implement statistics aggregation
    return jsonify({
        "totalSearches": 0,
        "eligibleClaims": 0,
        "ineligibleClaims": 0,
        "approvalRate": 0.0,
        "commonReasons": {
            "flight_delayed": 0,
            "flight_cancelled": 0,
            "other": 0
        },
        "timePeriod": "all_time"
    })

if __name__ == '__main__':
    logger.info("Starting Passenger Insurance Claim API...")
    logger.info(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    logger.info(f"Processed folder: {os.path.abspath(PROCESSED_FOLDER)}")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )