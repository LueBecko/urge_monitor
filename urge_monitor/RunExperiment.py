# -*- coding: utf-8 -*-
# top level experiment control ui

import os
import datetime
import wx
import config
import mainloop
from psychopy import core, logging


#baseDir = os.path.normpath(os.path.join(os.getcwd(), '..'))
baseDir = os.getcwd()

# Create on module wide app object.
# Within this programm there is no other position that uses a wx gui.
app = wx.App()


class ExpFolderException(BaseException):
    '''Exception indicating that the exp-subfolder is not setup correctly'''
    def __init__(self, expFolder):
        super(ExpFolderException, self).__init__()
        self.expFolder = expFolder

    def __str__(self):
        return ('ExpFolder ' + self.expFolder + ' does not exist, is empty' +
            ' or does not contain a valid experiment setup')


def ExperimentSelector():
    '''starts a little gui window, selection of experiment to run'''
    # read experiment list
    exp_folder = baseDir + os.sep + 'exp' + os.sep
    if not os.path.isdir(exp_folder):
        raise ExpFolderException(exp_folder)
    exps = os.listdir(exp_folder)
    for entry in exps:
        if not os.path.isdir(exp_folder + entry):
            exps.remove(entry)
    if len(exps) == 0:
        raise ExpFolderException(exp_folder)
    # start gui
    dlg = wx.Dialog(parent=None, id=-1, title='Select Experiment',
        style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER, size=(200, 150))
    # fill the dialog
    box = wx.BoxSizer(wx.VERTICAL)
    st = wx.StaticText(parent=dlg, id=-1, label=
"""Select one experiment from the list of
found experiment setups.
Experiment setups are found in the subfolder exp
of the programms main folder.""")
    expChoice = wx.Choice(parent=dlg, id=-1, choices=exps)
    OK = wx.Button(dlg, wx.ID_OK, 'Run Experiment')
    OK.SetDefault()
    box.Add(st, flag=wx.ALIGN_LEFT | wx.ALL, border=10)
    box.Add(expChoice, flag=wx.ALIGN_CENTER_HORIZONTAL)
    box.Add(OK, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, border=10)
    dlg.SetSizerAndFit(box)
    # perform
    if dlg.ShowModal() == wx.ID_OK:
        return exps[expChoice.GetSelection()]
    else:
        return None


