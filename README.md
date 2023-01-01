# Ping data analytics 
 This is python code written for the user to conduct analysis on ping variance of separate game channels for game server of interest. In this case, this scrapes the instantaneous ping data of a Maplestory ping github page multiple times to plot and study.


For the sake of brevity, I have only made 2 versions of my code available for personal use. 

1. A variance filter test available in the file Pingfinder.py. It takes all the ping values of the channels, and it plots the channels' pings per sample (number which you the user set yourself at your own discretion) that are below the user's chosen variance upper limit

2. A longer term stability list test available in the file stability.py. This one asks for 2 inputs as well like the first one. The first one is number of pings as the first one would ask, and the second one, is the norm value (any positive number) you wish to choose. The higher the norm value, the harder you are essentially penalising a channel for having rare, but huge spikes in ping. This is a piece of code I would run for a few hours if I ever wanted to find my "secret prime channels" for toteming. 

Please take note however, that the user should seek to determine for themselves what actually constitutes a "prime" channel. For now, we only hypothesize that channels with huge ping spikes are channels that tend to cause dcs. We also think that channels that sometimes show 0ms ping are very likely a hard on dc. But we could be very much wrong, and that is ok. That is why we wish to have more people to interpret the results themselves. At the end of the day, most of this data is hard data that shows you the channel pings for you to decide what channels are good, without necessarily YOLOing it. So without further ado, let us get into how to get this to work!

--------------------------------------------- 


### Intention
(Explained in simple layman terms...)

Refreshing this page allows you to see your own instantaneous ping at any point in time, and some of you might even be thinking, "well then I would only care about the ping value I see on this page at this instant, no?!".

And you would be right, if ping maintained its own value over time in each channel. If Channel 4 always had the lowest ping consistently versus the other channels, that would be true. And it does, on average. However, I are very certain that average ping does not determine the quality of a channel, the ping variance also is a significant factor. In simpler terms, how squiggly or how much the ping value of a channel spikes up or drops down arbitrarily is a significant factor that can affect how consistently you can utilise and time your skills. 

--------------------------------------------- 

## Execution | Pingfinder.py


Below is a example execution for 100 ping samples from Singapore executed at about 1:41am, which took about 40min to execute in total. On one hand, it could be argued that a quicker execution would be advantageous. However, the lengthier time period in which this ping data is gathered is a more sincere extraction of the troughs and peaks of channels' pings and their variances, which was the impetus of the client's desire for ping analysis. A future implementation of this with a low level language in an attempt to speed up this process may regardless, be attempted.


![Channels out of 1-30 for maplestory that showed below 150 standard deviation](https://user-images.githubusercontent.com/100022747/210152841-daf7dcab-dcfe-49da-8c78-f4f2481f2831.png)


Only channels 1-4 demonstrated a standard deviation below 150 as requested by the user in this example, so only the ping data of those 4 channels were plotted in this output.
