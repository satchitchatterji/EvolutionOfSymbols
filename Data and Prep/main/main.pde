//loop
//  import image
//  draw two points
int maxDim = 1000;
void setup() {
  for (int i = 0; i<refLine.length; i++) {
    refLine[i] = new PVector(0, 0);
  }
  loadNewImage();
  strokeWeight(2);
  stroke(255);

  size(1000, 1000);
}
void draw() {
  background(0);
  image(img, 0, 0);
  drawLine();
  drawPoints();
}
void keyPressed() {
  if (key == 'r') {
    reset();
    println("Reset!\n");
  }
  if (key == 'n') {
    next();
  }
  if (key == 'b') {
    back();
  }
}

void mousePressed() {
  if (refLine[0].mag()==0) {
    refLine[0] = new PVector(mouseX, mouseY);
    println("\nPoint 1: ", mouseX, mouseY);
  } else if (refLine[1].mag()==0) {
    refLine[1] = new PVector(mouseX, mouseY);
    println("Point 2: ", mouseX, mouseY);  
    drawLine=true;
    println("Distance: ", dist(refLine[0].x, refLine[0].y, refLine[1].x, refLine[1].y));
  } else {
    reset();
  }
}
