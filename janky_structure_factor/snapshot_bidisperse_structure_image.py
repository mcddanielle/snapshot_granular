#!/usr/bin/python

"""snapshot_bidisperse.py
Danielle McDermott
July 5, 2017

This is a powerful approach to making movies 
since it calls a function with arguments and does the looping itself

I can use the ffmpeg concatenate functions 
to combine mp4 (or other same codec formats) 
as long as they have the same framerate 
which seems to be a "no duh" to everyone except me.

However, I can't seem to convince the writer to insert a timed delay
between calls, which I would really like 
so that I may use "slow motion" during the interesting parts.
look up kwargs=interval, duration, etc
and see what I'm missing.  Something is going on here.
"""

import matplotlib

matplotlib.use('Agg')   #for batch jobs!!!

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#from matplotlib import cm
from matplotlib import colors
import sys, os
import numpy as np

from pylab import draw

#functions written by D.M. to get and plot specific data files
import data_importerDM as di
#import classColloid.plotColloid as plotColloid
#import command_line_args

################################################################
################################################################
################################################################


################################################################
################################################################
################################################################
#---------------------------------------------------------------
#nominal main plotting ingredients------------------------------
#---------------------------------------------------------------

#get and parse information that allows us to make the movie
#this is hardcoded, which is ugly
#want these variables to be globals to work with the animation subroutine
def get_input_data(filename):
    '''
    hardcoded to look for two particular types of files
    will exit if it does not get

    filename: Pa0 or Pd0
    '''

    if filename == "Pa0" or "Pd0":

        print("Reading movie making parameters from: %s"%(filename))

        try:
            #data is traditionally placed in a two column file
            #with a string/number format, where number is integer or float

            #make an empty list to hold data as strings
            input_data_strings = []
            for data in di.import_text(filename,' '):
                #print(data)
                input_data_strings.append(data)
                
        except:
            print("File read error")
            sys.exit()

        
    else:
        print("Code is not written to understand your input file")
        print("Either hardcode your parameters or write a new subroutine")
        sys.exit()
        
    if filename == "Pa0":

        #print(input_data_strings) #= di.get_data(file,2,sep=' ')
        density = float(input_data_strings[0][1])
        pdensity = float(input_data_strings[1][1])
        Sx = [0,float(input_data_strings[2][1])]
        Sy = [0,float(input_data_strings[3][1])]
        radius = float(input_data_strings[4][1])
        runtime = int(input_data_strings[5][1])
        runforce = float(input_data_strings[6][1])
        dt = float(input_data_strings[7][1])
        maxtime = int(input_data_strings[8][1])
        writemovietime = int(input_data_strings[9][1])
        kspring = float(input_data_strings[10][1])
        lookupcellsize = float(input_data_strings[11][1])
        potentialrad = float(input_data_strings[12][1])
        potentialmag = float(input_data_strings[13][1])
        lengthscale = float(input_data_strings[14][1])
        drivemag = float(input_data_strings[15][1])
        drivefrq = float(input_data_strings[16][1])
        decifactor = int(input_data_strings[17][1])


        
        return(density, Sx, Sy, radius )

    else:
        print("TBD")
        sys.exit()

#################################################################
#################################################################
#################################################################
def plot_particles(xp,yp,radius,ax,Sx=60.0,Sy=60.0):
    '''
    i:  integer "frame number"
    ax: matplotlib object pointer to plot data on
    '''


    #hardcode the particle plotting size.
    #This is markedly different than the simulation since this is a pixel size
    #could improve this by calculating a more precise value
    size=50

    #this is one subroutine in D.M.'s plotting library
    #meant to make scatter plots
    #see the documentation there, it is very detailed.

    
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['red', 'cornflowerblue'])

    scatter1=ax.scatter(xp,yp,c=radius,s=radius*size,edgecolor='k',
                        cmap=cmap)
        
    ax.set_xlabel("X",fontsize=22)
    ax.set_ylabel("Y",fontsize=22)
    ax.set_ylim(0,Sx) 
    ax.set_xlim(0,Sy)
    
    return 


#################################################################
def add_sk_image(ax,file_name="testplot2.png",dir_name=None):

    #get s(k) image
    if dir_name:
        image_file = dir_name+'/'+file_name
    else:
        image_file=file_name
    image = plt.imread(image_file)

    ax.set_aspect('equal')
    ax.imshow(image)       #plot image
    ax.axis('off')         # clear x- and y-axes
    ax.set_xlabel('S(k)')  #turned off

    return

#################################################################
#################################################################
def plot_histogram(data,ax,edgecolor="k",orientation="vertical",bins1=40,cum_boolean=False):

    weights=np.ones_like(data)/len(data)
    (n,bins,patches)=ax.hist(data,bins1,
                              weights=weights, orientation=orientation,
                              histtype='step',
                              edgecolor=edgecolor,facecolor=None,
                              cumulative=cum_boolean)

    return
#################################################################
#Okay, define plot and add data
#################################################################
if __name__ == "__main__":

    ################################################
    #get any command line args, NOT CURRENTLY USING
    ################################################
    if 0:
        (inputfile,outputfile) = command_line_args.get_command_args(sys.argv[1:])

    #HARDCODE THESE INSTEAD
    inputfile="Pa0"
    output_file="scatter.png"

    
    ################################################
    #get a bunch of data from the input file
    #we actually use very little of this
    #so you could change it how you would like to
    ################################################
    if 0:
        (density, Sx, Sy, small_radius ) = get_input_data(inputfile)

    ################################################
    #the user may change the follwing values at will,
    #they are nominially set by the original simulation
    #whose data was generated from Pa0
    ################################################


    ###############################################################
    #Figure parameters -- defines the matplotlib pointer to plot on
    ###############################################################

    columns = 2
    rows = 1

    #make a matplotlib object to plot to
    fig = plt.figure(figsize=(6.0*columns,6.0*rows),
                     num=None, facecolor='w', edgecolor='k')

    #a little convoluted, here we are using a single subplot
    #but could easily extend to a multiplot using this formalism
    G = gridspec.GridSpec(rows, columns)

    #leave room for subplotting
    ax1 = fig.add_subplot(G[0])
    ax2 = fig.add_subplot(G[1])

    #hardcode the data filename, could clean this up
    data_file = "velocity_data/XV_data_t=04500000"
    number_columns=8
    path1=os.getcwd()
    
    data_list=di.get_data(data_file,number_columns,sep=" ",path1=path1)

    x_particle = np.array(data_list[2])
    y_particle = np.array(data_list[3])
    #vx         = np.array(data_list[4])
    #vy         = np.array(data_list[5])
    radius     = np.array(data_list[6])
    #speed      = data_list[7]

    force_file = "force_distribution.dat"
    number_columns2=4
    data_list2=di.get_data(force_file,number_columns2,sep=" ",path1=path1)

    vx = np.array(data_list2[0])
    vy = np.array(data_list2[1])
        
    #ax 1: scatter plot of particles
    plot_particles(x_particle,y_particle,radius,ax1,Sx=60.0,Sy=60.0)
    
    
    ######################################################
    #ax 2: structure factor
    ######################################################

    if 0:
        #if you were going to plot histograms:
        
        plot_histogram(vx1, ax2, edgecolor='cornflowerblue')
        plot_histogram(vx2, ax2, edgecolor='red')

    else:
        file_name="testplot2.png"
        add_sk_image(ax2,file_name )


    
    fig.tight_layout()

    fig.savefig(output_file)
    
    sys.exit()




