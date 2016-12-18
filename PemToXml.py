#!/usr/bin/env python
#
# Converting RSA PEM key (PKCS#1) to XML compatible for .Net
# from https://github.com/MisterDaneel/
#
# Need pycrypto installed.
#
from Crypto.Util import number
from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
from base64 import standard_b64encode, b64decode
from binascii import a2b_base64
from os.path import basename, exists
from xml.dom import minidom
import argparse
#
# CreateXMLPubKey
#
def pubKeyXML(pemPublicKeyFile):
   with open (pemPublicKeyFile, 'rb') as pkFile:
      pemPublicKey = pkFile.read()
   publicKey = RSA.importKey(pemPublicKey)
   xml  = '<RSAKeyValue>'
   xml += '<Modulus>'
   xml += standard_b64encode(number.long_to_bytes(publicKey.n))
   xml += '</Modulus>'
   xml += '<Exponent>'
   xml += standard_b64encode(number.long_to_bytes(publicKey.e))
   xml += '</Exponent>'
   xml += '</RSAKeyValue>'
   fileName = basename(pemPublicKeyFile)
   with open (fileName+'.xml', 'w') as pkFile:
      pkFile.write(xml)
   return
#
# CreateXMLPrivKey
#
def privKeyXML(pemPrivateKeyFile):
   with open (pemPrivateKeyFile, 'rb') as pkFile:
      pemPrivKey = pkFile.read()
   print pemPrivKey
   lines = pemPrivKey.replace(" ", '').split()
   print lines
   keyDer = DerSequence()
   keyDer.decode(a2b_base64(''.join(lines[1:-1])))
   xml  = '<RSAKeyValue>'
   xml += '<Modulus>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[1]))
   xml += '</Modulus>'
   xml += '<Exponent>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[2]))
   xml += '</Exponent>'
   xml += '<D>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[3]))
   xml += '</D>'
   xml += '<P>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[4]))
   xml += '</P>'
   xml += '<Q>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[5]))
   xml += '</Q>'
   xml += '<DP>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[6]))
   xml += '</DP>'
   xml += '<DQ>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[7]))
   xml += '</DQ>'
   xml += '<InverseQ>'
   xml += standard_b64encode(number.long_to_bytes(keyDer[8]))
   xml += '</InverseQ>'
   xml += '</RSAKeyValue>'
   fileName = basename(pemPrivateKeyFile)
   with open (fileName+'.xml', 'w') as pkFile:
      pkFile.write(xml)
   return
#
# Get Long Int
#
def GetLong(nodelist):
   rc = []
   for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
         rc.append(node.data)
   string = ''.join(rc) 
   return number.bytes_to_long(b64decode(string))
#
# CreatePEMPubKey
#
def pubKeyPEM(xmlPublicKeyFile):
   with open (xmlPublicKeyFile, 'rb') as pkFile:
      xmlPublicKey = pkFile.read()
   rsaKeyValue = minidom.parseString(xmlPublicKey)
   modulus = GetLong(rsaKeyValue.getElementsByTagName('Modulus')[0].childNodes)
   exponent = GetLong(rsaKeyValue.getElementsByTagName('Exponent')[0].childNodes)
   publicKey = RSA.construct((modulus, exponent))
   fileName = basename(xmlPublicKeyFile)
   with open (fileName+'.pem', 'w') as pkFile:
      pkFile.write(publicKey.exportKey())
   return
#
# CreatePEMPrivKey
#
def privKeyPEM(xmlPrivateKeyFile):
   with open (xmlPrivateKeyFile, 'rb') as pkFile:
      xmlPrivateKey = pkFile.read()
   rsaKeyValue = minidom.parseString(xmlPrivateKey)
   modulus = GetLong(rsaKeyValue.getElementsByTagName('Modulus')[0].childNodes)
   exponent = GetLong(rsaKeyValue.getElementsByTagName('Exponent')[0].childNodes)
   d = GetLong(rsaKeyValue.getElementsByTagName('D')[0].childNodes)
   p = GetLong(rsaKeyValue.getElementsByTagName('P')[0].childNodes)
   q = GetLong(rsaKeyValue.getElementsByTagName('Q')[0].childNodes)
   qInv = GetLong(rsaKeyValue.getElementsByTagName('InverseQ')[0].childNodes)
   privateKey = RSA.construct((modulus, exponent, d, p, q, qInv))
   with open (fileName+'.pem', 'w') as pkFile:
      pkFile.write(privateKey.exportKey())
   return
#
# Parser args
#
def parse_args():
   """Create the arguments"""
   parser = argparse.ArgumentParser('\nxmlpem.py --xmltopem --public mypublickeyfile.xml\nxmlpem.py --pentoxml --private myprivatekeyfile.pem')
   parser.add_argument("-pub", "--public", help="Public Key")
   parser.add_argument("-priv", "--private", help="Private Key")
   parser.add_argument("-xtop", "--xmltopem", help="XML to PEM", action='store_true')
   parser.add_argument("-ptox", "--pemtoxml", help="PEM to XML", action='store_true')
   return parser.parse_args()
#
# Main
#
def main(args):
   if args.pemtoxml:
      if args.public:
         inputfile = args.public
         pubKeyXML(inputfile)
      elif args.private:
         inputfile = args.private
         privKeyXML(inputfile)
   elif args.xmltopem:
      if args.public:
         inputfile = args.public
         pubKeyPEM(inputfile)
      elif args.private:
         inputfile = args.private
         privKeyPEM(inputfile)
   else:
      print 'Nothing to do'
if __name__ == "__main__":
   main(parse_args())
