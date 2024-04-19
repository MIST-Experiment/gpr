from enum import Enum
import numpy as np
import uhd
from uhd import libpyuhd as lib
import matplotlib.pyplot as plt

__all__ = [
    "States",     
    "StateManager", 
    "usrp_connect",  
    "tune_center_freq",
    "rx_worker",
    "tx_worker",
    "generate_tx_data",
    "plot_scan"
]

from params import *

class States(Enum):
    """Enumerations to represent different states."""
    tune = 1
    scan = 2
    done = 3

class StateManager:
    """Class to manage state transitions."""
    def __init__(self):
        self.state = States.tune
        
    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
    
state_manager = StateManager() 

def usrp_connect():
    
    usrp = uhd.usrp.MultiUSRP("type = b200, num_recv_frames=800, num_send_frames=500")
    usrp.set_clock_source("internal")
        
    #Setting sample rates
    usrp.set_tx_rate(samp_rate)
    usrp.set_rx_rate(samp_rate)
    
    #Setting stream arguments
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = channels
    rx_streamer = usrp.get_rx_stream(st_args)
    tx_streamer = usrp.get_tx_stream(st_args)

    return usrp, rx_streamer, tx_streamer
        
def tune_center_freq(usrp, current_freq, channel_list, tx_gain0, tx_gain1, rx_gain0, rx_gain1):
    """Tune the center frequency and set the appropriate gain."""
    # Tune the center frequencies
    usrp.set_rx_freq(lib.types.tune_request(current_freq), 0)
    usrp.set_rx_freq(lib.types.tune_request(current_freq), 1)
    usrp.set_tx_freq(lib.types.tune_request(current_freq), 0)
    usrp.set_tx_freq(lib.types.tune_request(current_freq), 1)
    #Set gain values
    usrp.set_tx_gain(tx_gain0, channel_list[0])
    usrp.set_tx_gain(tx_gain1, channel_list[1])
    usrp.set_rx_gain(rx_gain0, channel_list[0])
    usrp.set_rx_gain(rx_gain1, channel_list[1])

    # Wait for the local oscillators to lock
    while not(
        usrp.get_rx_sensor("lo_locked", 0).to_bool()
        and usrp.get_rx_sensor("lo_locked", 1).to_bool()
        and usrp.get_tx_sensor("lo_locked", 0).to_bool()
        and usrp.get_tx_sensor("lo_locked", 1).to_bool()
        ):
        pass
    return True

def rx_worker(current_freq, num_samps, rx_streamer, rx_buffer_list, rx_buffer_list_ch2, wait_time):
        
    recv_samps0 = []
    recv_samps1 = []

    num_channels = rx_streamer.get_num_channels()
    recv_buffer = np.empty((num_channels, num_samps), dtype=np.complex64)

    # Craft and send the Stream Command
    rx_md = lib.types.rx_metadata()
    stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.num_done)
    stream_cmd.num_samps = num_samps
    stream_cmd.stream_now = False
    stream_cmd.time_spec = wait_time

    rx_streamer.issue_stream_cmd(stream_cmd)

    rx_streamer.recv(recv_buffer, rx_md)
    recv_samps0.extend(recv_buffer[0].tolist())
    recv_samps1.extend(recv_buffer[1].tolist())

    paired_samples0 = [(sample, current_freq) for sample in recv_samps0]
    paired_samples1 = [(sample, current_freq) for sample in recv_samps1]
    
    rx_buffer_list.extend(paired_samples0)
    rx_buffer_list_ch2.extend(paired_samples1)
    

    return 

def tx_worker(tx_streamer, tx_data, tx_md, wait_time):

    #Synchronize time and send data
    tx_md.time_spec = wait_time
    tx_streamer.send(tx_data, tx_md)

    return


def generate_tx_data(samp_rate, chirp_len, chirp_bandwidth):

    #generate chirps
    fs = samp_rate
    N2 = chirp_len
    bw = chirp_bandwidth
    n= np.arange(0, N2-1)
    t = n/fs 

    #send_chirp = np.array(np.sin(np.pi*.5*(bw/t[-1])*(t**2)), dtype = np.complex64)
    chirp = np.array(np.exp(1j*np.pi*.5*(bw/t[-1])*(t**2)), dtype = np.complex64)

    N = 4096 #Padding number
    send_chirp = np.pad(chirp, (N), 'constant', constant_values=(0))

    #tile the data because two channels
    tx_data = np.tile(send_chirp, (1,1)) #tiles to send one period
    tx_data = np.tile(tx_data[0], (len(channels),1)) 

    #create metadata for tx
    tx_md = lib.types.tx_metadata()
    # tx_md.start_of_burst = True
    # tx_md.end_of_burst = True
    tx_md.has_time_spec = True

    chirp_len = send_chirp.size

    return tx_data, tx_md, send_chirp, chirp_len

def plot_scan(rx0, rx1, name):

    fig, ax = plt.subplots(figsize = (6,6))

    ax.plot(list(datum[0] for datum in rx0), label="ch0")
    ax.plot(list(datum[0] for datum in rx1), label="ch1") 

    ax.set_title('Received Signal')
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude')
    
    plt.legend()
    plt.savefig(f"{name}.png")
    plt.show()