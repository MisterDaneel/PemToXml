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
import argparse
#
# CreateXMLPubKey
#
def pubKeyXML(pemPublicKeyFile):
   with open (pemPublicKeyFile, 'rb') as pkFile:
      pemPublicKey = pkFile.read()
      pkFile.close()
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
   open (fileName+'.xml', 'w').write(xml)
   return
#
# CreateXMLPrivKey
#
def privKeyXML(pemPrivateKeyFile):
   with open (pemPrivateKeyFile, 'rb') as pkFile:
      pemPrivKey = pkFile.read()
      pkFile.close()
   lines = pemPrivKey.replace(" ", '').split()
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
   open (fileName+'.xml', 'w').write(xml)
   return 
#
# Parser args
#
def parse_args():
   """Create the arguments"""
   parser = argparse.ArgumentParser()
   parser.add_argument("-pub", "--public", help="Encrypt file")
   parser.add_argument("-priv", "--private", help="Decrypt file")
   return parser.parse_args()
#
# Main
#
def main(args):
   if args.public:
      inputfile = args.public
      pubKeyXML(inputfile)
   elif args.private:
      inputfile = args.private
      privKeyXML(inputfile)
   else:
      print 'Nothing to do'
if __name__ == "__main__":
   main(parse_args())