class ExpDlg(wx.Frame):

    def __init__(self, conf):
        # prepare data
        self.conf = conf
        self.configured = False
        self.runNames = []
        self.runDone = []
        for run in self.conf['exp']['runs']:
            self.runNames.append(run[0])
            self.runDone.append(False)
        # create window
        title = ('Experiment Control: ' + self.conf['exp']['main']['name'])
        #self.app = wx.App()
        super(ExpDlg, self).__init__(parent=None, id=-1, title=title,
            style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER, size=(400, 550))
        # fill the frame
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        tex_top = wx.StaticText(panel, id=wx.ID_ANY,
            label="""Set configuration parameters before running sessions.
Note that no changes will be possible after starting.""")

        line_top = wx.StaticLine(panel)
        line_bot = wx.StaticLine(panel)

        self.but_conf = wx.Button(panel, id=wx.ID_ANY,
            label='Configuration Done',
            size=(150, 30))
        self.but_run = wx.Button(panel, id=wx.ID_ANY, label='Run Session',
            size=(150, 30))
        self.but_run.Disable()
        but_exit = wx.Button(panel, id=wx.ID_ANY, label='Exit', size=(150, 30))

        self.list_run = wx.ListBox(panel, id=wx.ID_ANY, size=(300, 200),
            style=wx.LB_SINGLE | wx.LB_ALWAYS_SB, choices=self.runNames)
        self.list_run.SetSelection(0)
        self.list_run.Disable()
        self.lbl_status = wx.StaticText(panel, id=wx.ID_ANY,
            label="Status: Configuration", style=wx.ALIGN_LEFT, size=(350, 30))

        self.confField = self.addConfFields(panel, self.conf['exp']['info'])

        box.Add(tex_top, flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        box.Add(self.confField,
            flag=wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, border=10)
        box.Add(self.but_conf, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
            border=10)
        box.Add(line_top, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        box.Add(self.list_run, flag=wx.ALIGN_CENTER_HORIZONTAL)
        box.Add(self.but_run, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
            border=10)
        box.Add(self.lbl_status, flag=wx.ALIGN_CENTER_HORIZONTAL)
        box.Add(line_bot, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        box.Add(but_exit, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, self.evConfBut, id=self.but_conf.GetId())
        self.Bind(wx.EVT_BUTTON, self.evRunBut, id=self.but_run.GetId())
        self.Bind(wx.EVT_BUTTON, self.evExitBut, id=but_exit.GetId())
        self.Bind(wx.EVT_CLOSE, self.evClose)
        panel.SetSizerAndFit(box)
        # present & run frame
        self.Centre()
        self.Show()
        app.MainLoop()

    def evConfBut(self, e):
        self.configured = True
        for child in self.confField.GetChildren():
            if child.GetWindow().isInput:
                self.conf['exp']['info'][child.GetWindow().GetKey] = (
                    child.GetWindow().GetValue())
        # prepare exeriment execution ??
        # configure gui
        for child in self.confField.GetChildren():
            child.GetWindow().Disable()
        self.but_conf.Disable()
        self.but_run.Enable()
        self.list_run.Enable()
        self.lbl_status.SetLabel("Status: Ready to start runs")

    def evRunBut(self, e):
        ri = self.list_run.GetSelection()
        if (ri == wx.NOT_FOUND):
            dial = wx.MessageDialog(None, """No run selected""", 'Warning',
                wx.OK | wx.NO_DEFAULT | wx.ICON_WARNING)
            dial.ShowModal()
            return
        # start the run
        dial = wx.MessageDialog(None,
"""Ready?
Press OK when the system is ready to start.""", 'Question',
            wx.OK | wx.ICON_QUESTION)  # | wx.NO_DEFAULT
        dial.ShowModal()
        self.conf['runtime']['curr_run'] = ri
        ## prepare GUI
        if (ri < self.list_run.GetCount() - 1):
            self.list_run.SetSelection(ri + 1)
        self.but_run.Disable()
        self.list_run.Disable()
        self.lbl_status.SetLabel("Status: Running " + self.runNames[ri] +
            "\n(to abort press " + self.conf['exp']['main']['abort_key'] + ")")
        ## RUN
        mainloop.MainLoop(self.conf)
        self.runDone[ri] = True
        ## DONE - reset GUI
        self.but_run.Enable()
        self.list_run.Enable()
        self.lbl_status.SetLabel("Status: Ready to start runs\n" +
            "    Last Run: " + self.runNames[ri])

    def evExitBut(self, e):
        self.Close()

    def evClose(self, e):
        dial = wx.MessageDialog(None,
"""This action will end the current running experiment.
Are you sure?""", 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
            wx.Exit()
        else:
            e.Veto()

    def addConfFields(self, panel, info):
        container = wx.GridSizer(cols=2, gap=wx.Size(10,10))
        for infoKey in info:
            #create label
            inputLabel = wx.StaticText(panel, -1, infoKey,
                style=wx.ALIGN_RIGHT)
            inputLabel.isInput = False
            container.Add(inputLabel, 1, border=10,
                flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT)
            #create input control
            if type(info[infoKey]) == bool:  # check box
                inputBox = wx.CheckBox(panel, -1)
                inputBox.SetValue(info[infoKey])
            elif type(info[infoKey]) in [list, tuple]:  # choice box
                inputBox = wx.Choice(panel, -1, choices=info[infoKey])
                inputBox.GetValue = inputBox.GetStringSelection
                inputBox.SetSelection(0)
            else:  # text box
                inputBox = wx.TextCtrl(panel, -1,
                    info[infoKey])

            inputBox.GetKey = infoKey
            inputBox.isInput = True
            container.Add(inputBox, -1, border=10,
                flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.RIGHT)
        return container

################################################################
## start basic components
clock = core.Clock()
base_log_file =os.path.join(baseDir, 'log.txt')
date_log_file_name = 'log-' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
L = logging.LogFile(f=base_log_file, filemode='w', encoding='utf8', level=0)
logging.setDefaultClock(clock)

logging.info(msg='Experiment started')

eName = ExperimentSelector()
if eName is None:
    core.quit()
logging.info(msg="Selected Experiment: " + eName)

Conf = config.ExperimentConfig(eName, baseDir)
logging.info(msg='Configuration Interface started, read all configs of exp')

## augment eConf with runtime information and run
eControl = ExpDlg(Conf)
del eControl
logging.info('Closing window, closing all other ressources')

from shutil import copyfile
copyfile(base_log_file, 
         os.path.join(baseDir, Conf['exp']['main']['log_folder'],  
                      Conf['exp']['main']['name'],
                      date_log_file_name))

core.quit()
