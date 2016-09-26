# Ansible AWS Hello World

Creates a running instance of a web server on Amazon EC2, displaying
a simple Hello World page.  Redirects all non-secure requests to HTTPS.

Includes a testing script that uses Ansible's EC2 dynamic inventory script
to retrieve the host names of instances created with the script, then
performs an HTTP request to them, ensuring that the redirect to HTTPS takes
place and that a response resembling an HTML page is returned.

## Usage

1.  Modify `ansible.cfg`, adding the path to your private key file for use
with EC2.
2.  Modify the variables in `hello.yml`, such as the region and number of
instances, as necessary.
3.  Run `./hello.yml`

## Testing

1.  Run `./run-tests.py`
