:title: Part 1: Intro to Microcontrollers With Emulation
:status: hidden

Introduction
============

This lesson will introduce you to programming the Arduino microcontroller board
using an electronics emulator.

Objectives
==========

- To understand what a microcontroller is and what it may be used for.
- To introduce the basics of programming an Arduino microcontroller.
- To understand what is and how to use an emulator.

Microcontrollers
================

Microcontrollers are very simple computers that have a central processing unit
(CPU), memory, and various electrical inputs and outputs. They allow us to
enhance electrical circuits with logic and algorithms. They are particularly
useful to engineers due to the ability to implement control systems for driving
electrically controlled actuators. They allow you write programs that can
execute in real time. The are typically used as "embedded systems", i.e.  for
lightweight very specific use hardware enhancements.

Examples:

- PIC_ family of chipsets.
- AVR_ family of chipsets.

.. _PIC: https://en.wikipedia.org/wiki/PIC_microcontroller
.. _AVR: https://en.wikipedia.org/wiki/Atmel_AVR

It is important to note the difference between computers and microcontrollers.
Computers may have multiple CPUs with many more inputs and outputs. They also
have more and varied memory. Computers can typically display to rich displays
and handle many standardized peripherals. Finally, a computer typically runs an
operating system that manages many processes at once and interfaces with
complex hardware. Operating systems typically do not execute their commands in
real time, but are queued.

Examples:

- Laptop
- Smart phone
- `Raspberry Pi <https://en.wikipedia.org/wiki/Raspberry_Pi>`_
- Supercomputer

Emulation
=========

In general, the code you write on your computer for the microcontroller must be
compiled, i.e.  transformed into the language of the Arduino's CPU, and then
uploaded onto the Arudino's memory. To try out code on the Arduino you must
have the actual hardware. But during this lesson we will make use of an Arduino
emulator which allows us to try out code we want to run on an Arduino without
having the actual hardware. There are a number of Arduino emulators available,
but we will make use of a web application called 123d.circuits.io_.

1. Visit 123d.circuits.io and create an account.
2. Log in to your account.
3. Select the "Create" tab.
4. Open "Electronics Lab Hub"
5. Open a new "Electronics Lab"

Components
   Open a library of components that can be dropped onto the workspace.
Breadboard
   The breadboard is a simple has a grid of input pins. The rows along the top
   and bottom are connected and generally used to supply a common voltage and
   ground. The columns in the middle rows are tied together.

Search for Arduino Uno and drag it onto the screen.

The Arduino board has the CPU chip which is connected to the black pins along
the edges. There is a USB plug to connect to your computer for communication
purposes.

Ground
   The common ground for the circuit (the negative polarity side of the
   circuit).
5V
   A 5V power supply which can provide up to X amps of current.
Digital I/O
   Pins that can read binary inputs and write binary outputs.
Analog Inputs
   Pins that can read continuous inputs and convert them to a digital signal.

Code editor
   Here you can edit the code that will be loaded onto any component that
   excepts code, e.g. the Arduino UNO.
Serial monitor
   This will display the outputs of the USB connection on the Arduino board.
Start Simulation
   This will run the simulation of the circuit.

.. _123d.circuits.io: http://123d.circuits.io

Processing Language
===================

The Arduino can be programmed by writing code in the `Processing language`_,
which is derivative of the C programming language. C is a low level language
that compiles directly to machine code for different CPU architectures and is
one of the most widely used programming languages. Most work with
microcontrollers is done in C.

.. _Processing language: https://en.wikipedia.org/wiki/Processing_%28programming_language%29

Variables
=========

Objectives:

- Explain how to declare and assign variables.
- Introduce the integer and double precision variables.
- Explain how to convert (cast) one type to another.

If you want to use a variable you have to specify the type of the variable when
you declare it. In the following case, a variable that holds the number for the
pin that is connected to the onboard LED is declared:

.. code-block:: arduino

   int led = 13;

Here the ``int`` specifies this value to be a signed integer, i.e. any positive
or negative whole number. ``led`` is the name of the variable and ``13`` is the
value assigned to it. Finally, a ``;`` is required to close the statement.

There are a number of other variable types: ``double``, ``float``, ``bool``,
``char``, etc. For decimal values we will make use of a double precision
variable in this lesson. For example:

.. code-block:: arduino

   double measurement = 0.0;

Lastly, you may need to cast variables of one type to another type. For example
you can convert an integer to a double with:

.. code-block:: arduino

   int int_val = 1;
   double double_val = (double) int_val;

Exercise
--------

