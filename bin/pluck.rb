#!/usr/bin/env ruby

require "json"

puts JSON.parse($stdin.read)[ARGV[0]].to_json
