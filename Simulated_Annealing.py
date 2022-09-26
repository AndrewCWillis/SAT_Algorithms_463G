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
        self.max_temp = 0.3
        self.min_temp = 0.01
        self.steps = 0
        self.deacyRate = 0
    
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
    
    def currentTemperature(self):
        return (self.max_temp * (2**(-1 * self.steps)*self.decayRate))
    
    def probability_i(self, literal, current_fitness, assignments):
        new_assignment = copy.deepcopy(assignments)
        new_assignment[literal] = new_assignment[literal] ^ 1
        new_clauses = self.applyAssignments(new_assignment, copy.deepcopy(self.clauses))
        new_fitness = self.getFitness(new_clauses)
        delta = current_fitness - new_fitness
        temp = self.currentTemperature()
        
        try:# for really small numbers that could overflow
            prob = 1 / (1 + 2**((delta) / temp))
        except:
            prob = 0
        return prob, new_assignment, new_fitness
    
    def localSearch(self, clauses):
        assignment = self.setFirstAssignments( self.num_literals)
        first_guess = self.applyAssignments(assignment, copy.deepcopy(clauses))
        fitness = self.getFitness(first_guess)
        print(f'CURRENT TEMPERATURE: {self.currentTemperature()}')
        #print(f'FITNESS OF FIRST GUESS: {fitness}/{len(self.clauses)}')
        
        while fitness != len(self.clauses):
            
            #print(f'CURRENT ASSIGNMENTS: {assignment}')
            
            for i, literal in enumerate(self.lit_dict):
                prob, new_assignment, new_fitness = self.probability_i(i, fitness, assignment)
                prob *= 100

                choice = np.random.randint(0, 101)
                if choice < prob:
                    #print(f'Changed literal {literal} with probability {prob}. FITNESS: {new_fitness}')
                    fitness = new_fitness
                    assignment = new_assignment
            #print(f'CURRENT FITNESS: {fitness}')
            if self.currentTemperature() < self.min_temp:
                return fitness, assignment
            
            self.steps += 1
                  
                
                
                
        return fitness, assignment
    
def main():
    
    parser = Parser('PA3_Benchmarks\CNF Formulas', '.cnf')
    
    while parser.last_evaluated < len(parser.files):
        sat = LocalSearch()
        sat.num_literals, sat.clauses, sat.lit_dict, sat.found_assignments, filename = parser.parseNext()
        sat.decayRate = len(sat.lit_dict)
        fitness, assignment = sat.localSearch(copy.deepcopy(sat.clauses))
        print(f'Result of Local Search on {filename}: FITNESS = {fitness} / {len(sat.clauses)}, assignments = {assignment}')
        
     
if __name__ == "__main__":
    main()