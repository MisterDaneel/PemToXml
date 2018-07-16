# PemToXml

Converting RSA PEM key (PKCS#1) to XML compatible for .Net

## Requirements:
1. Tested with python version 2.7
2. Uses pycrypto

For windows you may find binaries here: http://www.voidspace.org.uk/python/modules.shtml#pycrypto

## Tested scenarious:
1. PHP encrypt/decrypt using PEM keys, C# decrypt using coverted PEM to XML keys
2. C# encrypt/decrypt using using XML keys, PHP decrypt using coverted XML to PEM keys

## Usage:
Convert a public key from XML to PEM: `python PemToXml.py -ptox -pub "path/to/public.pem"`
Convert a public key from PEM to XML: `python PemToXml.py -xtop -pub "path/to/public.xml"`
Convert a public key from XML to PEM:`python PemToXml.py -ptox -priv "path/to/private.pem"`
Convert a public key from PEM to XML:`python PemToXml.py -xtop -priv "path/to/private.xml"`