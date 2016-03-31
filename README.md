# PemToXml

Converting RSA PEM key (PKCS#1) to XML compatible for .Net

Need pycrypto installed.

Convert a public key:

     python PemToXml.py -pub "/foo/bar/publicKey.pem"

Convert a private key:

     python PemToXml.py -priv "/foo/bar/privateKey.pem"
