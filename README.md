# pygauth
Autonomation of Google Authenticator OTP

Based on the work of [krissrex](https://github.com/krissrex/google-authenticator-exporter)

```diff
! Warning__
! This code is a PoC
! Using it at your own security hole risk !
```

## How it works !

- Get your otp url from google auth app

- From the url, isolate the base64 encoded URI

- Put the base64 in your code

- Run the script

- Enjoy your OTP automation !

## In depth

If you have your gauth secret key backuped from the first install you are lucky, you just need this simple python script

```python
#!/usr/bin/python3

import pyotp

secret = 'YOUR_BACKUPED_BASE32_KEY'

# Creating topt instannce with the secret
totp = pyotp.TOTP(secret)

# gen OTP
print(totp.now())
```

With the result:

```
081876
```

But in general we dont have this key so how to find it ?

### QRcode

First we need to get the qrcode from our gauth app:

Triple dot menu -> Transfer Accounts -> Export Account

This will give you a new qrcode, screen shot it !

### Read the qrcode

Simply use google Lens app who provide the hability to read qrcode from image gallery

### OTP URL

Behind the qrcode there is an url:

    otpauth-migration://offline?data=LONG_BASE64_STRING

"LONG_BASE64_STRING" is exactly what we need !

### Behind the URL

"LONG_BASE64_STRING" is in reality a [protobuf](https://protobuf.dev/) encoded in base64

### Unserialize the protobuf

Before unserialize (or serialize) we need to know the structure of the protobuf.

We are lucky, the structure of the gauth protobuf is weel knowed:

[google_auth.proto](google_auth.proto)

From this structure we need to generate the python code to help us to work with the protobuf.

Google provide a compiler `protoc` for this case (can provide code for many languages)

    protoc --<OUTPUT>=. <FILE.PROTO>
    protoc --python_out=. google_auth.proto

This will generate a python file module `google_auth_pb2.py` who will be included in our script.

Now we can unserialize our protobuf (a.k.a "LONG_BASE64_STRING") and obtain this human readable output:

```
otp_parameters {                                                                                                                                       
  secret: "xxxxxxxxxxxxxxxxxxx"                                                                                                  
  name: "account_name_1"                                                                                                 
  algorithm: ALGO_SHA1                                                                                                                                 
  digits: 1                                                                                                                                            
  type: OTP_TOTP                                                                                                                                       
}                                                                                                                                                      
otp_parameters {                                                                                                                                       
  secret: "yyyyyyyyyyyyy"                                                                                      
  name: "account_name_2"                                                                     
  issuer: "target_site"                                                                                                                        
  algorithm: ALGO_SHA1                                                                                                                                 
  digits: 1                                                                                                                                            
  type: OTP_TOTP                                                                                                                                       
}                                                                                                                                                      
```

- secret: binary representation of the real secret key -> base32

- name: the username
  
- issuer: website to login

The interesting parameter is `secret`

During the unserialization the secret is dumped as binary data.

To get our key we just need to encode the binary data to base32.

The base32 key can now be used to generate our otp code with the script pasted before !
