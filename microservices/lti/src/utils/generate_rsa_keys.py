"""
  RSA public and private key generator
  For generating the set of rsa keys, we are using pycryptodome library.
  We have 2 functions below:
    1. get_rsa_keys() => this function will generate and return a pair of
       private and public key

    2. get_rsa_keys_pem() => this function is using get_rsa_keys() to generate
       keys and writing them in 2 separate pem files on local

  Installation on Mac:
  `easy_install pycrypto==2.6.1`
"""

from Crypto.PublicKey import RSA


def get_rsa_keys():
  key = RSA.generate(2048)
  private_key = key.exportKey()
  public_key = key.publickey().exportKey()
  return private_key, public_key


def get_rsa_keys_pem():
  private_key, public_key = get_rsa_keys()

  with open("rsa_private_key.pem", "wb") as rsa_private_key:
    rsa_private_key.write(private_key)

  with open("rsa_public_key.pem", "wb") as rsa_public_key:
    rsa_public_key.write(public_key)


def main():
  get_rsa_keys_pem()


if __name__ == "__main__":
  main()
