#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Spread Spectrum Rx
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

'''
def timing(self,userStartTime):
    user_start_time = userStartTime

    # Convert local time to sturct_time format
    local_time = time.time()
    user_time = time.localtime(local_time)
    print('user time = ',user_time[0:9])

    # Create future time in struct_time format
    t = user_time[0:4]+user_start_time+(0,)+user_time[6:9]

    # Convert future time to seconds
    future_time = time.mktime(t)
    print('Start time in Sec: ', future_time)

    # Set start time delay to time difference between future and local time
    start_time = int(future_time - local_time)

    # Set start time, where start_time > 2.0
    self.uhd_usrp_source_0.set_start_time(uhd.time_spec(start_time))

    # Set to one radio next pps, initially
    self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0.0))
    curr_hw_time = self.uhd_usrp_source_0.get_time_last_pps()
    while curr_hw_time==self.uhd_usrp_source_0.get_time_last_pps():
        pass
    # Sleep for 50ms
    time.sleep(0.05)

    # Synchronize both radios time registers
    self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec_t(0.0))

    # Sleep for a couple seconds to make sure all usrp time registers latched and settled
    time.sleep(2)

    # Check the last pps time
    for ii in range(0,5):
        last_pps0 = self.uhd_usrp_source_0.get_time_last_pps()

        print("last_pps0 : %6.12f"%uhd.time_spec_t.get_real_secs(last_pps0))

        time.sleep(1.0)

    # For completion varification
    print(time.ctime())
    print('Processing time: ', time.process_time())

    return future_time

'''
class cir_rx8d(gr.top_block):

    def __init__(self, alpha=0.5, center_freq=3555e6, gain=20, index=0, samp_rate=24e6, start_time=59, duration = 2):
        gr.top_block.__init__(self, "Spread Spectrum Rx")

        ##################################################
        # Parameters
        ##################################################
        self.alpha = alpha
        self.center_freq = center_freq
        self.gain = gain
        self.index = index
        self.samp_rate = samp_rate
        self.start_time = start_time
        self.duration = duration
        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                samp_rate,
                alpha,
                64))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(duration*samp_rate))
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'RAW', False)
        self.blocks_file_sink_1.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_head_0, 0))

        self.init_timed_streaming(self.start_time)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate, self.alpha, 64))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate, self.alpha, 64))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def init_timed_streaming(self, start_time):
        user_start_time = (int(start_time),)

        # Convert local time to sturct_time format
        local_time = time.time()
        user_time = time.localtime(local_time)

        # Create future time in struct_time format
        t = user_time[0:4]+user_start_time+(0,)+user_time[6:9]

        # Convert future time to seconds
        future_time = time.mktime(t)
        print('Start time in Sec: ', future_time)

        local_time = time.time()
        start = int(future_time-local_time)

        self.uhd_usrp_source_0.set_start_time(uhd.time_spec(start))

        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))
        curr_hw_time = self.uhd_usrp_source_0.get_time_last_pps()
        while curr_hw_time==self.uhd_usrp_source_0.get_time_last_pps():
                pass
        time.sleep(0.05)

        self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec_t(0))

        time.sleep(2)

        '''
        tnow = self.uhd_usrp_source_0.get_time_now()

        self.reasonable_delay = delay


        #capture and transmit start at t0
        self.t0 = tnow + uhd.time_spec_t(self.reasonable_delay)
        self.t0_secs = self.t0.get_real_secs()
        print("tnow secs = ", tnow.get_real_secs())
        print("t0_secs = ", self.t0_secs)

        self.uhd_usrp_source_0.set_start_time(self.t0)
        '''

def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-a", "--alpha", dest="alpha", type=eng_float, default="500.0m",
        help="Set alpha [default=%(default)r]")
    parser.add_argument(
        "-f", "--center-freq", dest="center_freq", type=eng_float, default="3.555G",
        help="Set center_freq [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain", dest="gain", type=eng_float, default="20.0",
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "-i", "--index", dest="index", type=eng_float, default="0.0",
        help="Set index [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default="24.0M",
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "-t", "--start_time", dest="start_time", type=eng_float, default="59.0",
        help="Set start time in min relative to curr hour [default=%(default)r]")
    parser.add_argument(
        "-d", "--duration", dest="duration", type=eng_float, default="2",
        help="Set receiver duration in sec [default=%(default)r]")
    return parser


def main(top_block_cls=cir_rx8d, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(alpha=options.alpha, center_freq=options.center_freq, gain=options.gain,\
                       index=options.index, samp_rate=options.samp_rate, start_time=options.start_time, duration=options.duration)
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()
'''
    start_time=options.start_time
    run_time=options.run_time

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    future_time = timing(tb,start_time)
    print('future time = ',future_time)
    print('receiver starting now')
    tb.start()
    time.sleep(run_time)
    tb.stop()
    tb.wait()
    sys.exit(0)
'''


if __name__ == '__main__':
    main()
