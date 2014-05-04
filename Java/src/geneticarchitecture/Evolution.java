//	# The MIT License (MIT)
//	#
//	# Copyright (c) 2014 Jonathan Dortheimer
//	#
//	# Permission is hereby granted, free of charge, to any person obtaining a copy
//	# of this software and associated documentation files (the "Software"), to deal
//	# in the Software without restriction, including without limitation the rights
//	# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//	# copies of the Software, and to permit persons to whom the Software is
//	# furnished to do so, subject to the following conditions:
//	#
//	# The above copyright notice and this permission notice shall be included in
//	# all copies or substantial portions of the Software.
//	#
//	# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//	# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//	# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//	# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//	# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//	# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
//	# THE SOFTWARE.

package geneticarchitecture;
import java.util.Arrays;

public class Evolution {

	public Creature[] population;
	
	Evolution(Creature[] population){
		this.population = population;
	}
	
	public Creature[] fitness(Fitness[] fitnessAlgorithms, int creatureLimit){

	        double[] fintnessScore = new double[this.population.length];
	        
	        for (int i=0; i<this.population.length; i++ ){
	        	int score = 0;
	        	for (int j=0; j<fitnessAlgorithms.length; j++){
	        		score+= fitnessAlgorithms[j].score(this.population[i]);
	        	}
	        	this.population[i].score = score;
	        }
	        
	        Arrays.sort(this.population, Creature.CreatureComparator);
	        Creature[] topCreatures = Arrays.copyOfRange(this.population, 0, creatureLimit);
	        return topCreatures;
	}
	
	public Creature[] reproduce(Reproduction reproductionAlgorithm){
	        Creature[] newCreatures = new Creature[this.population.length^2];

			for (int i=0; i<this.population.length; i++){
				for (int j=0; i<this.population.length; j++){
					newCreatures[(i*j)] = reproductionAlgorithm.mitosis(this.population[i], this.population[j]);
					
				}
			}
			return newCreatures;
}
}