What will the value of the variable ``result``` be in the following code?

.. code-block:: arduino

   int a = 10;
   int b = 5;
   double c = 2.4;

   int result = (int) c * b + a;

a. 22.00
b. 20
c. 25
d. 20.00

Functions: setup(), loop(), and custom
======================================

Objectives:

- Understand what a function is, how to write one, and how to use one.
- Learn what the required ``setup()`` and ``loop()`` functions are.

For the first program let's send values from the Arduino to the connected
computer using the Universal Serial Bus (USB). Before we can do this we need to
discuss the two main functions that are in every Arduino program. The first
function is the `setup()` function and you specify it like so:

.. code-block:: arduino

   void setup() {

   };

The first word is ``void`` and this specifies what type of variable the
``setup()`` function will return. In this case, the type ``void`` means that
the setup function will not return anything, which is convention for this
function. Also convention, is the function name ``setup``, which tells the
Arduino that whatever is in this function must be run once before the Arduino
starts the main computation loop. This is typically used for setting the
initial states of pins or initializing various attached devices. The ``()``
parentheses typically hold the arguments to the function but as convention
``setup`` has no arguments. Finally the braces ``{}`` bound the code that will
execute in that function.

The second function that must be in every Arduino program is called ``loop``.
This function executes once every clock cycle (at 16 MHz) or as fast as it can
and contains the main code for your application. The function follows the style
of ``setup`` and looks like:

.. code-block:: arduino

   void loop() {

   };

You can also create your own custom functions. These functions typically take a
number of arguments (inputs) and return a single output. The following function
computes the average of three values:

.. code-block:: arduino

   double average(double first_val, double second_val, double third_val) {

     double result = (first_val + second_val + third_val) / 3;

     return result;
  };

Note that the type of the arguments must be declared in the call signature. The
function can be used as such:

.. code-block:: arduino

   double a = 1;
   double b = 2;
   double c = 3;

   average(a, b, c);

which will result in the value ``2.0``.

Note that variables declared inside functions will not be available to other
functions.

Exercise
--------

What will the result of the following code be if the values returned by the
``square()`` function were displayed to the screen?

.. code-block:: arduino

   int counter = 1;

   int square(int a) {
     return a * a;
   };

   void setup() {
     int a = 5;
     square(a);
   };

   void loop() {
     square(counter);
     counter = counter + 1;
   };

Exercise
--------

What is wrong with the following code?

.. code-block:: arduino

   void setup() {
     int a = 5;
   };

   void loop() {
     int result = a + a;
   };

Since ``a`` is declared inside the ``setup()`` function it will not be
available in the ``loop()`` function due to the scoping rules of the Processing
language. You can make ``a`` available to the ``setup()`` and ``loop()``
functions by declaring it globally, i.e. outside and above each function.

Serial Communications
=====================

Objectives:

- To understand the serial communications available on an Arduino.
- To learn to print the results of a calculation to the serial port.

The Arduino is capable of communicating using serial communications and we can
send simple ASCII text to and from the Arduino. There are many builtin
functions that are predefined that can be used in an Arduino program. To
initialize a serial communication with the Arduino at a communication baud rate
of 9600 symbols per second you can call:

.. code-block:: arduino

   Serial.begin(9600);

This function is typically called in ``setup()``.

You can print ASCII values to the serial communication port with the
``print()`` and ``println()`` functions, where the difference is that the
former doesn't print a newline character (``\n``), and the latter appends the
newline character automatically. The following code will print the integer
values to the serial port:

.. code-block:: arduino

   int a = 15;
   Serial.print(a)
   Serial.println(a)
   Serial.println(a)

The result would be::

   1515
   15

Let's modify the above exercise code so that we can see if our guess about the
result of the code is correct. You will need to open the serial monitor while
this code simulates to see the results.

Exercise
--------

Add some print statements to your code so that you can see the results of the
``square()`` function calls on the serial monitor.

Solution:

.. code-block:: arduino

   int counter = 1;

   int square(int a) {
     return a * a;
   }

   void setup() {
     Serial.begin(9600);
     int a = 5;
     Serial.println(square(a));
   };

   void loop() {
     Serial.println(square(counter));
     counter = counter + 1;
   }

Digital I/O
===========

The digital I/O pins on the board can be set to either input or output mode and
can be activated or deactivated as you see fit for your particular application.

Typically in ``setup()`` you will set the mode of the particular pin to input
or output, for example:

.. code-block:: arduino

   int led_pin_num = 13;

   void setup() {
     pinMode(led_pin_num, OUTPUT);
   };

In the above code, the builtin function ``pinMode()`` is used to set mode of
pin number 13 to ``OUTPUT`` which is a builtin predefined variable [1]_.

It turns out that pin #13 on the Arduino is wired in parallel to a small LED on
the board. So we can make this LED blink by utilizing the builtin
``digitalWrite()`` function. In addition, the builtin ``delay()`` function can
be used to control the duration of the cycle.

.. code-block:: arduino

   void loop() {
     digitalWrite(led_pin_num, HIGH);
     delay(100);
     dgitalWrite(led_pin_num, LOW);
     delay(100);
   };

``HIGH`` and ``LOW`` are builtin global variables that cause the pins to create
maximum and minimum voltage, respectively.

.. [1] All caps are convention for global variables.

Exercise
--------

Plug in an LED to the breadboard and connect its anode (+, long side) to a 150
ohm resistor [#]_.  Then connect the other end of the resistor to the number 13 pin.
Finally, connect the LED's cathode (-, short side) to the ground pin and
confirm that the LED component blinks the same as the on board LED.

`Solution <https://123d.circuits.io/circuits/1573816-simple-led>`__

