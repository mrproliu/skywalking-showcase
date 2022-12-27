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

import requests
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs, Kind, zipkin_client_span
from py_zipkin.request_helpers import create_http_headers
from py_zipkin.encoding import Encoding

def default_handler(encoded_span):
    body = encoded_span

    # decoded = _V1ThriftDecoder.decode_spans(encoded_span)
    app.logger.info("body %s", body)

    # return requests.post(
    #     "http://zipkin:9411/api/v1/spans",
    #     data=body,
    #     headers={'Content-Type': 'application/x-thrift'},
    # )

    return requests.post(
        "http://oap:9411/api/v2/spans",
        data=body,
        headers={'Content-Type': 'application/json'},
    )

if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def health():
        return 'OK'


    @app.route('/rcmd', methods=['GET'])
    def application():
        with zipkin_span(
                service_name='songs',
                span_name='/songs',
                transport_handler=default_handler,
                port=5000,
                sample_rate=100,
                encoding=Encoding.V2_JSON
            ):
            headers = create_http_headers()
            print(headers)
            r = requests.get('http://songs/songs', headers=headers)
            recommendations = r.json()
            return jsonify(recommendations)


    PORT = os.getenv('PORT', 80)
    app.run(host='0.0.0.0', port=PORT)
