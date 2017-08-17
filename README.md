# Steganography
This is command line program that can be used to:
- Hide a secret message within an image
- Obtain the secret message hidden within an image

## Usage

### Hide
In order to hide a message within an image you can do:

usage: steg.py hide [-h] filename output_file secret

positional arguments:
  filename     File to hide message in (image)
  output_file  Name of output file containing message
  secret       Secret message to hide

### Reveal
Reveal the message hiding within an image

usage: steg.py reveal [-h] filename

positional arguments:
  filename    File to search for message
