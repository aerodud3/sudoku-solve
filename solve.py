import numpy as np 

class Solver :
    def __init__(self) : 
        self.master_map = np.zeros([9,9])
        self.master_map[0] = np.array([0,0,3,0,2,1,0,4,0])
        self.master_map[1] = np.array([0,6,7,8,0,0,9,0,0])
        self.master_map[2] = np.array([0,0,0,0,0,0,0,1,3])
        self.master_map[3] = np.array([0,0,8,0,0,2,0,0,4])
        self.master_map[4] = np.array([5,0,0,0,6,0,0,0,9])
        self.master_map[5] = np.array([2,0,0,5,0,0,1,0,0])
        self.master_map[6] = np.array([7,3,0,0,0,0,0,0,0])
        self.master_map[7] = np.array([0,0,9,0,0,6,4,7,0])
        self.master_map[8] = np.array([0,1,0,2,9,0,3,0,0])
        self.row = np.copy(self.master_map)
        self.possible_vals = np.delete(np.arange(10), 0)
        self.guess_arr = [[0 for i in range(9)] for j in range(9)]

    def invert(self) : 
        self.col = self.row.T
    

    def makeBox(self) : 
        self.box = np.zeros([9,3,3])

        for p in range(3) :
            for i in range(3) :
                for j in range(3) : 
                    for k in range(3) :
                        self.box[i + 3*p][j][k] = self.row[j + 3*p][k + 3*i]


    def whichBox(self, row, col) :
        # Finding which box
        if row < 3 :
            if col < 3 : box_num = 0
            elif col < 6 : box_num = 1
            else : box_num = 2

        elif row < 6 :
            if col < 3 : box_num = 3
            elif col < 6 : box_num = 4
            else : box_num = 5

        else : 
            if col < 3 : box_num = 6
            elif col < 6 : box_num = 7
            else : box_num = 8
        
        return box_num
            
    
    def nonZero(self, row_num, col_num) : 
        if self.master_map[row_num][col_num] != 0 :
            print("Error, this box already has a number")

        else : 
            this_arr = []
            for i in np.nonzero(self.row[row_num]) :
                for j in self.row[row_num][i] :
                    this_arr.append(j)

            for i in np.nonzero(self.col[col_num]) :
                for j in (self.col[col_num][i]) :
                    this_arr.append(j)

            box_num = self.whichBox(row_num, col_num)

            box_arr = self.box[box_num][np.nonzero(self.box[box_num])]
            for k in box_arr : 
                this_arr.append(k)
                
            dirty_arr = np.unique(this_arr)
            guess = []
            for i in self.possible_vals :
                 if i not in dirty_arr : 
                    guess.append(i)

            return guess


    def populate(self) : 
        p = 0
        bSolve = False
        # Number of times this is run 
        while p < 4 :
            bSolve = False
            for i in range(9) : 
                for j in range(9) : 
                    if self.row[i][j] == 0 : 
                        
                        if len(self.nonZero(i,j)) == 1 :
                            self.row[i][j] = self.nonZero(i,j)[0]
                            bSolve = True
                            print(f"Solved for a value in pos {i} {j} ")

            p += 1
        if not bSolve :
            self.doubleExclude()

    
    def guessPrint(self) :
        for i in range(9) : 
            for j in range(9) : 
                if self.row[i][j] == 0 : 
                    print(self.nonZero(i,j), f"box {self.whichBox(i,j)}")
                if j == 8 :
                    print("\n")
    
    def doubleExclude(self) :
        iter = 0
        boxy_arr = np.zeros(9)
        for i in range(9) : 
            for j in range(9) : 
                if self.row[i][j] == 0 : 
                    # Filling the guess arrays
                    self.guess_arr[i][j] = self.nonZero(i,j)
                    boxy_arr[self.whichBox(i,j)] += 1

        # Popping values out of boxes with doubles
        while iter < 9 :
            for p in range(9) :
                for q in range(9) :
                    if self.row[p][q] == 0 :
                        if self.whichBox(p,q) == iter :
                                if len(self.guess_arr[p][q]) == 2 :
                                    print(self.guess_arr[p][q], iter)
            iter +=1

        
    def main(self) :
        self.invert()
        self.makeBox()
        self.populate()



    

trial = Solver()
trial.main()

