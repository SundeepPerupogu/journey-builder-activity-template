from flask import Flask, request, jsonify
import datetime
import pytz

app = Flask(__name__)

def parse_timezone_offset(tz):
    try:
        hours, minutes = map(int, tz[3:].split(':'))
        offset = datetime.timedelta(hours=hours, minutes=minutes)
        return offset
    except ValueError:
        return None

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    in_arguments = data['inArguments'][0]
    future_utc_time = in_arguments.get('futureUtcTime')
    user_time_zone = in_arguments.get('userTimeZone')

    if not future_utc_time or not user_time_zone:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        current_utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        future_utc_datetime = datetime.datetime.strptime(future_utc_time, '%H:%M:%S').replace(
            year=current_utc_time.year, 
            month=current_utc_time.month, 
            day=current_utc_time.day, 
            tzinfo=pytz.utc
        )

        offset = parse_timezone_offset(user_time_zone)
        if offset is None:
            return jsonify({'error': 'Invalid time zone format.'}), 400

        current_time_user_tz = current_utc_time + offset
        time_difference = future_utc_datetime - current_time_user_tz

        return jsonify({'timeDifference': str(time_difference)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/publish', methods=['POST'])
def publish():
    return jsonify({}), 200

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    in_arguments = data['arguments']['execute']['inArguments']

    if not in_arguments:
        return jsonify({'error': 'No configuration data provided'}), 400

    future_utc_time = in_arguments[0].get('futureUtcTime')
    user_time_zone = in_arguments[0].get('userTimeZone')

    if not future_utc_time or not user_time_zone:
        return jsonify({'error': 'Configuration data is missing required fields'}), 400

    return jsonify({}), 200

@app.route('/stop', methods=['POST'])
def stop():
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
