# pylinkam

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6758012.svg)](https://doi.org/10.5281/zenodo.6758012)

---

This Python module provides Python bindings for the official C/C++ Linkam SDK. It enables monitoring and control of various instruments provided by Linkam. Can optionally be used with the [pint](https://pint.readthedocs.io/en/stable/) package to handle unit conversion.

Note that the Linkam SDK binary files (`LinkamSDK_release.dll` or `LinkamSDK_debug.dll`) and the required license file (typically `Linkam.lsk`) are **not** distributed as part of this module.

## Usage
Initialise the SDK by creating an instance of `pylinkam.sdk.SDKWrapper` providing optional paths for SDK binary files and the license file. Once initialised calling `connect_usb()` on the wrapper  

## Tested Devices
This library has been developed for the following Linkam instruments/addons, a check indicated that functionality has been verified on working hardware:

- [x] T96 System Controller (via USB)
- [ ] T96 System Controller (via RS-232, this might work :shrug:)
- [x] HFS600E-PB4 Probe Stage
- [x] RH95 Humidity Controller
- [ ] LNP96 Cooling Option (should work)

Only tested under Windows 10 using LinkamSDK v3.0.15. In theory the SDK binary files for Linux should have identical mappings, but this hasn't been tested. 

## Acknowledgments

Developed at [Swinburne University of Technology](https://swin.edu.au). If used in an academic project, please consider citing this work as it helps attract funding and track research outputs:

```
C. J. Harrison and M. Shafiei. pylinkam. (2022). [Online]. doi: https://doi.org/10.5281/zenodo.6758012
```

*This activity received funding from [ARENA](https://arena.gov.au) as part of ARENA’s Research and Development Program – Renewable Hydrogen for Export (Contract No. 2018/RND012). The views expressed herein are not necessarily the views of the Australian Government, and the Australian Government does not accept responsibility for any information or advice contained herein.*

*The work has been supported by the [Future Energy Exports CRC](https://www.fenex.org.au) whose activities are funded by the Australian Government's Cooperative Research Centre Program.*