.. [#] The resistor ensures that the LED doesn't draw more current than the
   Arduino board and the LED can handle.

Conditionals
============

Processing supports flow control with ``if`` statements. For example, if you'd
like to activate the on-board LED every 100 milliseconds except on every 5th
cycle wait for 1000 milliseconds. You could use:

.. code-block:: arduino

   int count = 0;

   void setup() {
     pinMode(led_pin_num, OUTPUT);
   }

   void loop() {
     if (count % 5 == 0) {
         digitalWrite(led_pin_num, HIGH);
         delay(1000);
         digitalWrite(led_pin_num, LOW);
         delay(1000);
     } else {
         digitalWrite(led_pin_num, HIGH);
         delay(100);
         digitalWrite(led_pin_num, LOW);
         delay(100);
     };
     count = count + 1;
   }

The ``%`` operator computes the modulus (remainder after division).

Exercise
--------

What does the following code do?

.. code-block:: arduino

   if (digitalRead(13) == HIGH) {
     digitalWrite(12, HIGH);
   else {
     digitalWrite(12, LOW);
   }

Loops
=====

There are two types of loops available for use ``for`` and ``while`` loops. To
do something a specific number of times you can use a for loop. For example,
this loop will execute ten times, i.e. i = 0, 1, 2, ..., 9.

.. code-block:: arduino

   for (int i = 0, i < 10, i++) {

     int milliseconds = i * 100;
     digitalWrite(led_pin_num, HIGH);
     delay(milliseconds);
     digitalWrite(led_pin_num, LOw);
     delay(milliseconds);

   }

   delay(5000);

Analog Read
===========

There are six analog input pins on the Arduino Uno. Sources that supply
continuous voltage from 0 to 5 volts can be read using these pins. For example,
it is useful for reading the voltage from a potentiometer. To read the voltage
from pin ``A0`` you simply call:

.. code-block:: arduino

   int pin_num = A0;

   int val = analogRead(pin_num);

Note that this returns an integer. The on-board analog to digital converter has
10 bit resolution, i.e. 2^10 = 1024 possible readings. The values 0 to 1023 are
mapped to 0 to 5 volts, i.e. .0049 volts per step. You will need a conversion
factor to convert the value from an integer to a voltage value of double
precision.

Exercise
--------

Drop in a power supply component and connect the black pin to the Arduino's
ground and the red pin to the ``A0`` pin. Write some code that causes the
voltage to display to the serial monitor and ensure that it matches the voltage
supplied by the power supply.

`Solution <https://123d.circuits.io/circuits/1588003-simple-analog-read>`__

Arduino IDE
===========

To work with the real Arduino hardware you will use the Arduino integrated
development environment (IDE). The "verify" button compiles your code and
reports any errors you may have. The "upload" button will send the program to
the Arudino for execution.

`Arduino IDE <https://www.arduino.cc/en/Main/Software>`_

Homework Assignment
===================

The goal of the homework assignment is to create a fuel level indicator using a
row of 10 LEDS. The sensor for the fuel level should be a simple potentiometer.
It is connected to a floating bob in the fuel tank and the potentiometer
rotates as the fuel level increases and decreases. The potentiometer voltage 0
to 5 volts maps to a rotation of 270 degrees (the simple potentiometer
component on 123d.circuits.io). If all of the LEDs are on, that signals that the
fuel level is at a maximum and if all of the LEDs are off that signals that the
fuel tank is empty. If some LEDs are on, the number of lights should correspond
linearly to the fuel level. The following diagram shows the physical system.
Your job is to create the electronic side.

.. image:: {filename}/images/fuel-meter.svg
   :width: 600px
   :align: center
