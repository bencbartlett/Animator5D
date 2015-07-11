#####################################################################################################
# Animator5D                                                                                        #
# Ben Bartlett                                                                                      #
# benjamincbartlett AT gmail DOT com                                                               #|Side comments go here.
# github.com/bencbartlett/Animator5D                                                                #
# Program to render an animated gif of a 5-dimensional system (x, y, z, time, color quantity)       #
# I originally write this to reconstruct EM scattering in the CMS detector over time, using         #
# energy deposited per layer as the fifth "w" quantity, but use it however you want                 #
#####################################################################################################


import os, shutil, subprocess, signal                                                              #|System stuff
import numpy as np                                                                                 #|The package takes structured numpy arrays as arguments, but it shouldn't be terrible to modify it to take a list instead.
import matplotlib.pyplot as plt                                                                    #|Matplotlib stuff
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D, art3d

def animate(data, title="Animator5D", path="Animator5D Rendering", tstep=False, 
                  xname='x', yname='y', zname='z', wname='w', tname='t', 
                  xlim=False, ylim=False, zlim=False, wlim=False, tlim=False, 
                  xlabel='x', ylabel='y', zlabel='z', wlabel='w', tlabel='units', 
                  projections=True, transparency=False, delete=False, quiet=False, 
                  scalesize=True, msize=100, marker=",", renderframes=True):

    '''
    Usage: animate(data, title, tstep).

    Arguments:      data    np.recarray: structured array containing x, y, z, t, w data labeled with
                                    'x', 'y', 'z', 't', 'w'. (You can easily modify this to just be  
                                    a list that takes these quantities in order if you don't want to
                                    use structured arrays though.)
                    
    Optnl Params:   title   String: Title of the plot. Default: "Animator5D"
                    path    String: relative path frames and animation are saved to. 
                                    Default: "Animator5D Rendering/"
                    tstep   Float:  Time step for t. Defaults such that 50 frames are animated.
                    xname   String: Name of x-data entry in data. Default: "x"
                    yname   String: Name of y-data entry in data. Default: "y"
                    zname   String: Name of z-data entry in data. Default: "z"
                    wname   String: Name of w-data entry in data. Default: "w"
                    tname   String: Name of t-data entry in data. Default: "t"
                    xlim    List or tuple: sets the x-limit of the plot. Default: Automatic
                    ylim    List or tuple: sets the y-limit of the plot. Default: Automatic
                    zlim    List or tuple: sets the z-limit of the plot. Default: Automatic 
                    wlim    List or tuple: sets the w-limit of the plot. Default: Automatic 
                    tlim    List or tuple: sets the time interval to animate. Default: Automatic
                    xlabel  String: label to set x axis to. Default: "x"
                    ylabel  String: label to set y axis to. Default: "y"
                    zlabel  String: label to set z axis to. Default: "z"
                    wlabel  String: label to set w (color bar) axis to. Default: "w"
                    tlabel  String: determines units of time counter in upper left. Default: "units"
                    marker  String: marker type in matplotlib syntax. Default: ","
                    msize   Int:    marker size for matplotlib use. Default: 100
                    
    Options:        delete          Bool: delete frames when finished. Defualt: False
                    quiet           Bool: do not print statuses in terminal. Default: False
                    projections     Bool: include "shadow" projections of data to xy xz and yz 
                                          planes. Default: True
                    transparency    Bool: use matplotlib's default auto-transparency in 3D plots in 
                                          plotting the data. Default: False 
                    scalesize       Bool: scale marker size per point with that point's w value. 
                                          Default: True 
                    renderframes    Bool: whether or not to use render the frames to a single
                                          animated gif. Requires ImageMagick to render frames.
                                          Default: True
    '''
    # Interruption handler, in case you mistype the number of frames or something.
    def signal_handler(signal, frame):
        import sys
        print '(!) Rendering aborted: KeyboardInterrupt.'
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Set up figure
    colormap = cm.rainbow                                                                          #|Change this value to whatever you want
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')

    # Import and parse data
    data           = np.sort(data, order = [tname])
    xd,yd,zd,td,wd = data[xname], data[yname], data[zname], data[tname], data[wname]               #|Data is in numpy structured arrays, you can change this to lists though if you want
    maxwd          = np.max(wd)
    normwd         = wd / maxwd                                                                    #|Normalized w function                                                  
    xmin, xmax     = min(xd), max(xd)                                                              #|Get and set limits
    ymin, ymax     = min(yd), max(yd)
    zmin, zmax     = min(zd), max(zd)

    # Limits and labels
    ax.set_xlim(xmin, xmax)                                                                        #|Set axes and then modify later
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
    if xlim: ax.set_xlim(xlim)
    if ylim: ax.set_ylim(ylim)
    if zlim: ax.set_zlim(zlim)
    ax.set_xlabel(xlabel)                                                                          #|Label stuff
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    # Set up and clear path
    if os.path.exists(path):                                                                       #|Remove previous crap if anything is there
        shutil.rmtree(path)
        os.makedirs(path+"/frames")
    else:
        os.makedirs(path+"/frames")

    # Set up initial frame
    if tlim:
        t0, maxt = tlim
        t        = t0 
    else: 
        t = t0   = np.min(td)
        maxt     = np.max(td)
    if tstep == False: 
        tstep = (maxt-t0) / 50.0
    count    = 1 
    nframes  = int((maxt-t0)/tstep)
    title    = ax.text2D(.3,1.0, title, transform=ax.transAxes, size='large')
    colorcal = ax.scatter([0,0],[0,0],[0,0], c=[0,maxwd + 1], cmap=colormap)
    cbar     = fig.colorbar(colorcal, shrink=.7)
    cbar.set_label(wlabel) 

    # Render each frame over time
    while t <= np.max(maxt):
        if not quiet: print "Rendering %i of %i frames..." % (count, nframes)
        mask = np.logical_and(t<td, td<=(t+tstep))                                                 #|What to plot in this time step
        xplt = np.extract(mask, xd) 
        yplt = np.extract(mask, yd)
        zplt = np.extract(mask, zd)
        wplt = np.extract(mask, wd)
        if scalesize: 
            sizes = 100*wplt/maxwd
        else: 
            sizes = 100
        txt  = ax.text2D(0.1, 0.9,('$t=%.3f$'%t)+tlabel, transform=ax.transAxes)
        cx   = np.ones_like(xplt) * ax.get_xlim3d()[0]                                             #|Again, not a typo with mixing x and z
        cy   = np.ones_like(yplt) * ax.get_ylim3d()[1]
        cz   = np.ones_like(zplt) * ax.get_zlim3d()[0]
        mark = ax.scatter(xplt, yplt, zplt, c=wplt, cmap=colormap, vmin=0, vmax=maxwd, \
                                            s=sizes, marker=marker, lw=1)
        if projections:
            ax.scatter(xplt, yplt, cz, c='#444444', marker=marker, lw=0, s=sizes, alpha=0.3)       #|Plot the projections
            ax.scatter(xplt, cy, zplt, c='#444444', marker=marker, lw=0, s=sizes, alpha=0.3)
            ax.scatter(cx, yplt, zplt, c='#444444', marker=marker, lw=0, s=sizes, alpha=0.3)
        if transparency == False: mark.set_edgecolors = mark.set_facecolors = lambda *args:None    #|Super-hacky way to disable transparency in the 3D plot, makes it cleaner to read.

        plt.draw()
        plt.savefig(path + "/frames/"+str(count).zfill(3)+".gif")                                  #|Save the frame. zfill(3) supports up to 999 frames, change as you want.
        txt.remove()
        count += 1                                                                                 #|Increment frame number
        t += tstep                                                                                 #|Increment t

    # Combine frames
    if not quiet: print "Combining frames; may take a minute..."
    args = (['convert', '-delay', '.1', '-loop', '0', path+"/frames/*.gif", path+"/animation.gif"])#|This part requires ImageMagick to function. Change the arguments as you wish.
    subprocess.check_call(args)
    if not quiet: print "Successfully saved as "+path+"/animation.gif."
    if delete:
        shutil.rmtree(path+"/frames")
        if not quiet: print "Successfully deleted frames." 


if __name__ == "__main__":
    # Demonstration for how this program works
    data1 = np.load("SampleData/SampleData1.npy")
    data2 = np.load("SampleData/SampleData2.npy")
    # Super simple animation allowing the program to calculate defaults.
    animate(data1)
    # You can also adjust the parameters very easily for much more customization.
    animate(data2, title="EM Shower Reconstructed", path="EMReconstruction", tstep=.05, 
                   xname='z', zname='x', tname="correctT", wname="en", 
                   xlim=[320,340], ylim=[-50,-35], zlim=[40,55],
                   xlabel="x (cm)", ylabel="y (cm)", zlabel="Beamline (cm)", wlabel="Energy (keV)",
                   tlabel="ns", projections=True, transparency=True, delete=True, quiet=False, 
                   scalesize=False, msize=75, marker="o") 







