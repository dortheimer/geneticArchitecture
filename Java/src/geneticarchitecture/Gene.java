package geneticarchitecture;

import processing.core.PShape;
import java.util.Arrays;

public class Gene extends PShape{
	
	protected double[][] points;
	
	protected PShape shape;
	
	/**
	 * Constructor to get optional points
	 * @param points 2d array with points 4 * { x,y,z}
	 */
	Gene(double[][] points) {
		if (points!=null){
			this.points = points;	
		}
		else {
			this.generateRandom();
		}
		
	}
	
	public void generateRandom(){
			this.points = new double[][]{
				{this.getRandInt(-4,4),this.getRandInt(-4,4),this.getRandInt(-4,4)},
				{this.getRandInt(-4,4),this.getRandInt(-4,4),this.getRandInt(-4,4)},
				{this.getRandInt(-4,4),this.getRandInt(-4,4),this.getRandInt(-4,4)},
				{this.getRandInt(-4,4),this.getRandInt(-4,4),this.getRandInt(-4,4)}
		};
	}
	/**
	 * randomize points location.
	 * @return
	 */
	
	protected int getRandInt(int Min,int Max) {
		return Min + (int)(Math.random() * ((Max - Min) + 1));
	}
	
	protected double getRandFloat(int Min,int Max) {
		return Min + (Math.random() * ((Max - Min) + 1));
	}
	
	/**
	 * Get number of points
	 * @return
	 */
	public int size() {
		return this.points.length;
	}
	
	public Gene grow () {
		int removeIndex = this.getRandInt(0, this.points.length-1); 
		double[][] planePts = new double[4][3];
		int j=0;
		for (int i=0 ; i<this.size(); i++){
			if (i != removeIndex){
				planePts[j] = this.points[i];
				j++;
			}
		}
		
		double[] planeCenter = this.findCenter(planePts);
		double[] opposite = {
			2*planeCenter[0]-this.points[removeIndex][0],
			2*planeCenter[1]-this.points[removeIndex][1],
			2*planeCenter[2]-this.points[removeIndex][2]};
		double[] point = {
			opposite[0]+this.getRandFloat(-2, 2) ,
			opposite[1]+this.getRandFloat(-2, 2) ,
			opposite[2]+this.getRandFloat(-2, 2)};

		planePts[3] = point;
		return new Gene(planePts);
	}
	
	protected double[] findCenter(double[][] planePts){
		int x, y, z;
		x = y = z= 0;
		int l = planePts.length;
		
		for (int i = 0 ; i<l ;i ++){
			x+= planePts[i][0];
			y+= planePts[i][1];
			z+= planePts[i][2];
		}
		return new double[] {x/l, y/l, z/l};
	}
	
	
	public Gene render (GeneticArchitecture ppaplet, double locX , double locY,double locZ) {
		shape = ppaplet.createShape();
		shape.beginShape();
		
		shape.fill(255,255,255);
//		shape.noStroke();
		for (int i=0; i<this.points.length; i++){
			shape.vertex(
					(float)(this.points[i][0]+locX),
					(float)(this.points[i][1]+locY),
					(float)(this.points[i][2]+locZ));	
		}
		
		shape.endShape(CLOSE);
		ppaplet.shape(shape, 25, 25);
//		
//
//	
//		 polyline = rs.AddPolyline([
//		                            [self.points[0][0] + offsetX, self.points[0][1] + offsetY, self.points[0][2] + offsetZ],
//		                            [self.points[1][0] + offsetX, self.points[1][1] + offsetY, self.points[1][2] + offsetZ],
//		                            [self.points[2][0] + offsetX, self.points[2][1] + offsetY, self.points[2][2] + offsetZ],
//		                            [self.points[0][0] + offsetX, self.points[0][1] + offsetY, self.points[0][2] + offsetZ]])
//		                        point = [self.points[3][0] + offsetX, self.points[3][1] + offsetY, self.points[3][2] + offsetZ]
//		                        solid = rs.ExtrudeCurvePoint( polyline, point )
//		                        rs.DeleteObject(polyline)
//
//		                        # cup
//		                        # bool union
//		                        return solid
		return this; 
	}
	
	public String sig() {
		String sig = "";
		for (int i=0 ;i<this.points.length ; i++){
			sig += Arrays.toString(this.points)+" ";
		}
		
		return sig;
	}
}

