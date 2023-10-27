# pylinkam

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6758012.svg)](https://doi.org/10.5281/zenodo.6758012) ![license](https://img.shields.io/github/license/swinburne-sensing/pylinkam) ![python version](https://img.shields.io/pypi/pyversions/pylinkam) ![issues](https://img.shields.io/github/issues/swinburne-sensing/pylinkam)

---

This Python module provides Python bindings for the official C/C++ Linkam SDK. It enables monitoring and control of various instruments provided by Linkam Scientific. The library can optionally be used with the [pint](https://pint.readthedocs.io/en/stable/) package to handle unit conversion.

### Background
We use a Linkam HFS600E-PB4 stage with T96 controller for gas sensing experiments in the [Swinburne](https://swin.edu.au) Sensor Technology Lab. This library has been parted out from our custom developed experiment software for general use. If you find the package useful we'd love to hear about your projects!

## Installation
Note that the Linkam SDK binary files (`LinkamSDK.dll` or `libLinkamSDK.so`) and the required license file (typically `Linkam.lsk`) are **not** distributed as part of this module.

By default, the module will look for the Linkam SDK binary using the `$PATH` environment variable via the `ctypes` module and will automatically append the module directory before searching.

1. Place `LinkamSDK.dll` (debug or release) and `Linkam.lsk` files inside the `pylinkam` module folder (the one that contains `__init__.py`). Alternately, at runtime you can specify a binary name (remove the `.dll` extension on Windows) and path to access these files.
2. Run `demo.py` to check for any connection/path issues. This will set the stage temperature to 25°C temporarily.

## Usage
Initialise the SDK by creating an instance of `pylinkam.sdk.SDKWrapper` providing optional paths for SDK binary files and the license file. Once initialised, use the `connect()` method to create a context manager for the connection to a device.  

### Example
```python
from pylinkam import interface, sdk


with sdk.SDKWrapper() as wrapper:
    with wrapper.connect() as connection:
        print(f"Name: {connection.get_controller_name()}")

        temperature = connection.get_value(interface.StageValueType.HEATER1_TEMP)
        connection.set_value(interface.StageValueType.HEATER_SETPOINT, 30)
```

## Tested Devices
This library has been developed for the following Linkam instruments/addons, a check indicates that functionality has been verified on working hardware:

- [x] T96 System Controller (via USB)
- [ ] T96 System Controller (via RS-232, might work :shrug:)
- [x] HFS600E-PB4 Probe Stage (all stages should be supported)
- [x] RH95 Humidity Controller
- [ ] LNP96 Cooling Option (should work)

Note that connecting multiple devices to a single host is untested, though the connect functions per the Linkam API *can* accept a serial number.

## Tested API Versions and Platforms

- [x] `v3.0.5.5` on Windows 10
- [x] `v3.0.15.35` on Windows 10

In theory the SDK binary files for Linux should have identical mappings, but this hasn't been tested. Versions `< 1.2.3` used `WinDLL` to load the Linkam SDK binary, however more recent versions will automatically detect the platform and use `CDLL` when not on Windows. We don't have hardware connected to a Linux machine to test, so please report any issues.

## Acknowledgments

Developed at [Swinburne University of Technology](https://swin.edu.au). If used in an academic or research project, please consider citing this work as it helps attract funding and track research outputs:

```
C. J. Harrison and M. Shafiei. pylinkam. (2022). [Online]. doi: https://doi.org/10.5281/zenodo.6758012
```

*This activity received funding from [ARENA](https://arena.gov.au) as part of ARENA’s Research and Development Program – Renewable Hydrogen for Export (Contract No. 2018/RND012). The views expressed herein are not necessarily the views of the Australian Government, and the Australian Government does not accept responsibility for any information or advice contained herein.*

## Disclaimer
This library is not an official product or service of Linkam Scientific Instruments Ltd. This library is not endorsed, sponsored, or supported by Linkam Scientific Instruments Ltd. The name Linkam as well as related names, marks, emblems, and images are registered trademarks of their respective owners.
