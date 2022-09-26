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
    def findImprovingNeigbhor(self, clauses, assignments):
        neighbor_fitness = []
        
        for i in range (0, len(assignments)):
            new_assignment = copy.deepcopy(assignments)
            new_assignment[i] = new_assignment[i] ^ 1 # toggle a bit
            neighbor_fitness.append(self.getFitness(self.applyAssignments(new_assignment, copy.deepcopy(clauses))))
 
        return neighbor_fitness.index(max(neighbor_fitness)), max(neighbor_fitness)
    
    def localSearch(self, clauses):
        assignment = self.setFirstAssignments( self.num_literals)
        first_guess = self.applyAssignments(assignment, copy.deepcopy(clauses))
        fitness = self.getFitness(first_guess)
        
        #print(f'FITNESS OF FIRST GUESS: {fitness}/{len(self.clauses)}')
        
        while fitness != len(self.clauses):
            literal_flipped, next_fitness = self.findImprovingNeigbhor(self.clauses, assignment)
            assignment[literal_flipped] = assignment[literal_flipped] ^ 1
            clauses = self.applyAssignments(assignment, copy.deepcopy(self.clauses))
            
            if next_fitness ==  len(self.clauses):
                print('SUCCESS!')
                return fitness, assignment
            elif next_fitness <= fitness:
                print('FAIL :(')
                return fitness, assignment
            else:
                fitness = next_fitness
                
        return fitness
    
def main():
    
    parser = Parser('PA3_Benchmarks\CNF Formulas', '.cnf')
    
    while parser.last_evaluated < len(parser.files):
        sat = LocalSearch()
        sat.num_literals, sat.clauses, sat.lit_dict, sat.found_assignments, filename = parser.parseNext()
        fitness, assignment = sat.localSearch(copy.deepcopy(sat.clauses))
        print(f'Result of Local Search on {filename}: FITNESS = {fitness} / {len(sat.clauses)}, assignments = {assignment}')
     
if __name__ == "__main__":
    main()