# InnoBioDev_RandomWatering
## Table of Content
[roadmap](#roadmap)  
[TODO](#todo)  
[documentation](#documentation)  


## roadmap
- [find the best masking methode to process the images.](#image-masking)
- locat the plant pot, leaves
- meshing the image/coordinate
- give the instruction/coordinate to the watering programm

## TODO
- [x] create a project repository
  - [ ] src: all jupyter notebooks
  - [ ] data: all fotos taken from farmbot
  - [ ] libs: all the libraries used or created
  - [ ] docs: ducumentation
- [ ] sort the fotos
  - [ ] fotos with error
  - [ ] fotos with warm light
  - [ ] change file name

## documentation
### image masking
problems:
1. The photos were taken under different lighting conditions. Mainly in warm or cold light.
2. Some images cannot be displayed correctly. Part of the image consists of a monochrome block.
3. Almost all the pictures were taken too close to the object (in this case plants) so that the camera loses focus.
4. In most cases, the flower pots are not in the center of the picture. As a result, the circular shape of the flower pots is not fully depicted in the image area. This makes it difficult to recognize the circle. 
5. Many of the pictures showed more than just a flower pot.
6. Some flower pots are still equipped with sensors. The sensors must also be recognized. To prevent the sensors from being watered.
7. The flower pots used are in two different colors. Braun and black.

### solution to problem 2
We assume that each row of the image must be different from every other row. This assumption is reasonable because we are dealing with real-world objects that do not have perfect geometric shapes. So the algorithm to check the error image can be very simple and effective:  
We compare each row of pixels with the row below it. If the two rows have exactly the same value in the same order, we increment the counter by one. At the end, if the counter is more than a given threshold, we can say that the image is defect.