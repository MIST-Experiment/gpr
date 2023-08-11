#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.8.0-rc1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time



from gnuradio import qtgui

class fmcw_sim(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fmcw_sim")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 12000000
        self.center_freq = center_freq = 100000000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0_0 = uhd.usrp_source(
            ",".join(("serial=326F639", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='num send f rames = 1024',
                channels=[0,1],
            ),
        )
        self.uhd_usrp_source_0_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0_0_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0_0_0.set_bandwidth(samp_rate/2, 0)
        self.uhd_usrp_source_0_0_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0_0_0.set_normalized_gain(0.5, 0)

        self.uhd_usrp_source_0_0_0.set_lo_source('internal', uhd.ALL_LOS, 0)
        self.uhd_usrp_source_0_0_0.set_lo_export_enabled(False, uhd.ALL_LOS, 0)
        self.uhd_usrp_source_0_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_source_0_0_0.set_antenna("RX2", 1)
        self.uhd_usrp_source_0_0_0.set_bandwidth(samp_rate/2, 1)
        self.uhd_usrp_source_0_0_0.set_rx_agc(False, 1)
        self.uhd_usrp_source_0_0_0.set_normalized_gain(0.5, 1)

        self.uhd_usrp_source_0_0_0.set_lo_source('internal', uhd.ALL_LOS, 1)
        self.uhd_usrp_source_0_0_0.set_lo_export_enabled(False, uhd.ALL_LOS, 1)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(("serial=326F639", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='num send f rames = 1024',
                channels=[0,1],
            ),
            "",
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(samp_rate/2, 0)
        self.uhd_usrp_sink_0_0.set_normalized_gain(0.5, 0)

        self.uhd_usrp_sink_0_0.set_lo_source('internal', uhd.ALL_LOS, 0)
        self.uhd_usrp_sink_0_0.set_lo_export_enabled(False, uhd.ALL_LOS, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0_0.set_bandwidth(samp_rate/2, 1)
        self.uhd_usrp_sink_0_0.set_normalized_gain(0, 1)

        self.uhd_usrp_sink_0_0.set_lo_source('internal', uhd.ALL_LOS, 1)
        self.uhd_usrp_sink_0_0.set_lo_export_enabled(False, uhd.ALL_LOS, 1)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_sink_x_0_2 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_2.set_update_time(1.0/10000)
        self._qtgui_sink_x_0_2_win = sip.wrapinstance(self.qtgui_sink_x_0_2.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_2.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_2_win)
        self.blocks_vco_f_0_0 = blocks.vco_f(samp_rate, 3140000*2, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0_0_2 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/gprlab/Desktop/gpr/gnu_log/chirp_log', False)
        self.blocks_file_sink_0_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/gprlab/Desktop/gpr/gnu_log/out1_log', False)
        self.blocks_file_sink_0_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/gprlab/Desktop/gpr/gnu_log/out0_log', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SAW_WAVE, 10000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_vco_f_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_sink_0_0_2, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 1))
        self.connect((self.blocks_vco_f_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_vco_f_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_vco_f_0_0, 0), (self.qtgui_sink_x_0_2, 0))
        self.connect((self.uhd_usrp_source_0_0_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0_0, 1), (self.blocks_file_sink_0_0_1, 0))
        self.connect((self.uhd_usrp_source_0_0_0, 0), (self.qtgui_time_sink_x_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fmcw_sim")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_sink_x_0_2.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_bandwidth(self.samp_rate/2, 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(self.samp_rate/2, 1)
        self.uhd_usrp_source_0_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0_0.set_bandwidth(self.samp_rate/2, 0)
        self.uhd_usrp_source_0_0_0.set_bandwidth(self.samp_rate/2, 1)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 1)
        self.uhd_usrp_source_0_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0_0_0.set_center_freq(self.center_freq, 1)




def main(top_block_cls=fmcw_sim, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
