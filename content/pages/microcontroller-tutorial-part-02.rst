:title: Part 2: Implementing a PI Controller with an Arduino
:status: hidden

Introduction
============

This lesson will walk through using an Arduino to control ambient brightness
using a light-emitting diode (LED) for actuation and a photocell for sensing.


Learning Objectives
===================

Students will be able to

- identify a light emitting diode (LED), understand its function, and connect
  it into a circuit
- use pulse-width modulation (PWM) to mimic analog output for actuation
- identify a photocell, understand its function, and connect it into a
  circuit
- use a voltage divider to sense change in resistance of a photocell
- implement and tune a proportional-integral controller on a
  microcontroller
- write a program to integrate all of this information


Introduction to the Arduino IDE
===============================

Interactive demo of main IDE features:

-  Code editor
-  Verify sketch (blank)
-  Board selection
-  Port selection
-  Upload sketch (blank)
-  Serial monitor/plotter

For more in-depth descriptions of the IDE, see the `official guide
<https://www.arduino.cc/en/Guide/Environment>`_


The Circuit Components
======================

The circuit requires:

-  an LED
-  a photocell (photoresistor, light-dependent resistor)
-  4-8 jumper wires
-  a 4.7kΩ resistor (yellow, purple, red, [gold])
-  a 330Ω resistor (orange, orange, brown, [gold])

Once constructed, the circuit should look like the image below:

|complete-circuit|

The circuit consists of a light emitting diode (LED) circuit, driven by one of
the Arduino's digital I/O pins capable of producing a pulsewidth modulation
(PWM) signal. This will allow the LED’s brightness to change. A photocell
facing the LED senses the ambient lighting. The objective of the circuit is to
demonstrate an automatic feedback control system that drives the LED to
a desired brightness level near the sensor. You will be able to cast shadows on
the photocell and watch as the LED brightness increases to compensate for the
dimmed lighting.

Basic circuit modules
----------------------

Analog circuits are circuits dealing with signals free to vary from zero to
full power supply voltage. This stands in contrast to digital circuits, which
almost exclusively employ “all or nothing” signals: voltages restricted to
values of zero and full supply voltage, with no valid state in between those
extreme limits.

Light Emitting Diodes (LED)
---------------------------

Light emitting diodes (LEDs) are semiconductor devices that emit light
when voltage is applied across them. LEDs typically have a fixed voltage
drop of around 2V (depends on the LED), which is the voltage required to cause
it to illuminate. The brightness can then be controlled directly by varying the
current going through the device. In most applications (e.g. indicators),
a current-limiting resistor is connected in series with the LED to provide
a fixed brightness for a given control voltage.

|led|

|led-diagram|

In our application, we will use a fixed current-limiting resistor of 330Ω and
a 5V control voltage, but we will use a technique called pulsewidth modulation
(PWM) to effectively vary the current passing through the circuit.

PWM works by rapidly toggling a digital output between its high (e.g. 5V) and
low (e.g. 0V) values, with varying durations of on and off time. The ratio of
the on time to the total period of the PWM signal is referred to as duty cycle,
and is expressed as a percentage. The logic behind this is: if you were to
integrate the voltage over one period of the PWM signal, the effective voltage
would be the duty cycle times the "on" voltage level. If the switching is fast
enough, many sensors (including our own eyes) will not be able to detect that
the actuator (e.g. an LED) is actually turning on and off, but instead it will
detect an intermediate output roughly corresponding to the equivalent
voltage level. For mechanical systems, such as DC motors, the mechanical
dynamics are often slow enough with respect to the PWM signal that their output
will actually smoothly vary.

The Arduino Uno allows us to output a PWM signal on several of its pins. This
is done by setting the pin as an output, and using the `analogWrite
<https://www.arduino.cc/en/Reference/AnalogWrite>`_ function. This function
accepts any integer value between 0 (pin fully off, 0% duty cycle) and 255 (pin
fully on, 100% duty cycle).

|pwm|

Exercise 1: Vary the LED Brigtness
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Start by connecting the 5V and GND pins of the Arduino to the red and blue
   "power rails" of your breadboard, respectively.
2. LEDs are directional components, so ensure that the cathode is connected to
   ground (see diagram above). Connect the 330Ω resistor to the other lead, and
   connect the resistor to pin 5 of the Arduino using a jumper wire.
3. Check your circuit against the diagram below. Leave the circuit constructed
   throughout the session.

|led-circuit|

4. With this circuit hooked up, you can test its operation. Add to the code
   below to repeatedly ramp up the brightness of LED from off to fully on over
   a few seconds each time. You'll need the :code:`analogWrite` function as
   well as the :code:`delay` function.

.. code:: c++

   int LED_PIN = 5;

   void setup() {
       pinMode(LED_PIN, OUTPUT);
   }

   void loop() {
       // add code here
   }

Photocells
----------

