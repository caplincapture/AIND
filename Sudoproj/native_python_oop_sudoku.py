# Copyright Peter J.A. Cock, 2006
# All rights reserved.
# 
# You may choose to be bound by either:
#
# (a) Licenced free for personal non-commerial use.
#      May not be redistributed without prior permission.
#
# Or:
# (b) The GPL version 2, see http://www.gnu.org/licenses/gpl.html

RUN_BUILT_IN_TESTS=True
RUN_TEST_FILES=True

TRIPLETS = [[0,1,2],[3,4,5],[6,7,8]]

#Row/Col/3x3 iteration list, each is nine lists of nine (row,col) pairs
ROW_ITER = [[(row,col) for col in range(0,9)] for row in range(0,9)]
COL_ITER = [[(row,col) for row in range(0,9)] for col in range(0,9)]
TxT_ITER = [[(row,col) for row in rows for col in cols] for rows in TRIPLETS for cols in TRIPLETS]

class sudoku:
    def __init__(self, start_grid=None) :
        #Setup list of lists (the rows), each row is a list of 9 cells, which are each a list of integers 1-9 inclusive.
        self.squares =[ [range(1,10)  for col in range(0,9)] for row in range(0,9)]
        
        if start_grid is not None:
            if len(start_grid)==81 :
                for row in range(0,9) :
                    self.set_row(row, start_grid[(row*9):((row+1)*9)])
            else :
                assert len(start_grid)==9, "Bad input!"
                for row in range(0,9) :
                    self.set_row(row, start_grid[row])
                
        #self.check()
        self._changed=False

    def solved(self) :
        for row in range(0,9) :
            for col in range(0,9) :
                if len(self.squares[row][col]) > 1 :
                    return False
        return True

    def copy(self) :
        sudoku_copy = sudoku(None)
        for row in range(0,9) :
            for col in range(0,9) :
                sudoku_copy.squares[row][col] = self.squares[row][col][:] #copy!
        sudoku_copy._changed=False
        return sudoku_copy
    
    def set_row(self,row, x_list) :
        assert len(x_list)==9
        for col in range(0,9) :
            try :
                x = int(x_list[col])
            except :
                x = 0
            #self.set_cell(row,col,x)
            self.set_cell(row,col,x)

    def set_cell(self,row,col,x):
        if self.squares[row][col] == [x] :
            #Already done!
            pass
        elif x not in range(1,9+1) :
            #Set to unknown
            pass
        else:
            assert x in self.squares[row][col], \
            "Told to set square (%i,%i) to an impossible entry, %i" % (row,col,x)
            
            self.squares[row][col] = [x]
            self.update_neighbours(row,col,x)
            self._changed=True
            
    def cell_exclude(self, row,col,x) :
        assert x in range(1,9+1)
        if x in self.squares[row][col] :
            #Remove it...
            self.squares[row][col].remove(x)
            #Should be one or more entries left...
            assert len(self.squares[row][col]) > 0, \
            "Removed last possible entry for square (%i,%i) which was %i" \
            % (row, col, x)
            #Now, has this confirmed the value for this square?
            if len(self.squares[row][col]) == 1 :
                #This cell is now definate..
                #Need to update its friends...
                #print "After exluding %i, square (%i,%i) must be %i" \
                #% (x, self.row, self.col, self[0])
                self._changed=True
                self.update_neighbours(row,col,self.squares[row][col][0])
        else :
            #Don't need to remove this, already done!
            pass
        return

    def row_exclude(self, row, x) :
        assert x in range(1,9+1)
        for col in range(0,9) :
            self.cell_exclude(row,col,x)

    def col_exclude(self, col, x) :
        assert x in range(1,9+1)
        for row in range(0,9) :
            self.cell_exclude(row,col,x)

    def update_neighbours(self,set_row,set_col,x) :
        """Call this when the square is set to x, either directly,
        or as a side effect of an exclude leaving only one entry"""
        #print "Updating (%i,%i) to be %i..."  % (self.row, self.col, x)
        #Update the possibilies in this row...
        for row in range(0,9) :
            if row <> set_row :
                self.cell_exclude(row,set_col,x)
        #Update the possibilies in this col...
        for col in range(0,9) :
            if col <> set_col :
                self.cell_exclude(set_row,col,x)
        #Update the possibilies in this 3x3 square...
        for triplet in TRIPLETS :
            if set_row in triplet : rows = triplet[:]
            if set_col in triplet : cols = triplet[:]
        #Only need to do four of the eight possibles (well, 9 if you count the cell itself)
        #as did two on the row, and two on the col
        rows.remove(set_row)
        cols.remove(set_col)
        for row in rows :
            for col in cols :
                assert row <> set_row or col <> set_col 
                #print "Updating (%i,%i) to be %i, excluding %i from (%i, %i)" \
                #% (self.row, self.col, x, x, row, col)
                self.cell_exclude(row,col,x)
            
    def get_cell_int(self,row,col) :
        if len(self.squares[row][col])==1 :
            return int(self.squares[row][col][0])
        else :
            return 0

    def get_cell_str(self,row,col) :
        if len(self.squares[row][col])==1 :
            return "(%i,%i) = %i" % (row, col, self.squares[row][col][0])
        else :
            return ("(%i,%i) = " % (row, col)) + ",".join([str(x) for x in self.squares[row][col]]) 

    def get_cell_digit_str(self,row,col) :
        if len(self.squares[row][col])==1 :
            return str(self.squares[row][col][0])
        else :
            return "0"
            
    def as_test_81(self) :
        """Return a string of 81 digits"""
        return  "".join(self.as_test_list())
            
    def simple_text(self) :
        return  "\n".join(self.as_test_list())
        
    def as_test_list(self) :
        return  [  ("".join( [self.get_cell_digit_str(row,col) for col in range(0,9)]))  for row in range(0,9) ]
        """
        answer=[]
        for row in range(0,9) :
            line=""
            for col in range(0,9) :
                line = line + self.get_cell_digit_str(row,col)
            answer.append(line)
        return answer
        """

    def __repr__(self):
        answer="[" + ",".join([ \
            ("[" + ",".join( [self.get_cell_digit_str(row,col) for col in range(0,9)]) + "]") \
            for row in range(0,9) ])
        return answer

    def __str__(self):
        answer = "   123   456   789\n"
        for row in range(0,9) :
            answer = answer + str(row+1) \
                        +   " [" + "".join([self.get_cell_digit_str(row,col).replace("0","?") for col in range(0,3)]) \
                        + "] [" + "".join([self.get_cell_digit_str(row,col).replace("0","?") for col in range(3,6)]) \
                        + "] [" + "".join([self.get_cell_digit_str(row,col).replace("0","?") for col in range(6,9)]) \
                        + "]\n"
            if row+1 in [3,6] : 
              answer = answer + "   ---   ---   ---\n"
        return answer
                    
    def check(self, level=0) :
        self._changed=True
        while self._changed:
            #print "checking..."
            self._changed=False
            self.check_for_single_occurances()
            self.check_for_last_in_row_col_3x3()
            if level >= 1 :
                self.overlapping_3x3_and_row_or_col() #(aka slicing and dicing)
            if level >= 2 :
                self.one_level_supposition()
            if level >= 3 :
                self.two_level_supposition()
            
            #If nothing happened, then self.changed==False (still)
            #and we break the loop
        return
        
    def check_for_single_occurances(self):
        #Want to see if x only occurs once in this row/col/3x3...
        for check_type in [ROW_ITER, COL_ITER, TxT_ITER]:
            for check_list in check_type :
                for x in range(1,9+1) : #1 to 9 inclusive
                    x_in_list = []
                    for (row,col) in check_list :
                        if x in self.squares[row][col] :
                            x_in_list.append((row,col))
                    if len(x_in_list)==1 :
                        (row,col) = x_in_list[0]
                        #This position MUST be be x
                        if len(self.squares[row][col]) > 1 :
                            self.set_cell(row,col,x)

    def check_for_last_in_row_col_3x3(self):
        #Now, for each row/col/3x3 want to see if there is a single
        #unknown entry...
        for (type_name, check_type) in [("Row",ROW_ITER),("Col",COL_ITER),("3x3",TxT_ITER)]:
            for check_list in check_type :
                unknown_entries = []
                unassigned_values = range(1,9+1) #1-9 inclusive
                known_values = []
                for (row,col) in check_list :
                    if len(self.squares[row][col]) == 1 :
                        assert self.squares[row][col][0] not in known_values, \
                        "Already have %i (%i,%i) in known list [%s] for %s" % (self.squares[row][col][0],row,col, ",".join(map(str,known_values)), type_name)

                        known_values.append(self.squares[row][col][0])

                        assert self.squares[row][col][0] in unassigned_values, \
                        "Expected %i (%i,%i) in list [%s] for %s" % (self.squares[row][col][0],row,col, ",".join(map(str,unassigned_values)), type_name)

                        unassigned_values.remove(self.squares[row][col][0])
                    else :
                        unknown_entries.append((row,col))
                assert len(unknown_entries) + len(known_values) == 9
                assert len(unknown_entries) == len(unassigned_values)
                if len(unknown_entries) == 1 :
                    #This cell must be the only number 1-9 not in known_values
                    x = unassigned_values[0]
                    (row,col) = unknown_entries[0]
                    
                    #assert x not in known_values

                    #print "Because its the last cell in its row/col/3x3 entry (%i,%i) must be %i" \
                    #% (row,col,x)
                    self.set_cell(row,col,x)
        """
        for row in range(0,9) : self.check_row(row)
        for col in range(0,9) : self.check_col(col)
        #Check the 3x3 squares...
        for rows in TRIPLETS :
            for cols in TRIPLETS :
                for x in range(0,9) :
                    x_in_location=[]
                    for row in rows:
                        for col in cols :
                            if x in self.squares[row][col] :
                                x_in_location.append((row,col))
                    if len(x_in_location)==1 :
                        (row,col) = x_in_location[0]
                        #This position MUST be be x
                        if len(self.squares[row][col]) > 1 :
                            self.set_cell(row,col,x)
        """
        return
        
    def diagnosis(self) :
        answer=""
        df = long(1)
        for row in range(0,9) :
            for col in range(0,9):
                if len(self.squares[row][col]) > 1 :
                    answer = answer + str(self.squares[row][col]) + "\n"
                    df = df * len(self.squares[row][col])
        answer = answer + "Degrees of freedom: %i" % df
        return answer

    def overlapping_3x3_and_row_or_col(self):
        """Block and Column / Row Interactions (name from Simon Armstrong)

        http://www.simes.clara.co.uk/programs/sudokutechnique3.htm

        Also known as 'slicing and dicing'
        """
        #For a given 3x3, and a given digit, want to see if
        #all the remaining candidates are in a single row or column..
        #Want to see if x only occurs once in this row/col/3x3...
        for check_list in TxT_ITER :
            for x in range(1,9+1) : #1 to 9 inclusive
                #print "Checking %i in 3x3" % x, check_list
                rows_for_x = []
                cols_for_x = []
                for (row,col) in check_list :
                    if x in self.squares[row][col] :
                        #print "Found possible %i at (%i,%i)" % (x, row, col)
                        if row not in rows_for_x : rows_for_x.append(row)
                        if col not in cols_for_x : cols_for_x.append(col)
                #Are they all in the same row?
                if len(rows_for_x)==1 and len(cols_for_x) > 1 :
                    #print "%i must be in row %i using cols %s" % (x, rows_for_x[0]+1, ",".join(map(lambda i : str(i+1),cols_for_x)))
                    #print self
                    #This means, we can remove X from all the rest of the row...
                    row = rows_for_x[0]
                    for col in range(0,9) :
                        if col not in cols_for_x :
                            self.cell_exclude(row,col,x)
                    #We can also remove x from all the rest of this 3x3...
                    for (row,col) in check_list :
                        if col not in cols_for_x :
                            if row not in rows_for_x :
                                self.cell_exclude(row,col,x)
                #Are they all in the same col?
                if len(cols_for_x)==1 and len(rows_for_x) > 1 :
                    #print "%i must be in col %i using rows %s" % (x, cols_for_x[0]+1, ",".join(map(lambda i : str(i+1),rows_for_x)))
                    #print self
                    #This means, we can remove X from all the rest of the row...
                    col = cols_for_x[0]
                    for row in range(0,9) :
                        if row not in rows_for_x :
                            self.cell_exclude(row,col,x)
                    #We can also remove x from all the rest of this 3x3...
                    for (row,col) in check_list :
                        if col not in cols_for_x :
                            if row not in rows_for_x :
                                self.cell_exclude(row,col,x)

    def one_level_supposition(self):
        """Probably what is known as 'Nishio', try a number and see if it leads to a dead end.
        
        For all the ambigous squares, try each possible each entry and see
        if its OK, or if it leads to a contradiction.  In the case of a contradiction
        we can remove it as a possibility...
        
        Two level suppositions (two guess) may be required for extreme puzzles..."""
        progress=True
        while progress :
            progress=False
            #print "Doing one level supposition..."
            for row in range(0,9) :
                for col in range(0,9):
                    if len(self.squares[row][col]) > 1 :
                        bad_x = []
                        for x in self.squares[row][col] :
                            #print "/-- Trying setting (%i,%i) to %i" % (row,col,x)
                            sudoku_copy = self.copy()
                            try:
                                sudoku_copy.set_cell(row,col,x)
                                sudoku_copy.check(level=1)
                            except AssertionError, e :
                                #Leads to an error :)
                                #This means that this square cannot be x
                                #print e
                                #print "%s cannot be %i" % (str(self.squares[row][col]), x)
                                bad_x.append(x)
                            del sudoku_copy
                            #print "\-- End of exp"
                        if len(bad_x) == 0 :
                            pass
                        elif len(bad_x) < len(self.squares[row][col]) :
                            for x in bad_x :
                                self.cell_exclude(row,col,x)
                                self.check() 
                            progress=True
                        else :
                            assert False, "Bugger! All possible values for square (%i,%i) fail" \
                            % (row,col)
        #print "One level supposition done"
        
    def two_level_supposition(self) :
        progress=True
        while progress :
            progress=False
            #print "Doing two level supposition..."
            for row in range(0,9) :
                for col in range(0,9):
                    if len(self.squares[row][col]) > 1 :
                        bad_x = []
                        for x in self.squares[row][col] :
                            #print "/-- Trying setting (%i,%i) to %i" % (row,col,x)
                            sudoku_copy = self.copy()
                            try:
                                sudoku_copy.set_cell(row,col,x)
                                #sudoku_copy.check()
                                #sudoku_copy.one_level_supposition()
                                sudoku_copy.check(level=2)
                            except AssertionError, e :
                                #Leads to an error :)
                                #This means that this square cannot be x
                                #print e
                                #print "%s cannot be %i" % (str(self.squares[row][col]), x)
                                bad_x.append(x)
                            del sudoku_copy
                            #print "\-- End of exp"
                        if len(bad_x) == 0 :
                            pass
                        elif len(bad_x) < len(self.squares[row][col]) :
                            for x in bad_x :
                                self.cell_exclude(row,col,x)
                                self.check() 
                            progress=True
                        else :
                            assert False, "Bugger! All possible values for square (%i,%i) fail" \
                            % (row,col)
        #print "Two level supposition done"

