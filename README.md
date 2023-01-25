# Channel Estimation on the POWDER Platform

In this tutorial, we show how to perform a channel sounding experiment using the CBRS rooftop nodes. Slides with information about the channel sounder and relevant background information as well as a picture-guided tutorial can be found at [this link](https://docs.google.com/presentation/d/1W21RtjDfAuz6N182H0d56oc8SeaYWBAFSC1oGlfGyWk/edit?usp=sharing). For this experiment, it is assumed that you have already created a POWDER account and have access to node reservations.

## Instantiate Experiment

Once logged onto POWDER, navigate to:

**Experiments &rarr; Start Experiment &rarr; Change Profile &rarr; signal_power &rarr; Select Profile &rarr; Next**

Now we want to select the compute node type (d740) and base stations for the experiment. The frequency range you have access to is dependent on the project you belong to. For this experiment, a range of 3550MHz to 3560MHz is sufficient.

Any of the X310 CBRS Radio can be used. To add a radio, click the plus arrow and select a [location](https://powderwireless.net/area) from the drop down. A minimum of 2 radios is needed for transmission and reception. Check [resource availibilty](https://www.powderwireless.net/resinfo.php?embedded=true) to find open radios or reserve them beforehand.

**&rarr; Next**

Now you can name your experiment (optional).

**&rarr; Next**

Create a start and end time for your experiment (optional). Leaving the fields empty keeps your experiment availible for 16 hours.

**&rarr; Finish**

## SSH into Nodes

After your experiment is done setting up, SSH into the nodes.

**On the receiver node, you will want to make sure the following packages are installed in order for the python script for analysis will work:**

- Plotly
- SciPy
- NumPy
- Pandas
- Matplotlib
- fim

## Transmission

On the node you wish to transmit from, use the following command:

`cir_tx.py -a 0.5 -f 3555e6 -d 8 -g 31.5 -s 24e6`

For help on the arguments, use:

`cir_tx.py -h`

optional arguments: 

`-a` alpha value for root raised cosine filter

`-f` center frequency

`-d` degree of LSFR (corresponds to length L of PN sequence). L = 2^d - 1

`-g` gain of transmitter or receiver

`-s` sample rate 

## Reception

On the node(s) you with to receive from, use the following command:

`cir_rx8d.py -a 0.5 -f 3555e6 -g 31.5 -s 24e6`

This is for 8 degree PN sequence reception. Similarly for degrees 9 and 10, just use the commands:

`cir_rx9d.py` or `cir_rx10d.py`

Hit enter to stop reception. 5 seconds should be sufficient for a measurement, although you can continue receiving for longer. Longer recordings can become quite large files so post processing may take longer. 

## Analysis

Now that you have finished reception, a complex binary file "CIR" storing the channel impulse response should appear in your directory. We can use the script `pdp_analysis.py` to analyse the channel inpulse response file. The script returns the **rms delay** and **mean delay** as well as a PNG and CSV of the power delay profile.

Input the command:

`pdp_analysis.py -p pathToCirFile -w 100 -d 8 -s 24e6 -n nameOfPng -c nameOfCSV`

For example, if your CIR file is in the home directory, you would enter:

`pdp_analysis.py -p ~/CIR -w 100 -d 8 -s 24e6 -n pdp_image -c pdp`

optional arguments: 

`-p` Path to CIR file

`-w` Number of windows to average. More windows will increase signal to noise ratio

`-d` degree of LSFR (corresponds to length L of PN sequence). L = 2^d - 1

`-s` sample rate

`-n` Name of PNG file

`-c' Name of CSV file


