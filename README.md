What?
=====

The Swedish Postal Service runs a package tracking API used by
a lot of web stores and third party utilities that provides 
package tracking for customers.

This is a (very incomplete) attempt at creating a mock of that service.

With the web interface, you'll be able to simulate
the package tracking API.

How?
====

This is a small web service that uses the [webapp framework][webapp]. It uses WSGI and you can
run it as is on [Google App Engine][gae].

[webapp]: http://code.google.com/appengine/docs/python/tools/webapp/
[gae]: http://code.google.com/appengine/

License?
========
Copyright [2010] [Johan Mjönes]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 