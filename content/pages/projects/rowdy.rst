:title: Rowing Mechanics Modeling
:org: Hegemony Technologies
:org_url: http://therowingapp.com
:skills: dynamics, software
:location: Davis, CA, USA
:id: rowdy
:status: hidden
:template: project-page

The Need
========

The goal of this project is to formulate, build, test, and tune analysis
methods and a model that can be used to improve estimates of boat location and
motion using location and motion recordings made on rowers, boat, and/or oars.
The improved location and motion measures should be represented as components
in any coordinate system of choice: boat, rower, and/or seat. The people
working on this project will be given a database of rowing data that has been
collected experimentally. A rowing expert will work with the team to help them
understand the data and the use of the methods and model that the expert is
asking the team to develop.

Background
==========

The sport of rowing involves a significant number of mechanical and
physiological factors that interact in a complex way. Individual rowing
performance is affected by the biomechanics (how well you handle the oars, how
well you handle the sliding seat, how well you position yourself to transfer
power between the oar and the boat, etc.) and your physiologic ability to
systematically transfer energy to the oar.

An instrumentation system (GPS + 9 degree of freedom IMU) was mounted on boats,
rowers, and oars and has been used to collect a large volume of location,
motion, and orientation data.  This project is formed in response to the
hypothesis that these data can be processed, analyzed, translated, and improved
into actionable insights that a rower can use to improve their rowing
efficiency and performance.

Design Requirements
===================

1. Investigate and standardize a coordinate system nomenclature and methodology
   that allows for a clear and unambiguous representation of kinematic data in
   any of the reference coordinate systems of interest: oar, boat, and/or seat.
2. Build a robust numerical processing methodology for the transformation and
   representation of measured location and kinematic data into any reference
   coordinate systems of interest: oar, boat, and/or seat.
3. Investigate and built a robust numerical processing methodology for
   translating data into more useful and valuable forms (aka, “data munging”).
   Practically, this involves the development of techniques for filtering,
   selecting, and/or sorting data to eliminate noisy or useless data.
4. Investigate, build, test, tune, and validate a sensor fusion methodology
   that transforms raw measures of accelerometer, angular rate gyro, and
   magnetometer data into object orientation data (in any of the aforementioned
   coordinate systems of interest). The orientation results should include
   estimates of component error and an error correction implementation trigger
   (aka, “drift correction”) that can be parametrically controlled, e.g., at
   the end (and NOT in the middle) of a stroke.
5. Investigate, build, test, tune, and validate a model that combines GPS and
   IMU data to improve the accuracy and precision of location and motion data.
   Effectively, this involves building a Kalman filter. The Kalman filter
   should be as generic as possible but sensitivity analysis of results must be
   conducted to justify the introduction of configuration specific information
   and data into the model. The model should be self-tuning as much as
   possible. Estimates of accuracy and precision improvements on location and
   motion should be included with calculations.
6. Investigate, build, test, tune, and validate techniques for transformation
   of the time-domain data into stroke domain data. Effectively, this involves
   hypothesizing and testing signatures of data that correlate to defined points
   in the rowing stroke, i.e., the “catch” and “finish” of the stroke as
   defined by the local minimum and maximum angular displacements of the oar in
   the horizontal plane.

Note that this project has a sister project in the EECS Capstone class that is
focused on building a rowing analysis workstation to facilitate the plotting,
statistical analysis, and reporting on rowing data. Both projects will be given
similar data sets that the teams will use to test their work, but by design
neither project necessarily depends on the work product on the other team to
complete their work. Having said that, the customer encourages both project
teams to realize that more value will be realized if the projects can be
harmonized, i.e., all of the rowing analysis workstation functionality can be
combined with the rowing mechanics modeling functionality.

Deliverables
============

1. A report with illustrations and a set of definitions and nomenclature that
   clearly and unambiguously allows for an understanding of the referenced
   coordinate systems of interest.
2. A software package that allows for translation of data into any coordinate
   system of interest, the referenced data munging, and Kalman filter creation.
3. An installation package that allows a state-of-the-art PC and Mac system to
   be turned into a rowing mechanics modeling tool.
4. Upon launch of the workstation, the system should allow for the
   identification and linkage to a database and its associated schema.

Critical Issues
===============

1. While the rowing experts using this information and methods will be
   scientists and tech- savvy, the system must be robust, intuitive, and
   easy-to-use.
2. The installation of the workstation package on state-of-the-art PC and Mac
   systems systems must straightforward and robust.
3. The system should gracefully fail when errors are encountered and generate
   feedback to the user (and developer) that allows for efficient
   troubleshooting.
4. Python should be used to the maximum extent possible. Open-source packages
   and development environments are preferred.
5. The database is MySQL.
6. The code must be well-commented and developers should recognize their
   ability to make an impact with this work will depend on the ability of other
   developers to pick up, understand and build on this codebase.

.. figure:: {filename}/images/rowdy-01.jpg
   :width: 400px

   Figures of interest from the project.
