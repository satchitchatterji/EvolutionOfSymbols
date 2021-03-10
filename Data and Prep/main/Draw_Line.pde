PVector[] refLine = new PVector[2];
boolean drawLine = false;
void reset(){
  drawLine=false;
  refLine[0].x = 0;
  refLine[0].y = 0;
  refLine[1].x = 0;
  refLine[1].y = 0;
}
void drawPoints(){
  fill(0,255,0);
  if(refLine[0].mag()!=0){
    circle(refLine[0].x, refLine[0].y, 2.5);
  } 
  if(refLine[1].mag()!=0){
    circle(refLine[1].x, refLine[1].y, 2.5);
  }
}
void drawLine(){
  if(drawLine){
    line(refLine[0].x, refLine[0].y, refLine[1].x, refLine[1].y);
  }
}
