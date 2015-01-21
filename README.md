###Overview

This is a small traffic circut simulation using Pygame.  
Squares representing cars travel around a circut that meets in the middle over a bridge.  
The bridge under 'singleConstraint/circut.py' is used as a critical section under the following mutal exclusion rules:
1. Only one car on the bridge at time.
2. No car may be excluded from crossing. All cars must have a fair chance at crossing the bridge. 
3. If multiple cars are waiting to cross the bridge, they all must have a turn (queue).

Additionally there is no central mediation for the bridge constraint.  Each car sends messages to each other car 
for independant governance.  Even though the car objects are actually sharing the same memory they are logically 
seperate elements that send and receive messages, incidentally by shared memory.

The other source file is 'directionConstraint/circut.py'.  This is much like the previously described application, but 
the critical section (read: bridge) will allow multiple cars on the bridge if the following cars are travelling the 
same direction as the preceeding car that exists in the critical section (on the bridge).  

###Working it!
The applications were designed in an environment with python 2.7, and Pygame.  
With these in your path you should be able to simply copy, paste, run.  The velocity of each car can be increased 
with the keys {q,w,e,r} and decreased with {a,s,d,f}.  

###Demo
<a href="http://youtu.be/c1yVRJdhkXA" target="_blank"><img src="https://www.youtube.com/upload_thumbnail?v=c1yVRJdhkXA&t=hqdefault&ts=1421797793461" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

<a href="http://youtu.be/nHkTzj4LNUU" target="_blank"><img src="https://www.youtube.com/upload_thumbnail?v=nHkTzj4LNUU&t=hqdefault&ts=1421798304651" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>


###Note
The algorithm used for the distributed mutual exclusion is an implementation of Lamport's Algorithm.