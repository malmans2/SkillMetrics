import matplotlib.pyplot as plt
import numpy as np

def get_target_diagram_axes(x,y,option):
    '''
    Get axes value for target_diagram function.
    
    Determines the axes information for a target diagram given the axis 
    values (X,Y) and the options in the data structure OPTION returned by 
    the GET_TARGET_DIAGRAM_OPTIONS function.
    
    INPUTS:
    x      : values for x-axis
    y      : values for y-axis
    option : dictionary containing option values. (Refer to 
             GET_TARGET_DIAGRAM_OPTIONS function for more information.)
    
    OUTPUTS:
    axes           : dictionary containing axes information for target diagram
    axes['xtick']  : x-values at which to place tick marks
    axes['ytick']  : y-values at which to place tick marks
    axes['xlabel'] : labels for xtick values
    axes['ylabel'] : labels for ytick values
    option : dictionary containing updated option values
  
    Author: Peter A. Rochford
    Acorn Science & Innovation
        prochford@acornsi.com

    Created on Nov 25, 2016

    @author: rochfordp  
    '''
    # Specify max/min for axes
    foundmax = 1 if option['axismax'] != 0.0 else 0
    if foundmax == 0:
        # Axis limit not specified
        maxx = np.amax(np.absolute(x))
        maxy = np.amax(np.absolute(y))
    else:
        # Axis limit is specified
        maxx = option['axismax']
        maxy = option['axismax']
    
    # Determine default number of tick marks
    plt.figure()
    hhh = plt.plot([-1.0*maxx, -1.0*maxx, maxx, maxx],
                   [-1.0*maxy, maxy, maxy, -1.0*maxy])
    gca = plt.gca()
    v = [gca.get_xlim(), gca.get_ylim()]
    ntest = np.sum(gca.get_xticks() > 0)
    if ntest > 0:
        nxticks = np.sum(gca.get_xticks() > 0)
        nyticks = np.sum(gca.get_yticks() > 0)
        
        # Save nxticks and nyticks as function attributes for later 
        # retrieval in function calls
        get_target_diagram_axes.nxticks = nxticks
        get_target_diagram_axes.nyticks = nyticks
    else:
        # Use function attributes for nxticks and nyticks
        if hasattr(get_target_diagram_axes, 'nxticks') and \
            hasattr(get_target_diagram_axes, 'nxticks'):
            nxticks = get_target_diagram_axes.nxticks
            nyticks = get_target_diagram_axes.nyticks
        else:
            raise ValueError('No saved values for nxticks & nyticks.')
    
    hhh.pop(0).remove()
    plt.close()
    
    # Set default tick increment and maximum axis values
    if foundmax == 0:
        maxx = v[0][1]
        maxy = v[1][1]
        option['axismax'] = max(maxx, maxy)
    
    # Check if equal axes requested
    if option['equalaxes'] == 'on':
        if maxx > maxy:
            maxy = maxx
            nyticks = nxticks
        else:
            maxx = maxy
            nxticks = nyticks

    # Convert to integer if whole number
    if type(maxx) is float and maxx.is_integer(): maxx = int(round(maxx))
    if type(maxx) is float and maxy.is_integer(): maxy = int(round(maxy))
    minx = -maxx; miny = -maxy
    
    # Determine tick values
    if len(option['ticks']) > 0:
        xtick = option['ticks']
        ytick = option['ticks']
    else:
        tincx = maxx/nxticks
        tincy = maxy/nyticks
        xtick = np.arange(minx, maxx+tincx, tincx)
        ytick = np.arange(miny, maxy+tincy, tincy)
    
    # Assign tick label positions
    if len(option['xticklabelpos']) == 0:
        option['xticklabelpos'] = xtick
    if len(option['yticklabelpos']) == 0:
        option['yticklabelpos'] = ytick
    
    # Set tick labels using provided tick label positions
    xlabel =[]; ylabel = [];
    
    # Set x tick labels
    for i in range(len(xtick)):
        index = np.where(option['xticklabelpos'] == xtick[i])
        if len(index) > 0:
            xlabel.append(str(xtick[i]))
        else:
            xlabel.append('')

    # Set tick labels at 0 to blank
    index = np.where(abs(xtick) < 1.e-7)
    xlabel[index[0]] = ''
    
    # Set y tick labels
    for i in range(len(ytick)):
        index = np.where(option['xticklabelpos'] == xtick[i])
        if len(index) > 0:
            ylabel.append(str(ytick[i]))
        else:
            ylabel.append('')

    # Set tick labels at 0 to blank
    index = np.where(abs(ytick) < 1.e-7)
    ylabel[index[0]] = ''
    
    # Store output variables in data structure
    axes = {}
    axes['xtick'] = xtick
    axes['ytick'] = ytick
    axes['xlabel'] = xlabel
    axes['ylabel'] = ylabel
    
    return axes
