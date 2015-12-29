:title: Instrumented Bicycle For Crash Reconstruction
:org: InSciTech
:website: http://www.inscitech.com/
:location: Mountain View, CA, USA
:skills: instrumentation, measurement, software, dynamics
:status: hidden
:template: project-page

Need
====

Bicycling, while a common activity, is not particularly well understood.
“Simple” actions such as balancing and steady turning have been the subject of
recent research efforts (e.g., Moore et al., 2011; Kooijman et al., 2011;
Peterson and Hubbard, 2009; Meijaard et al., 2007) In terms of accident
reconstruction it would be useful to have better estimates of  meaningful
motion envelop of riding behavior as well as the ability to measure aspects of
an individual rider and/or bicycle. An instrumented bicycle would enable us to
conduct accurate and repeatable studies such as:

- Acceleration/braking performance
- Comfortable and maximum speeds of an individual rider
- Effects of road perturbations on steer inputs and other bicycle dynamics
- Compare/test accuracy of popular fitness devices (e.g., Garmin bike computers
  or popular fitness apps such as Strava, Run Keeper, or Endomondo)

To address this need, we propose a modular sensor and data acquisition system
that will facilitate data collection.

Desired Outcomes
================

We wish to be able to measure and log the following parameters:

1. Steer angle
2. Lean angle
3. Pitch angle
4. Speed (via wheel speed sensor)
5. Speed and position (via GPS)
6. Front and rear brake status (on/off), should also activate a high-intensity
   LED clearly visible to a video camera located ~30 feet to the side of the
   bike in daylight conditions (1 LED, or if necessary, 1 set of LEDs, for each
   brake)
7. Estimate the forces experienced by a rider due to road perturbations
8. Crank pedal cadence

Additional Measurement Requirements:

- Ideally the measurement and data logging system would be (relatively) easy to
  swap to different bicycles.
- An ideal measurement system would not influence the system it is trying to
  measure! In practice, this is never truly possible, but a useful system would
  not be particularly bulky, heavy, or otherwise encumber a rider.
- All the measurements should be collected by a single “computer”
  (microcontroller, embedded machine, DAQ box, etc.) and have a common time
  base
- Think about the position/alignment of the sensors. Ideally they would be
  placed so that swapping the system to a new bicycle would make comparison of
  results more straight forward without lots of calibration.

Software Requirements:

- If it is not practical to directly measure, the angular speeds for steer,
  lean, and pitch should be calculated in software.
- The system would make it easy to visually display the collected data.
- Whenever possible, we would prefer to use free and open source tools, e.g.,
  Python, Octave, etc.

References
==========

- Moore, J., Kooijman, J., Schwab, A., and Hubbard, M. (2011). Rider motion
  identification during normal bicycling by means of principal component
  analysis. Multibody System Dynamics, 25:225–244.
- J. D. G. Kooijman, J. P. Meijaard, Jim M. Papadopoulos, Andy Ruina, and A. L.
  Schwab. (2011). "A bicycle can be self-stable without gyroscopic or caster
  effects", Science 332(6027):339-342.
- Peterson, D. L. and Hubbard, M. (2009). General steady turning of a benchmark
  bicycle model. In Proceedings of IDETC/MSNDC 2009 the ASME 2009 International
  Design Engineering Technical Conferences & 7th International Conference on
  Multibody Systems, Nonlinear Dynamics, and Control, number
  DETC2009/MSNDC-86145.
- J.P. Meijaard, J.M. Papadopoulos, A. Ruina, and A.L. Schwab. (2007).
  Linearized dynamics equations for the balance and steer of a bicycle: a
  benchmark and review - including appendix. Proc. Roy. Soc. A.,
  463(2084):1955-1982.
