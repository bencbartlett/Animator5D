# Animator5D
Very simple-to-use framework for rendering 5-dimensional animations (x, y, z, time, some color value) as an animated gif. This requires ImageMagick to combine the frames, but you can still render them without having it installed and just combine them with some online gif maker.

## Example rendering
Below is a rendering made using this package.
![EM shower in the CMS HGcal](http://giant.gfycat.com/FickleHauntingHairstreak.gif)

## Installation
I'm working on getting this package on pip for easy installation. For the moment though, download this repository in a zip file, unzip it, and copy the Animator5D folder to the same directory as the program calling it. You can delete the SampleData folder if you want, as well, though it's nice to play around with. :P

Additionally, this package requires ImageMagick to render the frames into a single gif. Installation instructions (it's easy, I promise) can be found [here](http://www.imagemagick.org/script/binary-releases.php). If you don't have/want to install ImageMagick, you can still render the frames and combine them with some online gif maker using `animate(data, renderframes=False)`.

## Usage
This package is designed to be very easy to use, but also to allow you a full range of customization options. At the very least, you can simply use:
```python
from Animator5D import animate
animate(data)
```
Literally, that's it. 
The package will automatically calculate all of the needed quantitites simply from this statement. However, if you care about customizing the plot a bit more, you can configure the options with almost the same degrees of freedom as if you had coded the entire package yourself. Below is a list of the available options you can configure.

## Data structure
This code uses structured numpy arrays ([numpy.recarray](http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html)) as the data input. They are basically dictionaries with lists as their values, and I find them a very convenient way to work with complex data sets, rather than having to remember what order x, y, z, t, and w are in and enter them in that order. It is very easy to convert standard numpy arrays to numpy recarrays, by using [numpy.core.records.fromarrays](http://docs.scipy.org/doc/numpy/reference/generated/numpy.core.records.fromarrays.html).

In general, the data should consist of n number of "samples" containing an x, y, z, t, and w property each (you can configure what properties these go to). For example, a valid data set could be:
```python
array([ (49.29, -20.74, 339.42, 1.14, 1.05, 12.67, 1),
        (49.06, -20.06, 340.49, 1.19, 1.05, 12.73, 1)],
      dtype=[('x', '<f8'), ('y', '<f8'), ('z', '<f8'), ('RandomProperty1', '<f8'), 
            ('t', '<f8'), ('w','<f8'), ('RandomProperty2', '<i8')])
```
In this case, at most two frames could be plotted (two events), and it would use the variables x, y, z, t, and w in the plot, discarding `RandomProperty1` and `RandomProperty2`. You can also have different names for x, y, etc. by specifying `xname=<name>` in the `animate()` call.

In the program's `if __name__ == "__main__"` block, I've included two examples and their associated sample data files, with minimum and near maximum usage verbosity. Play around with them if you want.

## Documentation

Full list of parameters and usage (some non-boolean functions are initialized to a boolean value to indicate they should be automatically calculated):

    Usage:  Min. complexity:    animate(data)
            Max. complexity:    animate(data, title="Animator5D", path="Animator5D Rendering", tstep=False, 
                                    xname='x', yname='y', zname='z', wname='w', tname='t', 
                                    xlim=False, ylim=False, zlim=False, wlim=False, tlim=False, 
                                    xlabel='x', ylabel='y', zlabel='z', wlabel='w', tlabel='units', 
                                    projections=True, transparency=False, delete=False, quiet=False, 
                                    scalesize=True, msize=100, marker=",", renderframes=True)

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