if __name__ == "__main__" and RUN_BUILT_IN_TESTS :
    print "Running built in tests..."
    
    tests = []
    
    tests.append(
       ("Easy example from Warwick The Magazine",
       ['081074900', '004019307', '379085014', '007831000', '238456179', '006927400', '843562791', '762198543', '005743862'],
       ['681374925', '524619387', '379285614', '497831256', '238456179', '156927438', '843562791', '762198543', '915743862'],
       None,
       None,
       None))
    tests.append(
       ("Easy example from http://www.sudoku.com/",
       ['060104050', '008305600', '200609001', '800437006', '006852300', '700961004', '500703002', '007206900', '642598173'],
       ['963174258', '178325649', '254689731', '821437596', '496852317', '735961824', '589713462', '317246985', '642598173'],
       None,
       None,
       None))
    tests.append(
       ("Novemeber 2005 contest from http://www.sudoku.com/",
       ['000342000', '540070080', '002005406', '060200000', '308000204', '000008070', '609120500', '030080019', '000539000'],
       ['816342957', '543976182', '792815436', '467253891', '358791264', '921468375', '689127543', '235684719', '174539628'],
       None,
       None,
       None))
    tests.append(
       ("No. One from http://sudokublog.typepad.com/sudokublog/2005/08/two_and_three_i.html",
       ['000538400', '800007000', '437962851', '900605340', '700803005', '053004009', '004759160', '000001003', '001386000'],
       ['219538476', '865147932', '437962851', '982615347', '746893215', '153274689', '324759168', '678421593', '591386724'],
       None,
       None,
       None))
    tests.append(
       ("No. Two from http://sudokublog.typepad.com/sudokublog/2005/08/two_and_three_i.html",
       ['000004000', '000027486', '400803050', '009278300', '700030009', '003469800', '030702008', '248350000', '000900000'],
       ['800604000', '391527486', '400803050', '009278300', '784135009', '023469800', '930742008', '248350000', '000980000'],
       ['800604000', '391527486', '400803050', '009278300', '784135009', '023469800', '930742008', '248351007', '000986000'],
       ['852614793', '391527486', '467893152', '619278345', '784135629', '523469871', '936742518', '248351967', '175986234'],
       None))
    tests.append(
       ("No. Three from http://sudokublog.typepad.com/sudokublog/2005/08/two_and_three_i.html",
       ['508073190', '901600408', '000908035', '070000060', '002000900', '010000080', '190306000', '203007009', '687190304'],
       ['528473196', '931600478', '700918235', '070000560', '002700940', '010000780', '190306807', '203007619', '687190304'],
       ['528473196', '931600478', '700918235', '070000560', '002700940', '010000780', '190306807', '203007619', '687190304'],
       ['528473196', '931625478', '764918235', '379284561', '852761943', '416539782', '195346827', '243857619', '687192354'],
       None))
    tests.append(
       ("X-wings from http://sudokublog.typepad.com/sudokublog/2005/08/xwings.html",
       ['096047080', '000006000', '274108003', '560081207', '007002800', '428079031', '642813759', '000964328', '080725416'],
       ['196347582', '835296174', '274158963', '563481297', '917632845', '428579631', '642813759', '751964328', '389725416'],
       None,
       None,
       None))
    tests.append(
       ("http://blogs.sun.com/roller/page/danrice?entry=wednesday_sudoku_puzzle",
       ['006008070', '100600400', '004210003', '001080090', '260030184', '080060300', '600045700', '005001006', '010900500'],
       ['006408071', '170603400', '004217063', '001780690', '267539184', '089160307', '600045710', '005001006', '010906500'],
       ['006458071', '170693400', '004217063', '001780690', '267539184', '089160307', '600045710', '005001006', '010906500'],
       ['936458271', '172693458', '854217963', '341782695', '267539184', '589164327', '623845719', '795321846', '418976532'],
       None))
    tests.append(
       ("Hard or even impossible from http://langabi.name/blog/2005/07/15/soduku-solver",
       ['000010700', '000030005', '000890000', '320000500', '006000200', '008000090', '000020000', '900070001', '001460070'],
       ['000010700', '000030005', '000890000', '320000500', '006000200', '008000090', '000020000', '900070001', '001460070'],
       ['000010700', '000030005', '000890000', '320000500', '006000200', '008000090', '000020000', '900070001', '001460070'],
       None,
       None)) #Don't try second level supposition - it takes forever and may not work
    tests.append(
       ("Interlocking Triples Zero from http://sudokublog.typepad.com/sudokublog/2005/08/interlocking_tr.html",
       ['006809010', '000003600', '003207085', '290371000', '350624079', '000985032', '180006300', '005008000', '030702500'],
       ['506849013', '800153600', '013267085', '290371056', '350624079', '000985032', '180596300', '005438001', '030712508'],
       ['526849713', '879153624', '413267985', '298371456', '351624879', '647985132', '182596347', '765438291', '934712568'],
       None,
       None))
    tests.append(
       ("Interlocking Triples One from http://sudokublog.typepad.com/sudokublog/2005/08/interlocking_tr.html",
       ['051003040', '006051038', '380700520', '018000005', '000010000', '500000410', '067004153', '143675289', '020100674'],
       ['051003046', '006051038', '380700521', '018000305', '030510800', '500300410', '067004153', '143675289', '025130674'],
       ['051003046', '006051038', '380700521', '018000305', '030510800', '500300410', '067004153', '143675289', '025130674'],
       ['251983746', '476251938', '389746521', '718492365', '634517892', '592368417', '967824153', '143675289', '825139674'],
       None))
    tests.append(
       ("Interlocking Triples Two from http://sudokublog.typepad.com/sudokublog/2005/08/interlocking_tr.html",
       ['500830027', '700600100', '308004006', '180000002', '430070019', '900000074', '600100708', '804007001', '270086000'],
       ['500830427', '740600183', '308704006', '187000002', '430070019', '900000074', '603100708', '804307261', '271086005'],
       ['500830427', '740600183', '308704006', '187000002', '430070019', '900000074', '603100708', '804307261', '271086005'],
       ['569831427', '742695183', '318724956', '187469532', '435278619', '926513874', '653142798', '894357261', '271986345'],
       None))
    tests.append(
       ("A 'very hard Sudoku' from http://www.saidwhat.co.uk/sudokus/index.php",
       ['100802030', '700000020', '000560070', '008000900', '005217403', '004000700', '030089000', '020000008', '080004006'],
       ['159872634', '763001825', '842563179', '278000901', '695217483', '314008702', '030089207', '020000008', '080024006'],
       ['159872634', '763941825', '842563179', '278435961', '695217483', '314698752', '536189247', '421756398', '987324516'],
       None,
       None))
    tests.append(
       ("A 'Fiendish Sudoku' from http://www.saidwhat.co.uk/sudokus/index.php",
       ['030000014', '200500680', '900300000', '050010030', '080030070', '060020090', '000008002', '003004001', '570000000'],
       ['635782914', '247591683', '918346527', '752619438', '189435276', '364827195', '496178352', '823954761', '571263849'],
       None,
       None,
       None))
    tests.append(
       ("Angus Johnson",
       ['040300070', '800061000', '000087003', '006040010', '420010095', '010050600', '700630000', '000570001', '050004060'],
       ['140305876', '800061000', '000087103', '506040010', '420016095', '010050600', '701630000', '004570001', '050104060'],
       ['140305876', '800061000', '000087103', '506040010', '420016095', '010050600', '701630000', '004570001', '050104060'],
       ['149325876', '873461529', '265987143', '536849217', '428716395', '917253684', '791638452', '684572931', '352194768'],
       None))
    tests.append(
       ("http://sudoku.com/forums/viewtopic.php?t=1057",
       ['681735942', '592841637', '700000581', '006080203', '000000100', '009050470', '300000769', '917563824', '268479315'],
       ['681735942', '592841637', '700000581', '006080203', '000000100', '009050470', '300218769', '917563824', '268479315'],
       ['681735942', '592841637', '700000581', '006080203', '000000100', '009050470', '300218769', '917563824', '268479315'],
       ['681735942', '592841637', '734692581', '456187293', '873924156', '129356478', '345218769', '917563824', '268479315'],
       None))
    tests.append(
       ("Gallery: really tough puzzles, no 142. from http://www.paulspages.co.uk/sudoku/",
       ['850100000', '900000080', '600004003', '700000002', '308500100', '400090006', '200700004', '530000001', '100002070'],
       ['853169427', '914273685', '672854913', '795641832', '368527149', '421398756', '289715364', '537486291', '146932578'],
       None,
       None,
       None))
    tests.append(
       ("Gallery: outlaw puzzles, no 129. from http://www.paulspages.co.uk/sudoku/",
       ['900002600', '004000005', '007001000', '035080900', '600000004', '001007020', '000300800', '500000700', '002600001'],
       ['900002600', '004000005', '007001000', '035080900', '600000004', '001007020', '000300800', '500000700', '002600001'],
       ['900002600', '004000005', '007001000', '035080900', '600000004', '001007020', '000300800', '500000700', '002600001'],
       ['953742618', '124896375', '867531249', '235184967', '679253184', '481967523', '746315892', '518429736', '392678451'],
       None))
    tests.append(
       ("Gallery: outlaw puzzles, no 112. from http://www.paulspages.co.uk/sudoku/",
       ['800000600', '040500100', '070090000', '030020007', '600008004', '500000090', '000030020', '001006050', '004000003'],
       ['800000600', '040500100', '170090000', '430020007', '600008004', '500000090', '000030020', '301006050', '004000003'],
       ['800000600', '040500100', '170090000', '430020007', '600008004', '500000090', '000030020', '301006058', '004000003'],
       ['852314679', '943567182', '176892345', '438129567', '619758234', '527643891', '785431926', '391276458', '264985713'],
       None))
    tests.append(
       ("19-cell '#1' from Brain of Britain, http://sudoku.sourceforge.net/brain.htm#3x3",
       ['000040030', '980601000', '000000200', '000000001', '004050700', '600000000', '005000000', '000908076', '070030000'],
       ['000040030', '983621457', '000000200', '000000001', '004050700', '600000005', '005000000', '002918576', '070030000'],
       ['000040030', '983621457', '000000200', '000000001', '004050700', '600000005', '005000000', '002918576', '070030000'],
       ['267549138', '983621457', '541783269', '758392641', '314856792', '629174385', '195467823', '432918576', '876235914'],
       None))
    tests.append(
       ("19-cell '#4' - Hardest 3x3 ever - from Brain of Britain, http://sudoku.sourceforge.net/brain.htm#3x3",
       ['020000000', '000600003', '074080000', '000003002', '080040010', '600500000', '000010780', '500009000', '000000040'],
       ['026000000', '000600003', '074080000', '000003002', '080040010', '600500000', '000010780', '500009000', '000000040'],
       ['026000000', '000600003', '074080000', '000003002', '080040010', '600500000', '000010780', '500009000', '000000040'],
       ['126437958', '895621473', '374985126', '457193862', '983246517', '612578394', '269314785', '548769231', '731852649'],
       None))
    tests.append(
       ("Hard from Arjen Lentz for MySQL, http://forums.mysql.com/read.php?98,51406",
       #['043080250',  '600000000', '000001094', '900004070', '000608000', '010200003', '820500000', '000000005', '034090710'],
       ['043080250', '600000000', '000001094', '900004070', '000608000', '010200003', '820500000', '000000005', '534890710'],
       ['043980250', '600425000', '200001094', '900004070', '300608000', '410209003', '820500000', '000000005', '534890710'],
       ['043980250', '600425000', '200001094', '900004070', '300608000', '410209003', '820500000', '000000005', '534890710'],
       ['143986257', '679425381', '285731694', '962354178', '357618942', '418279563', '821567439', '796143825', '534892716'],
       None))
    tests.append(
       ("Ambiguous from Arjen Lentz for MySQL, http://forums.mysql.com/read.php?98,51406",
       #['043080250', '600000000', '000001094', '900004070', '000608000', '010200003', '020500000', '000000005', '034090710'],
       ['043080250', '600000000', '000001094', '900004070', '000608000', '010200003', '020500000', '000000005', '534890710'],
       ['043980250', '600425000', '200001094', '900004070', '300608000', '410209003', '020500000', '000000005', '534890710'],
       ['043980250', '600425000', '200001094', '900004070', '300608000', '410209003', '020500000', '000000005', '534890710'],
       ['043986250', '600425000', '200731694', '900304070', '300608040', '410209063', '020500000', '000100025', '534892716'],
       None))
    tests.append(
        ("top95 = 48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....",
        ['480300000','000000071','020000000','705000060','000200800','000000000','001076000','300000400','000050000'],
        ['480300000','000000071','120000000','705000060','000200800','000000000','001076000','300000400','000053000'],
        ['480300000','000000071','120000000','705000060','000200800','000000000','001076000','300000400','000053000'],
        ['487312695','593684271','126597384','735849162','914265837','268731549','851476923','379128456','642953718'],
        None))

    for test in tests :
        name = test[0]
        print "Running test: " + name

        x = sudoku(test[1])

        assert x.as_test_list() == test[1], "Load failed"
        
        x.check()
        assert x.as_test_list() == test[2], "Simple check failed"

        if test[3] is not None and not x.solved() :
            if test[3] <> test[2]: print "Overlapping (aka slicing and dicing) should helps"
            x.overlapping_3x3_and_row_or_col()
            #x.check()
            assert x.as_test_list() == test[3], "Overlapping failed"
        
        if test[4] is not None and not x.solved() :
            if test[4] <> test[3]: print "One level supposition helps"
            x.one_level_supposition()
            #x.check()
            assert x.as_test_list() == test[4], "One level supposition failed"

        if test[5] is not None and not x.solved() :
            if test[5] <> test[4]: print "Two level supposition helps"
            x.two_level_supposition()
            #x.check()
            assert x.as_test_list() == test[5], "Two level supposition failed"
    print "Builtin tests passed"
    
