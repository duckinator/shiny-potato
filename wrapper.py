#!/usr/bin/env python3

import falcon
import subprocess
from subprocess import PIPE

# /handler_name/:var1/:var2 => ["./handler_exectuable", "var1", "var2"]
# /ua => ["./ua.rb"]
# /status/:status_code

fns = {
  # POST /pluck/test
  # -> with body {"test": "awoo"}
  # => "awoo"
  "/pluck/{key}":       ["post",        "./bin/pluck.rb", ":key"],
  "/ua":                ["get",         "./bin/ua.rb"],
  "/echo":              ["get",         "./bin/echo.rb", ":text"],
}

class Handler:
    def __init__(self, route, raw_command):
        self.request_type, *self.command = raw_command
        self.route = route
        print("Creating route: {} {} => {}".format(self.request_type, route, " ".join(command)))

    def normalize_param(self, param, params):
        if param[0] == ":":
            return params[param[1:]]
        else:
            return param

    def normalize_command(self, command, params):
        return list(map(lambda x: self.normalize_param(x, params), command))

    def run(self, req, stdin, params):
        command = self.normalize_command(self.command, req.params)
        result = subprocess.run(command, input=stdin, stderr=PIPE, stdout=PIPE)

        content_type = falcon.MEDIA_TEXT

        if result.returncode == 0:
            return_code = falcon.HTTP_200
        else:
            return_code = falcon.HTTP_500 # TODO: Allow control of error code?

        return [return_code, content_type, result.stdout]

    def invalid_request_type(self, resp):
        resp.status = falcon.HTTP_405
        resp.content_type = falcon.MEDIA_TEXT

    def on_get(self, req, resp, **params):
        if self.request_type != "get":
            return self.invalid_request_type(resp)

        resp.status, resp.content_type, resp.body = self.run(req, None, params)

    def on_post(self, req, resp, **params):
        if self.request_type != "post":
            return self.invalid_request_type(resp)

        resp.status, resp.content_type, resp.body = self.run(req, req.bounded_stream)

app = falcon.API()
for (route, command) in fns.items():
    app.add_route(route, Handler(route, command))

#"/pluck/:key?thing=stuff"

# public key provider service
#
#
# lingo translation
#
