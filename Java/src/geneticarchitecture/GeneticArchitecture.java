package geneticarchitecture;

import processing.core.PApplet;
import peasy.*;

import static java.lang.System.out;

public class GeneticArchitecture extends PApplet {

	private int numberOfCreatures = 100;
	private PeasyCam cam;
	private Creature[] Creatures;
	private int creatureIndex = 0;

	@Override
	public void setup() {
		size(1024, 738, P3D);
		setCamera();
		
		this.Creatures = this.generateRandomCreatures(this.numberOfCreatures,20);
		
	    Fitness[] fitnessAlgorithms = {new FitnessEquilateral()};
	    Reproduction reproductionAlgorithm = new Reproduction();
	    
	    Evolution engine = new Evolution(this.Creatures);
	    
//	    for (int i=0 ; i<10 ;i ++){
//	    	engine.population = engine.reproduce(reproductionAlgorithm);
	    	engine.population = engine.fitness(fitnessAlgorithms, 12);
//	    }
	    
	   this.Creatures = engine.population;
	}
	
	public Creature[] generateRandomCreatures(int numberOfCreatures, int grow){
		Creature[] Creatures = new Creature[numberOfCreatures];
		for (int i=0; i<numberOfCreatures ; i++){
			
			Gene[] genes = new Gene[20];
			
			double[][] points= {
					{0,4,0},
					{4,0,0},
					{2,2,0},
					{2,2,4}
			};
			
			genes[0] = new Gene(points);;
		
			Creatures[i] = new Creature(genes);
			Creatures[i].grow(grow);
		}
		return Creatures;
	}

	@Override
	public void draw() {
		
		background(144);
		for (int i =0 ;i < this.Creatures.length ; i++){
			this.Creatures[i].render(this,i/4*40,i%4*40,0);
		}
	}
	
	private void setCamera() {
		cam = new PeasyCam(this, 500);
//		cam.setMinimumDistance(50);
//		cam.setMaximumDistance(500);	
	}
}
