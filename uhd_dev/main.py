from tqdm import tqdm   
import threading
import numpy as np
import uhd
from uhd import libpyuhd as lib
import matplotlib.pyplot as plt

from params import *
from scan import *

state_manager = StateManager() 

rx_buff0 = []
rx_buff1 = []

current_freq = start_freq
num_steps = (end_freq - start_freq) // step_freq

usrp, rx_streamer, tx_streamer = usrp_connect()
tx_data, tx_md, send_chirp, chirp_len = generate_tx_data(samp_rate, chirp_len, chirp_bw)

step_idx = 0

with tqdm(total=num_steps, desc="Scanning...") as pbar:

    while True:
        if (state_manager.get_state() == States.tune):

            if tune_center_freq(usrp, current_freq, channels, 50,30,10,10):
                state_manager.set_state(States.scan)
            
            current_freq += step_freq
            step_idx += 1
            
            if step_idx > num_steps:
                state_manager.set_state(States.done)
                
        elif (state_manager.get_state() == States.scan):

            usrp.clear_command_time()

            wait_time = usrp.get_time_now() + lib.types.time_spec(delay)
            
            rx_thread = threading.Thread(target=rx_worker, args=(start_freq, chirp_len, rx_streamer,
                                                                rx_buff0, rx_buff1, wait_time))
            
            tx_thread = threading.Thread(target=tx_worker, args=(tx_streamer, tx_data, tx_md, wait_time))
    
            rx_thread.start()
            tx_thread.start()

            rx_thread.join()
            tx_thread.join()

            state_manager.set_state(States.tune)

            usrp.clear_command_time()

            pbar.update(1)

        elif(state_manager.get_state() == States.done):

            break

print("Scan completed.")

if save_data:
    print("Saving data...")
    np.save(f"{savedir}/ch0_{test_ID}", rx_buff0)
    np.save(f"{savedir}/ch1_{test_ID}", rx_buff1)
    print("Data saved.")

if gen_plots:
    print("Generating plots...")
    plot_scan(rx_buff0, rx_buff1, f"{savedir}plot_{test_ID}")
    print("Plots saved.")

print("Quitting.")

            

