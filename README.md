# PemToXml

Converting RSA PEM key (PKCS#1) to XML compatible for .Net
```csharp

	using System;
    using System.Text;
    using System.Security.Cryptography;
```
```csharp

	private static readonly string privateKeyXml = "...";
    private static readonly string publicKeyXml = "...";

    // see https://msdn.microsoft.com/en-us/library/system.security.cryptography.rsacryptoserviceprovider.aspx
    // let exception be thrown if error
    public static string Encrypt(string data)
    {
        if (string.IsNullOrEmpty(data))
        {
            return null;
        }
        byte[] dataToEncrypt = Encoding.UTF8.GetBytes(data);
        byte[] encryptedData;
        using (RSACryptoServiceProvider rsa = new RSACryptoServiceProvider())
        {
            rsa.FromXmlString(publicKeyXml);
            encryptedData = rsa.Encrypt(dataToEncrypt, false);
        }
        return Convert.ToBase64String(encryptedData); 
    }

    // let exception be thrown if error
    public static string Decrypt(string data)
    {
        if (string.IsNullOrEmpty(data))
        {
            return null;
        }
        byte[] dataToDencrypt = Convert.FromBase64String(data);
        byte[] decryptedData;
        using (RSACryptoServiceProvider rsa = new RSACryptoServiceProvider())
        {
            rsa.FromXmlString(privateKeyXml);
            decryptedData = rsa.Decrypt(dataToDencrypt, false);
        }
        return Encoding.UTF8.GetString(decryptedData);
    }
```

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

Convert a public key from XML to PEM: `python PemToXml.py -ptox -priv "path/to/private.pem"`

Convert a public key from PEM to XML: `python PemToXml.py -xtop -priv "path/to/private.xml"`