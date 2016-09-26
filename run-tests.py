#!/usr/bin/env python2

import json
import os.path
import re
import subprocess
import sys
import urllib2

EC2_TAG_TYPE = 'web'
EC2_TAG_NAME = 'hello'
EC2_TAG_ENV = 'production'
URL_REQUEST_TIMEOUT = 5

def get_hosts():
  ''' Use EC2 dynamic inventory script to grab list of servers tagged as required '''
  ec2_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory', 'ec2.py')
  try:
    ec2_script_output = subprocess.check_output([ec2_script_path, '--list'])
  except:
    print_error_and_exit("Error running EC2 dynamic inventory script.")
  try:
    ec2_inventory = json.loads(ec2_script_output)
  except ValueError:
    print_error_and_exit("Unable to decode output from EC2 dynamic inventory script.")
  hosts = []
  if '_meta' in ec2_inventory and 'hostvars' in ec2_inventory['_meta']:
    for host in ec2_inventory['_meta']['hostvars'].values():
      if ('ec2_dns_name' in host and
          'ec2_tag_type' in host and host['ec2_tag_type'] == EC2_TAG_TYPE and
          'ec2_tag_Name' in host and host['ec2_tag_Name'] == EC2_TAG_NAME and
          'ec2_tag_env' in host and host['ec2_tag_env'] == EC2_TAG_ENV):
        hosts.append(host['ec2_dns_name'])
  return hosts

def print_error_and_exit(message):
  ''' Print error to stdout (not stderr) and exit with status code 1 '''
  print message
  sys.exit(1)

def run_tests(host):
  ''' For a given host, connect via HTTP and perform a series of tests '''
  print "Running tests for host " + host + "...\n"

  http_url = 'http://' + host + '/'
  print "Opening URL " + http_url + "..."
  try:
    url_file = urllib2.urlopen(http_url, None, URL_REQUEST_TIMEOUT)
  except urllib2.URLError:
    print_error_and_exit("Failure.")
  print "Success\n"

  print "Checking if request is redirected to HTTPS..."
  if (url_file.geturl() != 'https://' + host + '/'):
    print_error_and_exit("Failure.")
  print "Success\n"

  print "Checking for opening and closing <html> tags..."
  if not is_valid_webpage(url_file):
    print_error_and_exit("Failure.")
  print "Success\n"

def is_valid_webpage(file):
  ''' Return True if a file contains opening and closing html tags in the correct order,
  or False otherwise '''
  matched_opening_html_tag = False
  for line in file:
    if re.search(r'<html[^>]*>', line):
      matched_opening_html_tag = True
    if matched_opening_html_tag and re.search(r'</html>', line):
      return True
  return False

def main():
  ''' Run tests against each correctly tagged EC2 host '''
  hosts = get_hosts()
  if not hosts:
    print_error_and_exit('No hosts found.')
  for host in hosts:
    run_tests(host)

if __name__ == "__main__":
  main()