Photocells are passive circuit elements which change their resistance in
response to a change in brightness. Their resistance *decreases* when the
ambient environment becomes *brighter*.

|photocell|

An Arduino can sense voltages from 0V to 5V through the analog input pins, but
it has no direct way of sensing resistance. Since our sensor operates by
changing resistance, we need to convert this to a change in voltage. This is
achieved through a voltage divider circuit.

|photocell-circuit|

In this circuit, we supply 5V from the Arduino as :math:`V_{\text{in}}` and
measure :math:`V_{\text{out}}` with one of the Arduino's analog input pins (pin
A0). The output voltage for this voltage divider is given by

.. math::

   V_{\text{out}} = \frac{R}{R + \ R_{s}}V_{\text{in}}

We know :math:`R`, :math:`V_{\text{in}}`, and we can measure
:math:`V_{\text{out}}`, so we can calculate the photocell resistance
:math:`R_{s}`. The `datasheet
<https://media.digikey.com/pdf/Data%20Sheets/Photonic%20Detetectors%20Inc%20PDFs/PDV-P7002.pdf>`_
for our photocell provides an approximate relationship between resistance and
the illuminance hitting the sensor:

|photocell-resistance|

In our example, however, we will simply convert the value read in by
`analogRead <https://www.arduino.cc/en/Reference/AnalogRead>`_ to a voltage.
The input comes in the form of a **10-bit unsigned integer**, so it has the
range of 0 to 1023 (:math:`2^{10} - 1 = 1023`), corresponding to 0V up to 5V,
respectively. If we read a value of :math:`x`, we can map this value to
a voltage as follows:

.. math::

   V = \frac{5}{1023}x


Exercise 2: Read from the Photocell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Leave the 5V and GND connections from the LED example intact, then place one
   of the photocell leads on the 5V rail. A photocell is essentially
   a resistor, so its orientation in the circuit doesn't matter.
2. Bend the photocell's leads to 90° so that it faces the LED.
3. Connect the other lead of the photocell to the 4.7kΩ resistor which goes to
   GND.
4. Use a jumper wire to connect the junction between the photocell and the
   4.7kΩ resistor to the Arduino's A0 pin.
5. Check your circuit against the diagram above.
6. Create a new sketch using the Arduino IDE and replace it with the following
   code. You will need to fill in some code beneath the commented lines in the
   :code:`setup` function. You will need to make use of the :code:`analogRead`
   function.

.. code:: c++

   int SENSOR_PIN = A0;

   // variable to store the input reading
   int reading = 0;

   // variable to store the voltage corresponding to the reading
   float voltage = 0;

   void setup() {
       Serial.begin(9600);
       pinMode(SENSOR_PIN, INPUT);
   }

   void loop() {
       // read in the input value (10-bit unsigned int)

       // convert the reading to a voltage

       // the following prints the reading and then waits a bit to loop again
       Serial.println(voltage);
       delay(100);
   }

7. Once the code is uploaded and running, use the Arduino IDE's **serial
   monitor** or **serial plotter** to view the values being read. *What happens
   to the voltage if you cast shadows over the circuit?*
8. Allow the voltage to settle to a steady value. Use the serial monitor to
   record the numerical value.


Control System
==============

Now we'll put the LED and photocell together in order to obtain a desired
brightness level. Here is a block diagram of the control system we will
implement to achieve this:

|controller|

In this controller example, we will use voltage as a representation of
brightness. Because of the voltage divider configuration, the voltage read by
the Arduino's input pin will vary proportionally to the brightness sensed by
the photocell.

The measured voltage is compared to a voltage representing the desired
brightness, resulting in some error. This error is then fed into a controller,
which transforms the error into a PWM signal to change the LED brightness. For
example, if the measured brightness is lower than desired, the error will be
positive, and the controller coefficients will produce a positive PWM signal to
drive the LED to become brighter. This has the effect of increasing the
measured voltage, hence decreasing the error. This kind of controller
configuration is called a regulator, and its job is to achieve and maintain
zero error between the measured output and the desired output.

Circuit Construction
--------------------

Below is a diagram of the complete circuit and the photo from before. Both
components (the LED and the photocell) should be connected from the previous
two sections. The most important part of the control circuit construction
(aside from making the correct electrical connections) is that the LED and
photocell are close to and facing one another. This will ensure that the LED is
able to influence the reading of the sensor as much as possible. The photo of
the completed circuit is repeated below:

|complete-circuit|

Implementing the Controller
---------------------------

Excercise 3: Finding a Setpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Start with the photocell reading code you finished.
2. Add to that sketch the code for setting up the LED (refer to the first code
   listing for help), then use the :code:`analogWrite` function inside
   :code:`setup` to turn the LED on at **30% duty cycle**.
3. Run the sketch and observe the voltage output by the photocell circuit.
   **Write this value down** as this will be the desired brightness level we
   will seek to achieve with an automatic control system.

