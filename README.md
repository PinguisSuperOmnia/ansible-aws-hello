# Ansible AWS Hello World

Creates a running instance of a web server on Amazon EC2, displaying
a simple Hello World page.  Redirects all non-secure requests to HTTPS.

Includes a testing script that uses Ansible's EC2 external inventory script
to retrieve the host names of instances created with the script, then
performs an HTTP request to them, ensuring that the redirect to HTTPS takes
place and that a response resembling an HTML page is returned.

## Usage

1.  Modify `ansible.cfg`, adding the path to your SSH private key file for use
with EC2.
2.  Modify the variables in `hello.yml`, such as the region and number of
instances, as necessary.
3.  Run `./hello.yml`

## Testing

1.  Run `./run-tests.py`

## Development Process
This was my first introduction to Ansible.  To help me get started, I began
working through the *O'Reilly* book *Ansible: Up and Running*.  The examples
in Chapters 1, 2, and 12 served as a starting point for this project.

Of course, I did much more than simply copy examples from a book.  As I was
working through the book, I was making sure to build something that was suited
to my needs, and nothing more or less.  Here are some things I've done that
are absent from the examples:

* I'm using only the code that I need (and I've made doubly sure that I
understand all of the code I'm using).
* Fixed all warnings, such as deprecation warnings.
* Set up `public/` folder containing `index.html` and `robots.txt`, and set
up the web role to synchronize all contents of that folder.  The `robots.txt`
file was added to block all search engines from crawling the site, since we
don't want that.
* Automated TLS certificate generation, and made this happen on the host
machine, with certificate files stored in the unversioned `files/` directory
that it creates.  This is done because if we have multiple instances, we
still want them to be using the same TLS cert.
* Set up nginx to redirect all HTTP requests to HTTPS.
* Wrote a testing script in Python.  Python is something
I taught myself over the past few months, and I haven't yet developed with it
professionally, but I chose Python because it's going to be installed on
any machine that runs Ansible, and it's neither overkill nor underkill for what
I needed it for here - it seemed like the right tool for the job.  While I
believe that the script is efficient and readable as it stands, and gets
the job done, I'm confident that with more experience, my Python skills
will grow tremendously.

## TODOs
* Create a playbook to terminate all instances.  This can actually be done right
now by changing `count` to `0` in `hello.yml`, but the process isn't intuitive,
and the messages Ansible outputs suggest that it's actually creating
servers, not terminating them.
* The basic idea behind scaling this, as it exists now, is to simply increase
the `count` in `hello.yml`, then set up load balancing separately.  However, if
I had more time, another possibility would be to utilize something like Amazon's
Elastic Load Balancing.
* Implement monitoring.  Amazon's CloudWatch can be integrated with Ansible,
or instead, we could install some standalone monitoring tools on the servers
using Ansible.

## Credits
* [Ansible: Up and Running code samples](https://github.com/lorin/ansiblebook)
* The [EC2 external inventory script](https://github.com/ansible/ansible/blob/devel/contrib/inventory/ec2.py)
and [.ini file](https://github.com/ansible/ansible/blob/devel/contrib/inventory/ec2.ini)
from the [Ansible](https://github.com/ansible/ansible) project
