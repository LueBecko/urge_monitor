# -*- coding: utf-8 -*-
import sys
sys.path.append('../urge_report_fmri')
sys.path.append('../dependencies')

from psychopy import core, logging

import visuals  # to test
import config  # just to read config data

print('testing all properties and performance from the visuals class')

clock = core.Clock()
L = logging.LogFile(f='log.txt', filemode='w', encoding='utf8', level=0)

logging.setDefaultClock(clock)
logging.exp(msg='Testbench started')
Conf = config.config()  # read default config parameters
t = 5.0


def updateurgevalue_continous():
    updateurgevalue_continous.urgevalue += updateurgevalue_continous.increment
    if updateurgevalue_continous.urgevalue >= 1.0:
        updateurgevalue_continous.increment = -0.01
    elif updateurgevalue_continous.urgevalue <= 0.0:
        updateurgevalue_continous.increment = 0.01
    return updateurgevalue_continous.urgevalue
updateurgevalue_continous.urgevalue = 0.5
updateurgevalue_continous.increment = 0.01


def graphic_main(C, test_id, t):
    visuals.CreateVisuals(Cmon=C['monitor'],
        Cwin=C['window'],
        Cvis=C['visuals'])
    visuals.annote.AddAnnote(name='ID',
        text=test_id,
        pos=[0, 4],
        size=1,
        col=[255, 255, 255])
    fc = 0
    plotclock_increment = 1.0 / int(C['main']['hist_rate'])
    plotclock = core.Clock()
    T = core.Clock()
    while T.getTime() < t:
        urgevalue = updateurgevalue_continous()

        if plotclock.getTime() > 0.0:  # update plot
            visuals.hist.updateHist(urgevalue)
            plotclock.add(plotclock_increment)

        visuals.bars.UpdateFGBar(urgevalue)
        visuals.flip()
        fc += 1

    visuals.CloseVisuals()
    return fc