Exercise 4: Implement a Proportional Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a new sketch based on the code below. You will need to replace the
   value of :code:`r` with the setpoint you found in the previous exercise, and
   you will have to implement the controller equations inside :code:`loop` to
   find :code:`y`, :code:`e`, and :code:`u`. For now, leave :math:`K_{p} = 0`.

.. code:: c++

   int SENSOR_PIN = A0;
   int LED_PIN = 5;

   // desired voltage (change this to the value you found)
   float r = 2;

   // proportional controller coefficient
   float Kp = 0;

   // reading from the photocell
   float y = 0;
   // error between the desired output and the reading
   float e = 0;
   // output to send to the LED
   float u = 0;

   void setup() {
       Serial.begin(9600);
       pinMode(SENSOR_PIN, INPUT);
       pinMode(LED_PIN, OUTPUT);
   }

   void loop() {
       // update the photocell reading (voltage)
       y =

       // compute the error between the reading and the desired value
       e =

       // compute the output value by multiplying the error by Kp
       u =

       // make sure the output value is bounded to 0 to 255
       // then write it to the LED pin
       u = bound(u, 0, 255);
       analogWrite(LED_PIN, u);

       // plot the measurement
       Serial.print(y);
       Serial.print('\t');
       // plot the desired output
       Serial.print(r);
       Serial.print('\t');
       // plot the error
       Serial.println(e);

       delay(50);
   }

   // Bound the input value between x_min and x_max.
   float bound(float x, float x_min, float x_max) {
       if (x < x_min) { x = x_min; }
       if (x > x_max) { x = x_max; }
       return x;
   }

2. Once the code is uploaded and running, open up the serial plotter. The
   series of :code:`Serial.print` statements plots the measurement signal
   :math:`y(t)`, the reference signal :math:`r(t)` (constant), and the error
   signal :math:`e(t)`. Perturb the brightness reading of the photocell by
   casting shadows on it and figure out which line is which.
3. Let the signals become steady, then use the error measurement to make an
   estimate of what :math:`K_{p}` should be to drive the error to zero. Recall
   that the reference value was found by producing a PWM signal at 30% duty
   cycle, so the term :math:`u(t) = K_{p}e(t)` should be approximately
   :math:`0.3 \times 255 = 76.5`. This initial guess will likely produce
   a proportional constant that is too high and causes instability. Divide it
   by 2 to start.
4. Now try casting shadows over the circuit. Looking at the LED itself, does it
   seem to compensate when less light from the ambient environment hits the
   photocell? What do you observe when looking at the error signal in the
   serial plotter?

Exercise 5: Adding Integral Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you probably have noticed, proportional controllers may suffer from non-zero
*steady state error*. That is, there is a consistent mismatch between the
desired and measured outputs, but the controller does not compensate for it
exactly. To fix this problem, we can implement an integral control component,
which adds to the controller output a multiple of the total integral of the
error over all time. If a small but steady error is present, the integral of
this error over time will become large, and the integral component of the
controller will increase the total controller output to drive the error down to
zero.

1. Starting with the code you wrote to implement the proportional controller,
   introduce a global variable :math:`K_{i}` and set it to an order of
   magnitude smaller than :math:`K_{p}`.
2. Introduce a variable to keep track of the total accumulation of error. Each
   time the error is calculated, add it to the current value of the error
   accumulator variable.
3. Modify the line that computes the PWM control value to use the full control
   equation:

.. math::

   u(t) = K_{p}e(t) + K_{i}\sum_{\tau=0}^{t}e(\tau)

4. Upload the sketch and open the serial plotter. *What happens if you cast
   shadows on the circuit now?*
5. Play around with :math:`K_p` and :math:`K_i`. What does increasing or
   decreasing these coefficients do? Compare your observations to some of the
   information on Wikipedia's extensive article on `PID control
   <https://en.wikipedia.org/wiki/PID_controller>`_


.. |complete-circuit| image:: {filename}/images/microcontroller-tutorial/complete-circuit.jpg
   :width: 5in
.. |pwm| image:: {filename}/images/microcontroller-tutorial/pwm.svg
   :width: 5in
.. |led| image:: {filename}/images/microcontroller-tutorial/led.jpg
   :width: 3in
.. |led-diagram| image:: {filename}/images/microcontroller-tutorial/led-diagram.svg
   :width: 3in
.. |led-circuit| image:: {filename}/images/microcontroller-tutorial/led-circuit.svg
   :width: 3in
.. |photocell| image:: {filename}/images/microcontroller-tutorial/photocell.jpg
   :width: 3in
.. |photocell-circuit| image:: {filename}/images/microcontroller-tutorial/photocell-circuit.svg
   :width: 3in
.. |photocell-resistance| image:: {filename}/images/microcontroller-tutorial/photocell-resistance.png
   :width: 4in
.. |controller| image:: {filename}/images/microcontroller-tutorial/controller.svg
   :width: 7in
