# inflation_py 
An implementation of inflation from silhouettes in python.
Generate a height/depth map and a mesh from a single silhouette.
No machine learning is included.

# Run
`python inflation.py` generates sample outputs.

OpenCV, numpy and scipy are required as dependencies.

# Sample inputs and outputs
- Input
  - A single silhouette (mask) image
- Output
  - a depth/height map (colorized) and a mesh in .ply format (its shaded rendering is shown in the table below)

|Input silhouettes|<img src="./data/circle.png" width="128">|<img src="./data/square.png" width="128">|<img src="./data/A.png" width="128">|<img src="./data/hiragana.png" width="128">|<img src="./data/character.png" height="128">|
|---|:---:|:---:|:---:|:---:|:---:|
|Distance Transform|<img src="./data/visualized_depth/circle_dist.jpg" width="128"> <img src="./data/screenshots/circle_dist.jpg" width="128">|<img src="./data/visualized_depth/square_dist.jpg" width="128"> <img src="./data/screenshots/square_dist.jpg" width="128">| <img src="./data/visualized_depth/A_dist.jpg" width="128"> <img src="./data/screenshots/A_dist.jpg" width="128">|<img src="./data/visualized_depth/hiragana_dist.jpg" width="128"> <img src="./data/screenshots/hiragana_dist.jpg" width="128">|<img src="./data/visualized_depth/character_dist.jpg" width="128"> <img src="./data/screenshots/character_dist.jpg" width="128">|
|Distance Transform + Activation (tanh)|<img src="./data/visualized_depth/circle_dist_tanh.jpg" width="128"> <img src="./data/screenshots/circle_dist_tanh.jpg" width="128">|<img src="./data/visualized_depth/square_dist_tanh.jpg" width="128"> <img src="./data/screenshots/square_dist_tanh.jpg" width="128">|<img src="./data/visualized_depth/A_dist_tanh.jpg" width="128"> <img src="./data/screenshots/A_dist_tanh.jpg" width="128">|<img src="./data/visualized_depth/hiragana_dist_tanh.jpg" width="128"> <img src="./data/screenshots/hiragana_dist_tanh.jpg" width="128">|<img src="./data/visualized_depth/character_dist_tanh.jpg" width="128"> <img src="./data/screenshots/character_dist_tanh.jpg" width="128">|
|Baran's method|<img src="./data/visualized_depth/circle_baran.jpg" width="128"> <img src="./data/screenshots/circle_baran.jpg" width="128">|<img src="./data/visualized_depth/square_baran.jpg" width="128"> <img src="./data/screenshots/square_baran.jpg" width="128">|<img src="./data/visualized_depth/A_baran.jpg" width="128">  <img src="./data/screenshots/A_baran.jpg" width="128">|<img src="./data/visualized_depth/hiragana_baran.jpg" width="128"> <img src="./data/screenshots/hiragana_baran.jpg" width="128">|<img src="./data/visualized_depth/character_baran.jpg" width="128"> <img src="./data/screenshots/character_baran.jpg" width="128">|

# Algorithm
## Distance Transform (+ Activation)
Based on distance transform that computes distance from silhouette edges to pixels in the silhouette.
This method tends to cause steepy surfaces.
Additioanlly, you can set activation function to operate steepness but it is difficult to control.

## Baran's method
Based on Poisson's equation.
Implementation of the following paper:
"Notes on Inflating Curves" [Baran and Lehtinen 2009](http://alecjacobson.com/weblog/media/notes-on-inflating-curves-2009-baran.pdf).
This method generates smooth surfaces considering gradient space.
Especially, a circle silhouette becomes a hemisphere mesh.
