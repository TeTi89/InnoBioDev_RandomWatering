# RandomWatering
## Table of Content
[roadmap](#roadmap)  
[TODO](#todo)  
[documentation](#documentation)  


## roadmap
- [find the best masking methode to process the images.](#image-masking)
- locat the plant pot, leaves
- meshing the image/coordinate
- give the instruction/coordinate to the watering programm
- create a scoring method to add a measure of uncertainty to the result so that help can be requested if the image taken by the cam is faulty.
- to speed up the image processing time, the program should be able to process a whole trace of pots from one image.

## TODO
- [x] create a project repository
  - [x] src: all jupyter notebooks
  - [x] data: all fotos taken from farmbot
  - [x] libs: all the libraries used or created
  - [x] docs: ducumentation
- [x] sort the fotos
  - [x] fotos with error
  - [x] fotos with warm light
  - [x] fotos with ideal conditions
  - [x] change file name

## documentation
### image masking
#### problems:
1. The photos were taken under different lighting conditions. Mainly in warm or cold light.
2. Some images cannot be displayed correctly. Part of the image consists of a monochrome block.
3. Almost all the pictures were taken too close to the object (in this case plants) so that the camera loses focus.
4. In most cases, the flower pots are not in the center of the picture. As a result, the circular shape of the flower pots is not fully depicted in the image area. This makes it difficult to recognize the circle. 
5. Many of the pictures showed more than just a flower pot.
6. Some flower pots are still equipped with sensors. The sensors must also be recognized. To prevent the sensors from being watered.
7. The flower pots used are in two different colors. Braun and black.

##### solution to problem 1
To solve this problem, we combine the advantages of two color spaces, HSV and LAB. Please refer to the notebook (Masking) for detailed processing steps.
##### solution to problem 2
We assume that each row of the image must be different from every other row. This assumption is reasonable because we are dealing with real-world objects that do not have perfect geometric shapes. So the algorithm to check the error image can be very simple and effective:  
We compare each row of pixels with the row below it. If the two rows have exactly the same value in the same order, we increment the counter by one. At the end, if the counter is more than a given threshold, we can say that the image is defect.
##### solution to problem 3
Images without proper focusing do not affect the recognition of the plants, because the moths use only the information of the colors.
But this will affect the recognition of flower pots, because the circle recognition relay on the recognition of edges. without clear edges the circle will not be properly recognized.
##### solution to problem 4
If the approximate coordinates of the pots can be provided, the Farmbot can move to a better location to take the photo.
##### solution to problem 5
open
##### solution to problem 6
Sensors must be colored with an easily recognizable color. A color that is not often found in nature.
##### solution to problem 7
need to be tested.
