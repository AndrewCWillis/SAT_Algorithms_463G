# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 16:53:34 2022

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
        self.map = {}
        self.new_clauses = None
        
    def new_data_structs(self):
        self.new_clauses = [False for _ in range(len(self.clauses))]
        
        for lit in self.lit_dict:
            pos = []
            neg = []
            negation = lit
            negation *= -1
            for clause in self.lit_dict[lit]:
                if lit in clause:
                    pos.append(self.clauses.index(clause))
                elif negation in clause:
                    neg.append(self.clauses.index(clause))
                    
            self.map[lit] = pos
            self.map[negation] = neg
        
                
    def applyAssignments(self, truth_assignment, clauses):
        
       
        for i, key in enumerate(self.lit_dict):
            if truth_assignment[i]:
                clauses = self.literalSet(key, True, clauses)
            else:
                clauses = self.literalSet(key, False, clauses)
        
        return clauses
    
    def setFirstAssignments(self, num_literals):
        
        truth_assignment = [np.random.randint(0,2) for i in range(1,num_literals + 1)]
        
        return truth_assignment
    
    def literalSet(self, literal, truth, clauses):
        # for the return statement in the dpll alg 
        # will set literal = True or False in each clause
          
        if truth:
            for index in self.map[literal]:
                clauses[index] = True
        else:
            neg = literal
            neg *= -1
            for index in self.map[neg]:
                clauses[index] = True
                
        return clauses
    
    def getFitness(self, clauses):
        return clauses.count(True)
    
    def getChildren(self, clauses):
        return set(literal for clause in clauses for literal in clause)
    
    def findImprovingNeigbhor(self, assignments, curr_fitness):
        neighbor_fitness = 0
        improved_i = -1
        improved_f = -1
        
        for i in range (0, len(assignments)):
            assignments[i] = assignments[i] ^ 1 # toggle a bit
            
            neighbor_fitness = self.getFitness(self.applyAssignments(assignments, [False for _ in range(len(self.clauses))]))
            
            assignments[i] = assignments[i] ^ 1 #undo
            
            if curr_fitness < neighbor_fitness:#take first improvement and run
                improved_i = i
                improved_f = neighbor_fitness
                break
    
        return improved_i, improved_f
    
    def localSearch(self, clauses):
        assignment = self.setFirstAssignments(self.num_literals)
        first_guess = self.applyAssignments(assignment, [False for _ in range(len(self.clauses))])
        fitness = self.getFitness(first_guess)
        
        print(f'FITNESS OF FIRST GUESS: {fitness}/{len(self.clauses)}')
        
        while fitness != len(self.clauses):
            
            literal_flipped, next_fitness = self.findImprovingNeigbhor(assignment, fitness)
            
            if literal_flipped != -1:
                assignment[literal_flipped] = assignment[literal_flipped] ^ 1
            clauses = self.applyAssignments(assignment, [False for _ in range(len(self.clauses))])
            
            #print(self.new_clauses)
            if next_fitness ==  len(self.clauses):
                #print('SUCCESS!')
                #print(clauses)
                return fitness, assignment
            elif next_fitness <= fitness:
                #print('FAIL :(')
                #print(clauses)
                return fitness, assignment
            else:
                fitness = next_fitness
                
            #print(f'FITNESS OF NEXT GUESS: {next_fitness}/{len(self.clauses)}')
            #print(f'LITERAL FLIPPED: {literal_flipped + 1} to {assignment[literal_flipped]}. affected: {self.map[literal_flipped + 1]}, {self.map[-1 * (literal_flipped + 1)]}')
                
        return fitness, assignment
    
def main():
    
    parser = Parser('PA3_Benchmarks/CNF Formulas', '.cnf')
    #parser = Parser('PA3_Benchmarks/HARD CNF Formulas', '.cnf')
    begin = time.time()
    while parser.last_evaluated < len(parser.files):
        num_literals, clauses, lit_dict, found_assignments, filename = parser.parseNext()
        fitness = 0
        assignment = None
        start_time = time.time()
        end_time = 0.0
        #print(num_literals)
        for _ in range(500):
            
            sat = LocalSearch()
            sat.num_literals = num_literals
            sat.clauses = copy.deepcopy(clauses)
            sat.lit_dict = lit_dict
            sat.found_assignments = found_assignments
            
            sat.new_data_structs()
            fitness, assignment = sat.localSearch(sat.clauses)
            if fitness == len(clauses):
                break
            
        end_time = time.time() - start_time
        print(f'Result of Local Search on {filename}: FITNESS = {fitness} / {len(sat.clauses)}. Time: {end_time}')
        
    total = time.time() - begin
    print(f'Total Time: {total}')
if __name__ == "__main__":
    main()