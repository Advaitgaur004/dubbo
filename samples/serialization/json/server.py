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
from typing import Dict

import orjson

import dubbo
from dubbo.configs import ServiceConfig
from dubbo.proxy.handlers import RpcMethodHandler, RpcServiceHandler


def request_deserializer(data: bytes) -> Dict:
    return orjson.loads(data)


def response_serializer(data: Dict) -> bytes:
    return orjson.dumps(data)


def handle_unary(request):
    print(f"Received request: {request}")
    return {"message": f"Hello, {request['name']}"}


if __name__ == "__main__":
    # build a method handler
    method_handler = RpcMethodHandler.unary(
        handle_unary,
        request_deserializer=request_deserializer,
        response_serializer=response_serializer,
    )
    # build a service handler
    service_handler = RpcServiceHandler(
        service_name="org.apache.dubbo.samples.serialization.json",
        method_handlers={"unary": method_handler},
    )

    service_config = ServiceConfig(service_handler)

    # start the server
    server = dubbo.Server(service_config).start()

    input("Press Enter to stop the server...\n")
