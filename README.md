nameserver
==========

Simple module to create and destroy A and CNAME records on a bind server where we have update rights

This is a very simplified implementation for basic creation and destruction of
A and CNAME records. The ttl is hardcoded to 300. You'll need to configure your
DNS bind server to accept updates from the machine you are using this (see
the bind allow-update feature help for this.
