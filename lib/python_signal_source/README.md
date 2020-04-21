Signal Source  
=============  
custom_sig_souce.py is a custom signal source that will output a complex signal straight out from the python block. If you take use the following flow:  
custom_sig_source -> throttle -> output  
The output will be expected value.  

## Usage  
This python block accepts two inputs `frequency` and `sample rate`. This acts just as the sig_souce block found in base GNU radio. There is a pmt message port and a complex output. The pmt message port is used for debuging.

The intent of this block is that you are able to easily add to it. See ascii_spectrum_painter for an example, you will still be able to see the base of what is in this file.