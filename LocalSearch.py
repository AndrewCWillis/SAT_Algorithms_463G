# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 19:39:15 2022

@author: dreww
"""
import numpy as np
import time
import copy
from CNF_Parser import Parser

class LocalSearch:
    def __init__(self): 
        self.clauses = [] #list of lists
        
        self.lit_dict = {} # a mapping of literals to (pointer) the clauses that contain them
        self.num_literals = 0
     
    def applyAssignments(self, truth_assignment, clauses):
        
        for i, key in enumerate(self.lit_dict):
            if truth_assignment[i]:
                clauses = self.literalSet(key, clauses)
            else:
                clauses = self.literalSet(int(-1 * key), clauses)
        
        return clauses 
    
    def setFirstAssignments(self, num_literals):
        
        truth_assignment = [np.random.randint(0,2) for i in range(1,num_literals + 1)]
        
        return truth_assignment
    
    def literalSet(self, literal, clauses):
        # for the return statement in the dpll alg 
        # will set literal = True or False in each clause
          
        negation = literal
        negation *= -1
        temp = []
        for clause in clauses:
            
            if literal in clause: #look at dictionary to find the clauses that contain this literal
                
                temp.append(clause)
                
            if negation in clause:
                
                clause.remove(-1 * literal)
                
        for clause in temp:
            clauses.remove(clause)    
        return clauses
    
    def getFitness(self, clauses):
        return int(len(self.clauses) - len(clauses))
    
    def getChildren(self, clauses):
        return set(literal for clause in clauses for literal in clause)
    def findImprovingNeigbhor(self, clauses, assignments, curr_fitness):
        neighbor_fitness = 0
        improved_i = -1
        improved_f = -1
        
        for i in range (0, len(assignments)):
            assignments[i] = assignments[i] ^ 1 # toggle a bit
            neighbor_fitness = self.getFitness(self.applyAssignments(assignments, copy.deepcopy(clauses)))
            assignments[i] = assignments[i] ^ 1 #undo
            
            if curr_fitness < neighbor_fitness:#take first improvement and run
                improved_i = i
                improved_f = neighbor_fitness
                break
 
        return improved_i, improved_f
    
    def localSearch(self, clauses):
        assignment = self.setFirstAssignments( self.num_literals)
        first_guess = self.applyAssignments(assignment, copy.deepcopy(clauses))
        fitness = self.getFitness(first_guess)
        
        #print(f'FITNESS OF FIRST GUESS: {fitness}/{len(self.clauses)}')
        
        while fitness != len(self.clauses):
            literal_flipped, next_fitness = self.findImprovingNeigbhor(self.clauses, assignment, fitness)
            assignment[literal_flipped] = assignment[literal_flipped] ^ 1
            clauses = self.applyAssignments(assignment, copy.deepcopy(self.clauses))
            if next_fitness ==  len(self.clauses):
                #print('SUCCESS!')
                return fitness, assignment
            elif next_fitness <= fitness:
                #print('FAIL :(')
                return fitness, assignment
            else:
                fitness = next_fitness
                
        return fitness
    
def main():
    
    parser = Parser('PA3_Benchmarks/HARD CNF Formulas', '.cnf')
    
    while parser.last_evaluated < len(parser.files):
        num_literals, clauses, lit_dict, found_assignments, filename = parser.parseNext()
        for _ in range(1):
            start_time = time.time()
            sat = LocalSearch()
            sat.num_literals = num_literals
            sat.clauses = copy.deepcopy(clauses)
            sat.lit_dict = lit_dict
            sat.found_assignments = found_assignments
            fitness, assignment = sat.localSearch(sat.clauses)
            end_time = time.time() - start_time
            if fitness == len(clauses):
                break
        print(f'Result of Local Search on {filename}: FITNESS = {fitness} / {len(sat.clauses)}. Time: {end_time}')
     
if __name__ == "__main__":
    main()