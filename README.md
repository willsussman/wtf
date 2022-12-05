# Where's The Fault

Elements generate raw data. Conveniently, many already store this data. For example, our Jitsi server is configured with InfluxDB; other elements generate log files.

Unfortunately, some elements do not store the data that they generate. For example, Mac computers have `Airport` and `iostat` utilities which report current values but do not store them. We provide `wtf/wifi/raw_wifi.py` and `wtf/cpu/raw_cpu.sh`, respectively, for this purpose.

The stored raw data ultimately needs to be converted into WTF bits. We provide a function in `wtf.py`, `vitals2bits()`, which performs the conversion. However, in order to accept arbitrary signals, we require the raw data to be formatted as `Vital`s, defined in `wtf.py`. We provide `wtf/jitsi/main_jitsi.py`, `wtf/loglevels/main_loglevels.py`, `wtf/wifi/main_wifi.py`, and `wtf/cpu/main_cpu.py`, for this purpose.

In principle, elements could generate WTF bits directly. We do not do this, at least not yet.

`vitals2bits()` applies a simple signal-processing scheme: For the $j$ th sample of vital $i$, if $y_{ij} R \beta_i * EWMA(\alpha_i, y_{ij})$, then the bit is set. Else, the bit is unset. We do not claim that this scheme is optimal; improving it is future work.
