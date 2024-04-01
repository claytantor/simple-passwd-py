import click
import os

# use from Crypto.Cipher import AES to encrypt the file
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2, scrypt
import os

import pandas as pd

def strip_non_ascii(string):
    stripped_string = ""
    for char in string:
        if ord(char) < 128:
            stripped_string += char
    return stripped_string

def pad(data):
    block_size = AES.block_size
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding

def encrypt_file(file_path, password):
    # Generate a random salt
    salt = get_random_bytes(AES.block_size)

    # Derive key from password using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)

    # Create AES cipher object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC)

    # Read file content and pad it
    with open(file_path, 'rb') as file:
        plaintext = pad(file.read())

    # Encrypt padded file content
    cipher_text = cipher.encrypt(plaintext)

    # Write salt and cipher text to encrypted file
    with open(file_path + '.enc', 'wb') as file:
        file.write(salt + cipher.iv + cipher_text)

def decrypt_file(encrypted_file_path, password):
    # Read salt, IV, and cipher text from encrypted file
    with open(encrypted_file_path, 'rb') as file:
        salt = file.read(AES.block_size)
        iv = file.read(AES.block_size)
        cipher_text = file.read()

    # Derive key from password and salt using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)

    # Create AES cipher object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt cipher text
    plaintext = cipher.decrypt(cipher_text)

    # Remove padding from plaintext
    plaintext = plaintext.rstrip(b'\0')
    plaintext = plaintext.rstrip(b'\b')
    plaintext = plaintext.decode('utf-8')
    plaintext = strip_non_ascii(plaintext)

    # Write decrypted file content
    with open(encrypted_file_path[:-4], 'w') as file:
        file.write(plaintext)
   
@click.group()
def cli():
    pass

@cli.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name",
              help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo("Hello, %s!" % name)

@cli.command()
@click.option("--password", prompt="Your password",
              help="The password to decrypt.")
@click.option("--input", prompt="Input file",
                help="The file to decrypt.")
def encrypt(password, input):
    """Simple program that encrypts a password."""
    encrypt_file(input, password)

    # delete the original db
    os.remove(input)

    click.echo("Encrypted file saved at %s" % input + ".enc")

@cli.command()
@click.option("--password", prompt="Your password",
              help="The password to decrypt.")
@click.option("--input", prompt="Input file",
                help="The file to decrypt.")
def decrypt(password, input):
    """Simple program that decrypts a password."""
    decrypt_file(input, password)

    # delete the original db
    os.remove(input)

    click.echo("Decrypted file saved at %s" % input.replace('.enc', ''))

@cli.command()
@click.option('--title', prompt='title to find',
              help='Use a title that allows lookup.')
@click.option('--db', prompt='path to db file',
                help='Use a path to the passwod db file.')
def find(title, db):
    # load the csv file as a pandas dataframe
    df = pd.read_csv(db, sep='|')
    click.echo(df[df['Title'] == title])

if __name__ == '__main__':
    cli()