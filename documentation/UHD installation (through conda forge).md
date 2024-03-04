This outlines the steps requires to install the UHD python API through conda forge in a specified miniconda environment. This greatly simplifies the task of installing UHD compared to building from source, and allows for a quick and easy way to create and test new environments. This guide will contain specifics to creating the working environment on a Raspberry Pi.

1. Install miniconda
	```
	mkdir -p ~/miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
	rm -rf ~/miniconda3/miniconda.sh
	```
2. Initialise newly-installed miniconda
	```
	~/miniconda3/bin/conda init bash
	~/miniconda3/bin/conda init zsh
	```
1. Restart shell 
	 `source ~/.bashrc`
4. Create a new environment
	`conda create --name uhd_env python=3.12.1`
5. Activate the environment
	`conda activate uhd_env`
6. Install jupyter lab (while we're here)
	` pip install jupyter lab`
7. Install chardet (needed for jl)
	`pip install chardet`
8. Install UHD
	`conda install conda-forge::uhd`
9. Download UHD FPGA images
	`uhd_images_downloader`
10. Configure USB
	```
	cd $HOME/gprpi/miniconda3/envs/uhd_env/uhd/utils
	sudo cp uhd-usrp.rules /etc/udev/rules.d/
	sudo udevadm control --reload-rules
	sudo udevadm trigger
	```

## Sources and helpful links:
[miniconda docs](https://docs.conda.io/projects/miniconda/en/latest/)
[miniconda on RPi4 (specifies architecture)](https://forums.raspberrypi.com/viewtopic.php?t=316338)
[anaconda uhd package](https://anaconda.org/conda-forge/uhd)
[radioconda, an SDR software package bundle](https://github.com/ryanvolz/radioconda)
[installing UHD from source on RPi](https://www.radiosrs.net/installing_uhd_gnuradio.html)



