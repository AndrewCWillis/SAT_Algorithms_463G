# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 12:08:24 2022

@author: Owner
"""
import numpy as np
import time
import copy
from CNF_Parser import Parser

class DPLL:
    def __init__(self): 
        self.clauses = [] #list of clauses [lists also]
        
        self.lit_dict = {} # a mapping of literals to (pointer) the clauses that contain them
        self.found_assignments = None
        self.fitness = 0
        
    def findUnitClauses(self, clauses):
        unitClauses = []
        for clause in clauses:
            if len(clause) == 1 and clause not in unitClauses:
                unitClauses.append(clause)
            
        if len(unitClauses) != 0:
            unitClauses.sort()
        return unitClauses     
    
    def findPureLiterals(self, clauses):
        #find all the literals in the set of clauses[] that only occur with a single polarity across all clauses
        
        pureLiterals = []
        
        literals_left = set(literal for clause in clauses for literal in clause)
        
        
        for literal in literals_left:
            if (-1*literal) not in literals_left:
                pureLiterals.append(literal)
                
          
        return pureLiterals
       
    def unitProp(self, unit_literal, clauses):
        #the Unit_literal is the ONLY unassigned literal in a clause. 
        #this might be the instance of a clause only containing one literal, which is unassigned
        #or this might be a clause with many assigned literals, and only one unassigned literal
        
        #UNIT PROP STEPS:
            #1. The Unit-Clause is removed, if it is in the set of clauses. Because it must evaluate to True, thus can be ignored
            #2. every clause containing the unit_literal is removed from clauses set
            #3. for every clause containing !unit_literal, the !unit_literal entry is deleted from that clause
        if unit_literal < 0:
            
            self.found_assignments[abs(unit_literal)] = False
        else:
            
            self.found_assignments[unit_literal] = True
            
        negation = unit_literal
        negation *= -1
        temp = []
        for clause in clauses:
            
            if unit_literal in clause: #look at dictionary to find the clauses that contain this literal
                
                temp.append(clause)
                
            if negation in clause:
                
                clause.remove(-1 * unit_literal)
                
        for clause in temp:
            clauses.remove(clause)    
        return clauses

    def literalAssign(self, pure_literal, clauses):
        #a PURE literal is a literal that only appears with a single polarity in each clause in the set of clauses[]
        #that could be each occurance being: !x1, OR x1. Not both.
        
        #LITERAL ASSIGNMENT STEPS:
            #A pure literal can always be assigned a value that make all the clauses it occurs in evaluate to TRUE
            #Thus we simply delete each clause that contains pure_literal from the list of clauses
        if pure_literal < 0:
            self.found_assignments[abs(pure_literal)] = False
        else:
            self.found_assignments[pure_literal] = True
            
        temp = []   
        for clause in clauses:
            if pure_literal in clause:
                temp.append(clause)
        
        for clause in temp: #remove the clauses identified to be removed
            clauses.remove(clause)
            
        return clauses
    

    def chooseLiteral(self, clauses):
        #will probably do the literal with the most occurances, and return it 
        
        literals_left = set()
        for clause in clauses: #get the (unique) literals left in clauses
            for literal in clause:
                literals_left.add(literal)
                
        output = [abs(x) for x in literals_left]#makes random literal selection easier  
        return output[np.random.randint(0, len(literals_left))]

    def  dpll(self, clauses, depth, display):

        unitClauses = self.findUnitClauses(clauses)
        #print(display)

        while len(unitClauses) != 0:
            
            unitClause = unitClauses.pop()
            if unitClause != []:
                clauses = self.unitProp(unitClause[0], clauses)
            unitClauses = self.findUnitClauses(clauses)
            
        pureLiterals = self.findPureLiterals(clauses)
        
        while len(pureLiterals) != 0:
            
            pureLiteral = pureLiterals.pop()
            clauses = self.literalAssign(pureLiteral, clauses)
            pureLiterals = self.findPureLiterals(clauses)
            
        fitness = len(self.clauses) - len(clauses)
        if fitness > self.fitness:
            self.fitness = fitness
        
        if len(clauses) == 0:
            return True
        if [] in clauses:
            #print(f'[Depth: {depth}] BRANCH FAILURE!! FITNESS: '+str(len(self.clauses) - len(clauses)))
            return False
        
        chosen_literal = self.chooseLiteral(clauses)

        return self.dpll(self.unitProp(chosen_literal, copy.deepcopy(clauses)), depth+1, f'[Depth: {depth+1}] Try {chosen_literal} as True.') or self.dpll(self.unitProp(chosen_literal * -1, copy.deepcopy(clauses)), depth+1, f'[Depth: {depth+1}] Try {chosen_literal} as False.')
        
def main():
    
    parser = Parser('PA3_Benchmarks\CNF Formulas', '.cnf')
    #parser = Parser('PA3_Benchmarks\HARD CNF Formulas', '.cnf')

    while parser.last_evaluated < len(parser.files):
        sat = DPLL()
        sat.num_literals, sat.clauses, sat.lit_dict, sat.found_assignments, filename = parser.parseNext()
        start_time = time.time()
        result = sat.dpll(copy.deepcopy(sat.clauses), 0, f'Begin DPLL on {filename}.')
        end_time = time.time() - start_time
        print(f'Result of DPLL on {filename}: {result}. Time Spent: {end_time}. Max Fitness: {sat.fitness} per ')
        print(f'Found assignments for {filename}: {sat.found_assignments}')
        
if __name__ == "__main__":
    main()