from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/wifi_profiles')
def get_wifi_profiles():
    data = (subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n'))
    profile = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i ]
    results = []
    for i in profile:
        cmd = ['netsh', 'wlan', 'show', 'profiles', i, 'key=clear']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = proc.communicate()
        output = out.decode('utf-8').split('\n')
        password = [b.split(":")[1][1:-1] for b in output if "Key Content" in b]
        try:
            results.append({"name": i, "password": password[0]})
        except IndexError:
            results.append({"name": i, "password": ""})
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
