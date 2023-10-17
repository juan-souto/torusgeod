   What this thing does is basically the following: calculate a few things for closed geodesics in the 
punctured torus and then use them to "visualize" some math theorems. 

   Basically what it computes are things like length for a given hyperbolic structure and intersection number, 
calculates the systoles of a punctured torus and estimates where in Teichmueller space is the length function
of a (filling) curve minimized. This last thing is done via gradient descent and it is surprisingly unprecise,
maybe suggesting that the length functions of curves are less convex than one thinks. Or maybe suggesting that
my implementation of gradient descent is not very good...

   With those pretty limited tools it does a couple of more or less interesting things. For example you can draw 
a heat map of the systole function (that actually looks cool), you can see how the size of the homology changes 
when you take a sequence of geodesics obtained by following a random ray for some time and then closing up (as
expected it looks like a random walk), or it makes you "listen" to a geodesic, making clear that you can
distinguish between random geodesics, random words in pi_1 and randomly chosen simple geodesics.

   If I have enough drive, I might at some point write a little math text about these things. 

   Cheers,

   Juan

   P.S.: The dist foldet contains a version executable under windows. For other operating systems you need to 
      compile the file "main.py". You might need to add some packages to your python distribution.
