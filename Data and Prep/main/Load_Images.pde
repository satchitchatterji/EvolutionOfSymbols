PImage img;
int curFileInt = 1;
String curFile = "(1).jpg";

boolean checkValid() {
  return curFileInt > 0 && curFileInt < 39;
}

void loadNewImage() {
  reset();
  curFile = "("+str(curFileInt)+").jpg";
  img = loadImage(curFile);
  
  if(img.width < img.height){
    img.resize(0,maxDim);
  } else {
    img.resize(maxDim, 0);
  }
  println("\nImage "+curFile+" loaded!");
}

void next() {
  curFileInt++;
  if (!checkValid()) {
    println("End of list of images! Cannot move forward!");
    curFileInt = 38;
    return;
  }
  loadNewImage();
}
void back() {
  curFileInt--;
  if (!checkValid()) {
    println("Start of list of images! Cannot move backward!");
    curFileInt = 1;
    return;
  }
  loadNewImage();
}
