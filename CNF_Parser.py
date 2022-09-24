# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:26:11 2022

@author: dreww
"""
import numpy as np
import os

class Parser:
    def __init__(self, folder, extension): 
        self.directory = folder
        self.extension = extension
        self.files = os.listdir(self.directory)
        self.last_evaluated = 0
        
    def parseNext(self):
        
        filename = self.files[self.last_evaluated]
        file = os.path.join(self.directory, filename)
        
        while not filename.endswith(self.extension):
            filename = self.files[self.last_evaluated]
            file = os.path.join(self.directory, filename)
            if self.last_evaluated < len(self.files):
                self.last_evaluated += 1
            else:
                self.last_evaluated = 0
                break
        
        if os.path.isfile(file) and file.endswith(self.extension):
            with open(file, 'r') as f :
                lines = f.readlines()
            
            num_literals = 0 #should be given in format
            clauses = []
            lit_dict = {}
            
            for clause in lines:
                if clause[0] == '\n' or clause[0] == '%':
                    break
                elif clause[0] != 'c' and clause[0] != 'p':
                    clauses.append([int(lit) for lit in clause.strip(" ").split(" ")])
                elif clause[0] == 'p':
                    num_literals = int(clause.split(" ")[2])

                    
            for clause in clauses:
                if 0 in clause:
                    clause.remove(0)
                clause.sort()
                
            for literal in range(1, num_literals+1):
                lit_dict[literal] = [clause for clause in clauses if literal in clause or -1* literal in clause]
            
            found_assignments = {i: None for i in range(1, num_literals+1)}
            
        if self.last_evaluated < len(self.files):
            self.last_evaluated += 1
        else:
            self.last_evaluated = 0
            
        return num_literals, clauses, lit_dict, found_assignments, filename