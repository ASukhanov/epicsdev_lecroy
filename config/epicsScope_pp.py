"""Pypet page for LeCroy oscilloscopes served by epicsdev_lecroy server."""
# pylint: disable=invalid-name
__version__ = 'v1.0.0 2026-02-15'
print(f'epicsdev_lecroy {__version__}')

#``````````````````Definitions````````````````````````````````````````````````
# python expressions and functions, used in the spreadsheet
_ = ''
def span(x,y=1): return {'span':[x,y]}
def color(*v): return {'color':v[0]} if len(v)==1 else {'color':list(v)}
def font(size): return {'font':['Arial',size]}
def just(i): return {'justify':{0:'left',1:'center',2:'right'}[i]}
def slider(minValue,maxValue):
    """Definition of the GUI element: horizontal slider with flexible range"""
    return {'widget':'hslider','opLimits':[minValue,maxValue],'span':[2,1]}

LargeFont = {'color':'light gray', 'font':['Arial',13],
    'fgColor':'dark green'}
ButtonFont = {'font':['Open Sans Extrabold',14]}
LYRow = {'ATTRIBUTES':{'color':'light yellow'}}
lColor = color('lightGreen')

# definition for plotting cell
PyPath = 'python -m'
PaneT = 'timing[1] timing[2] timing[3]'
#``````````````````PyPage Object``````````````````````````````````````````````
class PyPage():
    """Pypet page for LeCroy oscilloscopes served by epicsdev_lecroy server"""
    def __init__(self, instance:str, title:str, channels=4):
        """instance: unique name of the page.
        For EPICS it is usually device prefix 
        """
        print(f'Instantiating Page {title} for device{instance} with {channels} channels')

        #``````````Mandatory class members starts here````````````````````````
        self.namespace = 'PVA'
        self.title = title

        #``````````Page attributes, optional`````````````````````````````
        self.page = {**color(240,240,240)}

        #``````````Definition of columns`````````````````````````````
        self.columns = {
            1: {'width': 120, 'justify': 'right'},
            2: {'width': 80},
            3: {'width': 80},
            4: {'width': 80},
            5: {'width': 80},
            6: {'width': 80},
            7: {'width': 80},
            8: {'width': 80},
            9: {'width': 80},
        }
        D = instance

        #``````````Abbreviations, used in cell definitions
        def ChLine(suffix):
            return [f'{D}c{ch+1:02}{suffix}' for ch in range(channels)]
        
        PaneP2P = ' '.join([f'c{i+1:02}Peak2Peak c{i+1:02}Mean' for i in range(channels)])
        PaneWF = ' '.join([f'c{i+1:02}Waveform' for i in range(channels)])
        Plot = {'Plot':{'launch':f'{PyPath} pvplot -aV:{instance} -#0"{PaneP2P}" -#1"{PaneWF}" -#2"{PaneT}"',
            **lColor, **ButtonFont}}
        print(f'Plot command: {Plot}')

        #``````````mandatory member```````````````````````````````````````````
        self.rows = [
['Device:',D, {D+'server':LargeFont}, {'Save:':just(2)},D+'setup',
    D+'host', D+'version'],
['Status:', {D+'status': span(8,1)}],
['Cycle time:',D+'cycleTime', 'Sleep:',D+'sleep', 'Cycle:',D+'cycle', Plot],
['Triggers recorded:', D+'acqCount', 'Lost:', D+'lostTrigs',
  'Acquisitions:',D+'scopeAcqCount',_], 
['Time/Div:', {D+'timePerDiv':span(2,1)},_,'recLength:', D+'recLengthS',
  D+'recLengthR',_],
['SamplingRate:', {D+'samplingRate':span(2,1)},_,_,_,_,_],
['Trigger state:',D+'trigState','   trigMode:',D+'trigMode',
  'TrigLevel','TrigDelay',_],
[{D+'trigger':color('lightCyan')}, D+'trigSource', D+'trigCoupling',
  D+'trigSlope', D+'trigLevel', D+'trigDelay',_],
[{'ATTRIBUTES':color('lightGreen')}, 'Channels:','CH1','CH2','CH3','CH4','CH5','CH6'],
['Volt/Div:']+ChLine('VoltsPerDiv'),
['Offset:']+ChLine('VoltOffset'),
['Coupling:']+ChLine('Coupling'),
['Termination:']+ChLine('Termination'),
['On/Off:']+ChLine('OnOff'),
['Peak2Peak:']+ChLine('Peak2Peak'),
['Mean:']+ChLine('Mean'),
[LYRow,'',{'For Experts only!':{**span(6,1),**font(14)}}],
[LYRow,'Scope command:', {D+'instrCmdS':span(2,1)},_,{D+'instrCmdR':span(4,1)}],
[LYRow,'Special commands', {D+'instrCtrl':span(2,1)},_,_,_,_,_,],
[LYRow,'Timing:',{D+'timing':span(6,1)}],
]
