"""! @file encoder_reader.V2.py
"""

''' 
   \brief     ME 405 Week 5 Lab 2
   \details   This program controls a motor and returns and alters the timer counter values using an Encoder object
   \author    Jenna Mast, Emily Mendyke
   \version   2.0
   \date      2/15/2024
   \Todo      Add to github
'''

import pyb
import time

class Encoder:
    def __init__(self, tim_num, chanA_pin, chanB_pin):
        """! 
        Creates a motor encoder object
        @param  tim_num: a timer number parameter that can be altered later for specific corresponding encoder
        @param  chanA_pin: a channel 1 parameter that will have different timer numbers for either encoder 1 or 2
        @param  chanB_pin: a channel 2 parameter that will have different timer numbers for either encoder 1 or 2
        """
        
        # Set the timer, prescaler, and period. More technically, creates a timer object,
        # tim, within the encoder class so we can access Timer class variables and functions/methods.
        # and accesses the.
        
        self.tim = pyb.Timer(tim_num, prescaler=0, period=65535)
        

        # Set up the encoder mode for the timer
        # More technically it uses the timer object, tim, that we've created in the Encoder class,
        # and uses it to call the Timer class channel functiom.
        
        self.tim.channel(1, pyb.Timer.ENC_AB, pin=chanA_pin)
        self.tim.channel(2, pyb.Timer.ENC_AB, pin=chanB_pin)
        self.val_i = self.tim.counter()                       # Set inital counter value
        self.pos = 0                                          # Set initial position to 0
        
    def read(self):
        """!
        This method reads the current values of the counter
        and also checks for overflow
        """
        
        val_f = self.tim.counter()         # Set the current value of the counter
        diff = val_f - self.val_i          # Find the difference between the initial and current values of the counter
        
        # Check for overflow
        if diff > 32767:
            diff = diff - 65536
        
        # Check for underflow
        if diff < -32768:
            diff = diff + 65536
            
        self.pos = self.pos + diff         # Calculate position
        self.val_i = val_f                 # Reset initial value
        return self.pos                    # Return position
        
    def zero(self):
        """!
        This method sets the count to zero at the current position
        """
        self.pos = 0                       # Reset position in software
        self.tim.counter(0)                # Reset the hardware counter
        self.val_i = self.tim.counter()    # Reset initial value
        
        

if __name__ == "__main__":
        
    """!
    The test code creates 2 encoder instances, stores initial encoder value, and
    subsequently tests the methods "read()" and "zero()"
    from the Encoder class
        """
    encoder1 = Encoder(4, pyb.Pin.board.PB6, pyb.Pin.board.PB7)  # Create encoder 1 instance
    encoder2 = Encoder(8, pyb.Pin.board.PC6, pyb.Pin.board.PC7)  # Create encoder 2 instance
    
    read1M1 = 0                                  # Stores initial encoder 1 value
    read1M2 = 0                                  # Stores initial encoder 2 value
   
    while True:
        read2M1 = encoder1.read()                # Gets final encoder 1 value
        if read2M1 != read1M1:                   # If the count of the encoder has changed
            print("Motor 1:", read2M1)           # print it
            read1M1 = read2M1                    # Set final count to initial
            
        read2M2 = encoder2.read()                # Same as above but for encoder 2
        if read2M2 != read1M2:
            print("Motor 2:", read2M2)
            read1M2 = read2M2

    
    