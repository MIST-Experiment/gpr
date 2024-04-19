channels = [0,1]

chirp_len = 80000
chirp_bw = 5e6
start_freq = 400e6
end_freq = 600e6
step_freq = 10e6
samp_rate = 10e6
delay = 0.1

savedir = "gpr/data/test"
test_ID = "6-1"
save_data = True
gen_plots = True

_all__ = [
    "channels",
    "chirp_len",     
    "chirp_bw", 
    "usrp_connect",  
    "start_freq",
    "end_freq",
    "step_freq",
    "samp_rate",
    "delay",
    "savedir",
    "test_ID",
    "save_data",
    "gen_plots"
]
