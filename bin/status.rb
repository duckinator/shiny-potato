#!/usr/bin/env ruby

require "json"

puts {"status" => ARGV[0]}.to_json
