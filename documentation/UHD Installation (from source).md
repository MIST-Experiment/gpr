This is a homemade guide for installing UHD on your device to communicate with the B210 board. This guide was adapted from the official [Ettus Knowledge base](https://kb.ettus.com/Building_and_Installing_the_USRP_Open-Source_Toolchain_(UHD_and_GNU_Radio)_on_Linux) with specific commands used to get it running properly. 

## Installing dependencies

First run `sudo apt update`

Then install the following dependencies:

`sudo apt-get -y install autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool fort77 g++ gir1.2-gtk-3.0 git gobject-introspection gpsd gpsd-clients inetutils-tools libasound2-dev libboost-all-dev libcomedi-dev libcppunit-dev libfftw3-bin libfftw3-dev libfftw3-doc libfontconfig1-dev libgmp-dev libgps-dev libgsl-dev liblog4cpp5-dev libncurses5 libncurses5-dev libpulse-dev libqt5opengl5-dev libqwt-qt5-dev libsdl1.2-dev libtool libudev-dev libusb-1.0-0 libusb-1.0-0-dev libusb-dev libxi-dev libxrender-dev libzmq3-dev libzmq5 ncurses-bin python3-cheetah python3-click python3-click-plugins python3-click-threading python3-dev python3-docutils python3-gi python3-gi-cairo python3-gps python3-lxml python3-mako python3-numpy python3-opengl python3-pyqt5 python3-requests python3-scipy python3-setuptools python3-six python3-sphinx python3-yaml python3-zmq python3-ruamel.yaml swig wget

`pip install pygccxml`
`pip install pyqtgraph`

## Building and installing UHD from source code

1. make a folder to hold the repository.
	`cd $HOME
	`mkdir workarea
	`cd workarea
2. Next, clone the repository and change into the cloned directory.
	`git clone https://github.com/EttusResearch/uhd
	`cd uhd
3. heckout the desired UHD version. You can get a full listing of tagged releases by running the command:
	`git tag -l`
	Example truncated output of git tag -l:
	`git tag -l
	``...
	`release_003_009_004
	`release_003_009_005
	`release_003_010_000_000
	`...`

	**Note:** As of UHD Version 3.10.0.0, the versioning scheme has changed to be a quadruplet format. Each element and version will follow the format of: Major.API.ABI.Patch. Additional details on this versioning change can be found here.
	After identifying the version and corresponding release tag you need, check it out:

4.  Checkout the most recent stable version
	`git checkout v4.4.0.0-rc1
5. Next, create a build folder within the repository.
	`cd host
	`mkdir build
	`cd build
6. Invoke CMake.
	`cmake ..
	**Note:** if the shell PATH is set such that /bin comes before /usr/bin, then this step is likely to fail because cmake will set the FIND_ROOT_PATH to / and this setting will fail as a prefix for Boost headers or libraries. The cmake output will include messages such as:
	`--   Boost include directories: /include
	`--   Boost library directories: /lib/x86_64-linux-gnu
	and
	 `CMake Error in lib/CMakeLists.txt:
	 `Imported target "Boost::chrono" includes non-existent path "/include"`
	 `in its INTERFACE_INCLUDE_DIRECTORIES.  Possible reasons include:
	 `* The path was deleted, renamed, or moved to another location.
	 `* An install or uninstall procedure did not complete successfully.
	 `* The installation package was faulty and references files it does not provide.~
	
	One of the following 3 options should fix this situation:
	1. `/usr/bin/cmake ..
	2. `PATH=/usr/bin:$PATH cmake ..
	3.  `cmake -DCMAKE_FIND_ROOT_PATH=/usr ..` **<- THIS ONE WORKED**
	**Note:** If you wish to also install the USRP Python API (which you will need to), add the following [argument](https://www.controlpaths.com/2022/12/19/using-the-python-api-for-usrp-sdr-devices/) to cmake:
	`-DENABLE_PYTHON_API=ON
7. Once the cmake command succeeds without errors, build UHD.
	`make
8. You can optionally run some basic tests to verify that the build process completed properly.
	`make test
9. Install UHD, using the default install prefix, which will install UHD under the /usr/local/lib folder. You need to run this as root due to the permissions on that folder.
	`sudo make install
10.  Next, update the system's shared library cache.
	`sudo ldconfig
11. inally, make sure that the LD_LIBRARY_PATH environment variable is defined and includes the folder under which UHD was installed. Most commonly, you can add the line below to the end of your `$HOME/.bashrc file`:
	`export LD_LIBRARY_PATH=/usr/local/lib

## Downloading the UHD FPGA Images

You can now download the UHD FPGA Images for this installation. This can be done by running the followingg command:

`sudo uhd_images_downloader

**Note:** Since this installation is being installed to a system level directory (e.g. /usr/local), the uhd_images_downloader command requires sudo privileges.
Example ouput for UHD 3.13.3.0:

`sudo uhd_images_downloader 
`Images destination:      /usr/local/share/uhd/images
`Downloading images from: http://files.ettus.com/binaries/images/uhd-images_003.010.003.000-release.zip
`Downloading images to:   /tmp/tmpm46JDg/uhd-images_003.010.003.000-release.zip
`57009 kB / 57009 kB (100%)
`Images successfully installed to: /usr/local/share/uhd/images

## Configuring USB

Finally, run the following commands to allows UHD to access the device

`cd $HOME/workarea/uhd/host/utils
`sudo cp uhd-usrp.rules /etc/udev/rules.d/
`sudo udevadm control --reload-rules
`sudo udevadm trigger