# begin tests: fullscr
test_id = 'test0: defaults'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.1: defaults + background col changed'
Conf['visuals']['col'] = (255, 127, 0)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.2: defaults + center_pos changed'
Conf['visuals']['pos'] = [2, -1]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# bg_bar
test_id = 'test0.3.1: defaults + bgbar geometry changed'
Conf['visuals']['bg_width'] = 2.0
Conf['visuals']['bg_height'] = 5.0
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.3.2: defaults + bg_col changed'
Conf['visuals']['bg_col'] = (0, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.3.3: defaults + bg_frame_* changed'
Conf['visuals']['bg_frame_col'] = (63, 127, 191)
Conf['visuals']['bg_frame_width'] = 5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# fg_bar
test_id = 'test0.4.1: defaults + fgbar geometry changed'
Conf['visuals']['fg_width'] = 2.5
Conf['visuals']['fg_height'] = 0.75
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.4.2: defaults + fg_col changed'
Conf['visuals']['fg_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.4.3: defaults + fg_frame_* changed'
Conf['visuals']['fg_frame_col'] = (63, 192, 192)
Conf['visuals']['fg_frame_width'] = 5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.4.4: defaults + fg_opacity changed'
Conf['visuals']['fg_opacity'] = 0.25
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# hist
test_id = 'test0.5.1: defaults + hist_col changed'
Conf['visuals']['hist_col'] = (255, 0, 0)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.2: defaults + hist_line_width changed'
Conf['visuals']['hist_line_width'] = 6
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.3: defaults + hist_width changed'
Conf['visuals']['hist_width'] = 4.5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.4: defaults + hist_samples changed'
Conf['visuals']['hist_samples'] = 60
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.5.1: defaults + hist_side none'
Conf['visuals']['hist_side'] = 'none'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.5.2: defaults + hist_side left'
Conf['visuals']['hist_side'] = 'left'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.5.3: defaults + hist_side right'
Conf['visuals']['hist_side'] = 'right'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.5.4: defaults + hist_side both'
Conf['visuals']['hist_side'] = 'both'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

Conf['visuals']['hist_fade'] = False
test_id = 'test0.5.6.1: defaults + hist_side none (no fade)'
Conf['visuals']['hist_side'] = 'none'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.6.2: defaults + hist_side left (no fade)'
Conf['visuals']['hist_side'] = 'left'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.6.3: defaults + hist_side right (no fade)'
Conf['visuals']['hist_side'] = 'right'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.5.6.4: defaults + hist_side both (no fade)'
Conf['visuals']['hist_side'] = 'both'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

Conf['visuals']['hist_fade'] = True
# scale
test_id = 'test0.6.1: defaults + simple scale (1, b)'
Conf['visuals']['scales_text'] = ['']
Conf['visuals']['scales_text_pos'] = ['c']
Conf['visuals']['scales_text_size'] = [0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.25
Conf['visuals']['scales_widthr'] = 0.25
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.2: defaults + simple scale (2, r)'
Conf['visuals']['scales_text'] = ['', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.0
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 6
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.3: defaults + simple scale (3, l)'
Conf['visuals']['scales_text'] = ['', '', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.8
Conf['visuals']['scales_widthr'] = 0.0
Conf['visuals']['scales_thickness'] = 2
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.4: defaults + simple scale (5, b)'
Conf['visuals']['scales_text'] = ['', '', '', '', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c', 'c', 'c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.5: defaults + text scales'
Conf['visuals']['scales_text'] = ['0', '', '', '', '100']
Conf['visuals']['scales_text_pos'] = ['b', 'c', 'c', 'c', 'a']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.5: defaults + text scales'
Conf['visuals']['scales_text'] = ['0', '25', '50', '75', '100']
Conf['visuals']['scales_text_pos'] = ['b', 'l', 'c', 'r', 'a']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.6.5: defaults + text scales'
Conf['visuals']['scales_text'] = ['Nothing', 'Low', 'Medium', 'High', 'Highest']
Conf['visuals']['scales_text_pos'] = ['b', 'l', 'c', 'r', 'a']
Conf['visuals']['scales_text_size'] = [1.2, 0.6, 0.2, 0.6, 1.2]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# annotations
test_id = 'test0.7.1: defaults + annotations'
Conf['visuals']['aname'] = ['a1']
Conf['visuals']['atext'] = ['Annotation 1']
Conf['visuals']['apos'] = [[0, 0]]
Conf['visuals']['asize'] = [0.5]
Conf['visuals']['acol'] = [[0, 0, 0]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.7.2: defaults + annotations'
Conf['visuals']['aname'] = ['a1', 'a2']
Conf['visuals']['atext'] = ['Annotation 1', 'More Annotations']
Conf['visuals']['apos'] = [[0, 0], [-3, -2]]
Conf['visuals']['asize'] = [0.5, 1]
Conf['visuals']['acol'] = [[0, 0, 0], [255, 0, 127]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test0.7.3: defaults + annotations'
Conf['visuals']['aname'] = ['a1', 'a2', 'a3']
Conf['visuals']['atext'] = ['Annotation 1', 'More Annotations', 'Lorem Ipsum']
Conf['visuals']['apos'] = [[0, 0], [-3, -2], [2, -1]]
Conf['visuals']['asize'] = [0.5, 1, 2]
Conf['visuals']['acol'] = [[0, 0, 0], [255, 0, 127], [255, 255, 0]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# begin tests: windowed
Conf = config.config()
Conf['window']['fullscr'] = False
Conf['window']['resolution'] = [1024, 768]

test_id = 'test1: win'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.1: win + background col changed'
Conf['visuals']['col'] = (255, 127, 0)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.2: win + center_pos changed'
Conf['visuals']['pos'] = [2, -1]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# bg_bar
test_id = 'test1.3.1: win + bgbar geometry changed'
Conf['visuals']['bg_width'] = 2.0
Conf['visuals']['bg_height'] = 5.0
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.3.2: win + bg_col changed'
Conf['visuals']['bg_col'] = (0, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.3.3: win + bg_frame_* changed'
Conf['visuals']['bg_frame_col'] = (63, 127, 191)
Conf['visuals']['bg_frame_width'] = 5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# fg_bar
test_id = 'test1.4.1: win + fgbar geometry changed'
Conf['visuals']['fg_width'] = 2.5
Conf['visuals']['fg_height'] = 0.75
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.4.2: win + fg_col changed'
Conf['visuals']['fg_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.4.3: win + fg_frame_* changed'
Conf['visuals']['fg_frame_col'] = (63, 192, 192)
Conf['visuals']['fg_frame_width'] = 5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.4.4: win + fg_opacity changed'
Conf['visuals']['fg_opacity'] = 0.25
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# hist
test_id = 'test1.5.1: win + hist_col changed'
Conf['visuals']['hist_col'] = (255, 0, 0)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.2: win + hist_line_width changed'
Conf['visuals']['hist_line_width'] = 6
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.3: win + hist_width changed'
Conf['visuals']['hist_width'] = 4.5
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.4: win + hist_samples changed'
Conf['visuals']['hist_samples'] = 60
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.5.1: win + hist_side none'
Conf['visuals']['hist_side'] = 'none'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.5.2: win + hist_side left'
Conf['visuals']['hist_side'] = 'left'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.5.3: win + hist_side right'
Conf['visuals']['hist_side'] = 'right'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.5.4: win + hist_side both'
Conf['visuals']['hist_side'] = 'both'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

Conf['visuals']['hist_fade'] = False
test_id = 'test1.5.6.1: win + hist_side none (no fade)'
Conf['visuals']['hist_side'] = 'none'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.6.2: win + hist_side left (no fade)'
Conf['visuals']['hist_side'] = 'left'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.6.3: win + hist_side right (no fade)'
Conf['visuals']['hist_side'] = 'right'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.5.6.4: win + hist_side both (no fade)'
Conf['visuals']['hist_side'] = 'both'
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

Conf['visuals']['hist_fade'] = True
# scale
test_id = 'test1.6.1: win + simple scale (1, b)'
Conf['visuals']['scales_text'] = ['']
Conf['visuals']['scales_text_pos'] = ['c']
Conf['visuals']['scales_text_size'] = [0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.25
Conf['visuals']['scales_widthr'] = 0.25
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.2: win + simple scale (2, r)'
Conf['visuals']['scales_text'] = ['', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.0
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 6
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.3: win + simple scale (3, l)'
Conf['visuals']['scales_text'] = ['', '', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.8
Conf['visuals']['scales_widthr'] = 0.0
Conf['visuals']['scales_thickness'] = 2
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.4: win + simple scale (5, b)'
Conf['visuals']['scales_text'] = ['', '', '', '', '']
Conf['visuals']['scales_text_pos'] = ['c', 'c', 'c', 'c', 'c']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (0, 255, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.5: win + text scales'
Conf['visuals']['scales_text'] = ['0', '', '', '', '100']
Conf['visuals']['scales_text_pos'] = ['b', 'c', 'c', 'c', 'a']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.5: win + text scales'
Conf['visuals']['scales_text'] = ['0', '25', '50', '75', '100']
Conf['visuals']['scales_text_pos'] = ['b', 'l', 'c', 'r', 'a']
Conf['visuals']['scales_text_size'] = [0.5, 0.5, 0.5, 0.5, 0.5]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.6.5: win + text scales'
Conf['visuals']['scales_text'] = ['Nothing', 'Low', 'Medium', 'High', 'Highest']
Conf['visuals']['scales_text_pos'] = ['b', 'l', 'c', 'r', 'a']
Conf['visuals']['scales_text_size'] = [1.2, 0.6, 0.2, 0.6, 1.2]
Conf['visuals']['scales_text_col'] = [255, 255, 255]
Conf['visuals']['scales_widthl'] = 0.5
Conf['visuals']['scales_widthr'] = 0.5
Conf['visuals']['scales_thickness'] = 4
Conf['visuals']['scales_col'] = (255, 0, 255)
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# annotations
test_id = 'test1.7.1: win + annotations'
Conf['visuals']['aname'] = ['a1']
Conf['visuals']['atext'] = ['Annotation 1']
Conf['visuals']['apos'] = [[0, 0]]
Conf['visuals']['asize'] = [0.5]
Conf['visuals']['acol'] = [[0, 0, 0]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.7.2: win + annotations'
Conf['visuals']['aname'] = ['a1', 'a2']
Conf['visuals']['atext'] = ['Annotation 1', 'More Annotations']
Conf['visuals']['apos'] = [[0, 0], [-3, -2]]
Conf['visuals']['asize'] = [0.5, 1]
Conf['visuals']['acol'] = [[0, 0, 0], [255, 0, 127]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

test_id = 'test1.7.3: win + annotations'
Conf['visuals']['aname'] = ['a1', 'a2', 'a3']
Conf['visuals']['atext'] = ['Annotation 1', 'More Annotations', 'Lorem Ipsum']
Conf['visuals']['apos'] = [[0, 0], [-3, -2], [2, -1]]
Conf['visuals']['asize'] = [0.5, 1, 2]
Conf['visuals']['acol'] = [[0, 0, 0], [255, 0, 127], [255, 255, 0]]
fc = graphic_main(Conf, test_id, t)
logging.info(msg='Test completed - '
        + test_id + ' (' + str(fc) + ' frames/' + str(t) + ' s)')
logging.flush()

# end everything
core.quit()
