:title: Power Measurment Device
:org: Davis Energy Group
:website: http://www.davisenergy.com/
:location: Davis, CA, USA
:skills: instrumentation, measurement, software, electronics

One service we do a lot of here is to consult on projects trying to determine
energy savings in buildings before and after energy saving measures have been
applied. Often this involves measuring power from many devices plugged into
electrical outlets (plug loads) throughout a building. There currently is no
inexpensive, wireless, an unobtrusive commercial product to do this. We are
interested in having a student group work to develop something we can use on
future projects. This would include:

- prototyping a lab scale power meter and ensuring it can accurately measure
  power for a variety of real world load shapes (function of current transducer
  and voltage transducer response times, acquisition speed, etc. - non trivial)
- design a small scale version to make this unobtrusive. The goal would be
  something approaching the size of a wall outlet and an inch thick.
  Alternatively, instead of concentrating on outlet-based packaging, a
  powerstrip-based device that could measure several plug loads would also be
  valuable.
- design a logging and communication system.

  - a micro controller would be required to do signal processing and
    integration to determine real power
  - put the data in an onboard buffer to avoid data losses during temporary
    communication outages
  - communicate the data to a base station (through a mesh network is a plus)

- test product for accuracy
- test product for electrical safety