if __name__ == "__main__" and RUN_TEST_FILES :
    print "Running test files"
    #Using only check() and one_level_suposition(), completes 82 out of 95 in this test file, http://magictour.free.fr/top95
    import os
    import time
    for test_file in ["top95.txt","top91.txt","top100.txt","msk_009.txt","top870.txt"] :
        if not os.path.isfile(test_file) :
            #Try without the extension...
            test_file = test_file[:-4]
        if os.path.isfile(test_file) :
            print "Running tests from file %s" % test_file
            input_file = open(test_file, "r")
            score = 0
            count = 0
            start_time = time.time()
            while True :
                line = input_file.readline()
                if not line : 
                    break
                if len(line)==0 :
                    break
                if line[-1] == "\n" :
                    line = line[:-1]
                if line[-1] =="\r" :
                    line = line[:-1]
                if len(line)==81 :
                    count=count+1
                    print "%i - [%s]" % (count, line),
                    x = sudoku(line)
                    x.check(level=2)
                    #x.overlapping_3x3_and_row_or_col()
                    #x.check()
                    #x.one_level_supposition()
                    #x.check()
                    if not x.solved() :
                        print "Trying level two",
                        #x.two_level_supposition()
                        x.check(level=3)
                    if x.solved() :
                        print " - Done"
                        score=score+1
                    else :
                        print "- Failed"
                        print x.as_test_list()
                else :
                    print "Bad line:\n%s" % line
            job_time = time.time()-start_time
            input_file.close()
            print "Score %i / %i in %0.2f seconds" % (score,count,job_time)
        else :
            print "Could not find test file " + test_file
    
if __name__ == "__main__" :
    print "Running demonstration..."
    
    t = sudoku(["800500930",
                   "050000000",
                   "000200100",
                   "007020000",
                   "600190008",
                   "400300069",
                   "000000450",
                   "104080000",
                   "000406007"])
                   
    print "Before:"
    #print t.as_test_list()
    print t

    print "Check:"
    t.check()
    print t

    print "overlapping_3x3_and_row_or_col:"
    t.check(level=1)
    print t

    print "supposition:"
    t.check(level=2)
    #print t.as_test_list()
    print t

