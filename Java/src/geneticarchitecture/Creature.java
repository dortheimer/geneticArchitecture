package geneticarchitecture;
import static java.lang.System.out;

import java.util.Arrays;
import java.util.Comparator;

public class Creature implements Comparable<Creature>{
	
	protected Gene[] genes;
	protected Gene[] renderedGenes;
	protected int geneIndex = 0;
	public double score;
	
	public Creature(Gene[] genes){
		this.genes = genes;
	}
	
	public void grow(int size) {
		for (int i=0;i<size-1; i++){
			if (this.genes[i]!=null){
				
			}
			else {
				this.genes[i] = this.genes[i-1].grow();
			}
		}
	}
	
	public boolean render(GeneticArchitecture ppaplet, double locX , double locY,double locZ) {
		for (int i=0; i<this.genes.length-1;i++){
			this.genes[i].render(ppaplet, locX , locY,locZ);
		}
		return true;
	}   
	
	public String sig() {
		String sig = "";
		for (int i=0 ;i<this.genes.length ; i++){
			if (this.genes[i]!=null){
				sig += this.genes[i].sig();
			}
		}
		
		return sig;
	}
	
	public int compareTo(Creature enemy) {
		return (int) (this.score - enemy.score);
	}	
	
	public static Comparator<Creature> CreatureComparator = new Comparator<Creature>() {

		public int compare(Creature creature1, Creature creature2) {
		
		
			//ascending order
			return creature1.compareTo(creature2);

		}

	};
}
