from flask import Flask, render_template, jsonify
import psutil
import time

app = Flask(__name__)

prev_counters = None
prev_time = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bandwidth')
def bandwidth():
    global prev_counters, prev_time
    net_io = psutil.net_io_counters()
    current_time = time.time()

    if prev_counters is None:
        prev_counters = net_io
        prev_time = current_time
        return jsonify(upload=0, download=0)

    elapsed = current_time - prev_time
    upload_speed = (net_io.bytes_sent - prev_counters.bytes_sent) / elapsed
    download_speed = (net_io.bytes_recv - prev_counters.bytes_recv) / elapsed

    prev_counters = net_io
    prev_time = current_time

    return jsonify(upload=upload_speed, download=download_speed)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
