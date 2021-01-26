import logging
import pylsl as lsl


stream_outlet = None


def init(stream_name):
    global stream_outlet
    logging.info('Creating LSL stream: %s' % (stream_name))
    lsl_stream_info = lsl.StreamInfo(name=stream_name,
                                     type='Markers',
                                     channel_format=lsl.cf_string,
                                     source_id='UrgeMonitor01')
    stream_outlet = lsl.StreamOutlet(lsl_stream_info)


def send_marker(value):
    global stream_outlet
    if stream_outlet:
        stream_outlet.push_sample([value])
    else:
        raise Exception('LSL stream not initialized')
