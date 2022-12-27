#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import requests

from py_zipkin.util import generate_random_64bit_string
from py_zipkin.zipkin import create_http_headers_for_new_span
from py_zipkin.zipkin import ZipkinAttrs
from py_zipkin.zipkin import zipkin_span
from flask_zipkin import Zipkin

if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)
    zipkin = Zipkin(app, sample_rate=100)
    app.config['ZIPKIN_DSN'] = "http://oap:9411/api/v2/spans"

    @app.route('/health', methods=['GET'])
    def health():
        return 'OK'


    @app.route('/rcmd', methods=['GET'])
    def application():
        headers = {}
        headers.update(zipkin.create_http_headers_for_new_span())
        print(headers)
        r = requests.get('http://songs/songs', headers=headers)
        recommendations = r.json()
        return jsonify(recommendations)


    PORT = os.getenv('PORT', 81)
    app.run(host='0.0.0.0', port=PORT)
