### fetch-images.py
This script downloads a collection of image files from on a list of URL
locations and then stores them to a local directory. An `image-sources.txt`
file containing the list of URL locations must exist in the working directory
from where the script is being executed. To create a generic name for a
collection of images, a `rename` template must be added to the top of each
collection. A collection consists of the names of each image file separated by
a new line. If a URL in the `image-sources.txt` file does not have a template,
then the original URL file name will be used instead.

### Templates

+ `rename`: *filename*

  Renames each successive URL file name to *filename*. Repeating URLs will be
  enumerated with a number appended to *filename*. If *filename* contains an
  extension, then the number will be inserted after its base name. A recurrence
  of a `rename` template within the same `image-sources.txt` file can cause it
  to override and, thus, conflict with a prior declaration if they have the
  same *filename*.
+ `folder`: *dirpath*

  Specifies the local directory path, *dirpath*, where a file or collection
  should be saved. By default, if this template is not declared, then the
  current working directory will be used instead. The directory path can be
  either absolute or relative.

### Example `image-sources.txt` files

1. To generate a set of image files in the current working directory and
to retain their original file names:
```
http://www.site.com/circle.jpg
http://www.site.com/square.jpg
http://www.site.com/triangle.jpg
```

2. To assign a generic name to each file using the `rename` template:
```
rename: shape.jpg
http://www.site.com/circle.jpg
http://www.site.com/square.jpg
http://www.site.com/triangle.jpg
```
This will create the files *shape.jpg*, *shape-1.jpg*, and *shape-2.jpg*.

3. To redirect the output of each file to another directory using the `folder`
template:
```
folder: /path/to/a/directory
http://www.site.com/circle.jpg
http://www.site.com/square.jpg
http://www.site.com/triangle.jpg
```

4. To redirect to multiple directories and use multiple generic names:
```
rename: piece-of-cone.jpg
folder: /shapes/3d/cone
http://www.site.com/circle.jpg
http://www.site.com/triangle.jpg
  
rename: piece-of-cube.jpg
folder: /shapes/3d/cube
http://www.site.com/square.jpg
```
Note that it is possible to exclude the `rename` template from the first
collection of images (*circle.jpg* and *triangle.jpg*) so that they can retain
their original file names while only the second set, *square.jpg*, is renamed.
