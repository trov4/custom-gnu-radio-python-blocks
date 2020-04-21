# Frequency jumping modules  
The files contained in this directory are frequency jumping modules. These are usefull adhering to v2v communication that requires a frequency hopping signal.  

## Usage  
There are two files here, a direct out and a pmt msg hopper. Both of these perform the same task but with different outputs.  

### pmt message output  
This frequency hopper module is meant to suppliment the the Signal Source Block in gnu radio. The pmt message output from this block can be connected the pmt input on the sig_source block to control the frequency of that block.   
A [pmt message](https://wiki.gnuradio.org/index.php/Message_Passing) is just a method of passing messages around in gnu radio. The input of a pmt message expects a certain form. If the message is that form, then an interupt will be triggered and perform some action. In this module, sending to the sig_source block will change the frequency it sends at.  
The inputs for this block are `base frequency`, the frequency where jumping will begin, `number of frequencies`, how many jumps will occur, and `bandwidth`, the distance between jumps.  
Finally, every block in gnu radio must have an input or an output for the work function to be triggered. So for this block, you can send the output straight to a Null source, while the message output goes to the sig source.  

### direct out hopper  
This builds upon the custom python signal source found in this repo. The output of this block can go directly into a throttle block into an output. The pmt message output has been kept for debug purpose, but it does not need to be hooked up to anything for the block to run.  
The inputs are the same as the pmt output block, however it also expects `sample frequency` which should match the throttle block.
