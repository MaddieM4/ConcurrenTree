## Announcements

### Version 0.5 is out! Commence the cheering!

ConcurrenTree v0.5.0 is hitting stable, and I gotta admit, it has me stoked.
It's been a long time since any sort of official release, too long probably.
The protocol is fairly stable, the codebase has been broken down to a much
more manageable size, and there is much better/more realistic version planning
going on in the issue tracker. At the time of this writing, there are 110 unit
tests that are processed with the automated doctest walker every time it is
run, to prevent regressions from creeping into the code. And while there's
always a long way to go, this is the most solid step forward in awhile here,
and the light at the end of the tunnel is in sight.

Unfortunately, very little of the documentation is up to date, except for the
in-code doctest examples, which are always up to date. Be ye warned to take
anything in the wiki or the doc folder with a brick of salt, as these are
retained for historical purposes more than practical ones, and treating them
like gospel will lead you down confusing paths of nonsense. However, if you are
interested in the anthropology of the long development path this library took,
these are exactly what you're looking for.

From here on out, all documentation will include the library version described
in that documentation, so you can tell when things are out of date, and by how
much. If you don't see a version attached to something, assume it's ancient.

## SIMPLE VERSION:

[JSON](http://json.org/) is a format that lets you take programming-type
objects, like a list or a dictionary, and encode them as text. You can encode
pretty much anything as JSON.

MCP is the open standard protocol I'm working on, which allows you to connect
to a worldwide network and share document updates. These documents can hold any
JSON object, have a permissions system built in, and it's set up so you can't
download an out-of-date copy of the document or have "write collisions" (where
two people try to write at the same time, so nobody knows what it actually
should be).

Orchard is a proof-of-concept MCP node with a friendly web interface. It
encrypts all your data when storing it to disk, and part of MCP is that all
data going through it is encrypted anyways. There are no central servers, and
it's designed so that the network works just as well with just you and your
friend, as it does years down the road with thousands of people on it.

The point of it is not so much MCP, though. That's the underlying protocol.
The important thing is what you can build *on top* of MCP, like a distributed
version of Google Wave, or a software repository that supports live typing for
code collaboration in real time. It's even possible to have a P2P image editor
made out of nothing but a web page!

## TECHNICAL VERSION:

ConcurrenTree is a concurrency solution that does the heavy lifting for you.
It was originally called OT+, but has diverged so much from OT that the name
was beginning to be deceptive.

Designed for distributed networks where there is no guarantee that Machine A
and Machine B have even vaguely similar pictures of a document, CTree is a new
and revolutionary concurrency model that can resolve just about anything. It
includes formatting standards, a protocol for network sync/introduction, and
some example code showing you how to write clients in Javascript.

Why start from scratch, when there's already OT? Well, nothing's stopping you
from using OT if you have stiff memory constraints, as in theory memory usage
is not CTree's strong suite. However, OT has a lot of conceptual problems: it
forces you to track the state of a server in order to submit customized ops,
it uses complex and arcane algorithms that require advanced theorem proving
programs to test, and there is no standard set of those algorithms (meaning
my OT doesn't speak the same language as your OT unless we spend days of work
minimum making sure our algorithms are functionally equivalent, and when I say
days, I'm assuming each of us have half a dozen well-paid competent workers).

CTrees solve all these problems and more. There is no state-tracking, because
any operation can be safely submitted to any peer. And because of that, there's
no need for obtuse and ill-defined algorithms. And because of that, we've
been able to make a simple system with clearly defined correct ways to process
data, no ambiguity or fuzziness here, making it easy to port the model to other
programming languages without wondering constantly whether you're doing it
right. The right way makes sense, you can trust your gut.

This code is under heavy construction, and it's important to understand what
CTree is and is not, so you don't end up waiting for features that are not
going to be added. For example, authentication. The protocol being designed
for ConcurrenTree includes operation signing but leaves the majority of auth
to the larger project implementing CTree to do stuff. CTree is not so much its
own thing, as it is something that's embedded in other projects as a simple
backend that handles all your network concurrency.


Dependencies
============
* python 2.6.6+
* [python-libcps](https://github.com/campadrenalin/python-libcps)
* [python-libejtp](https://github.com/campadrenalin/EJTP-lib-python)
* pycrypto (2.3): https://www.dlitz.net/software/pycrypto/
* Works a lot more efficiently with python-gevent, but doesn't need it.
