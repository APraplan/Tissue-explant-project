
def vial(name):
    '''
    Returns the position of the vials A and B. These should be the water's vial and the cellmatrix solution's vial.
    Input:  name :      (string) A or B
    Output: position :  [x, y, z]
    '''
    if name == 'A':
        return [25.5, 120, 60]
    elif name == 'B':
        return [54.5, 120, 60]
    else:
        print('Wrong vial name')
        
        
def tube(name):
    '''
    Returns the position of the desired tube (for the first part of the mixture, without the cellmatrix solution)
    Input:  name :      (string) A, B, C, D, E or F
    Output: position :  [x, y]
    '''
    pos = [5, 140, 42]
    offset = 14
    
    if name == 'A':
        pos[0] += 0
    elif name == 'B':
        pos[0] += 1*offset
    elif name == 'C':
        pos[0] += 2*offset
    elif name == 'D':
        pos[0] += 3*offset
    elif name == 'E':
        pos[0] += 4*offset
    elif name == 'F':
        pos[0] += 5*offset
    
    return pos
    

def well_plate(id, type='TPP12'):
    '''
    Defines the position of the well in the well plate. The argument type is defined in the settings.json, and can
    either be modified manually there, or during the code's execution, in the user's window.
    Refer to the manufacturer's documentation for the well plate's dimensions.
    Input:  id :        (string) A1, A2, ..., F8
            type :      (string) TPP6, TPP12, TPP24, TPP48, NUNC48, FALCON48
    Output: position :  [x, y]
    '''
    # https://www.tpp.ch/page/downloads/IFU_TechDoc/TechDoc-testplates-measurements-d-e.pdf?m=1643984087&
    
    border = [170, 134]
    
    if type == 'TPP6':
        position = [border[0]-24, border[1]-24.4, 25]
        well_offset = 37.5
    elif type == 'TPP12':
        position = [border[0]-17.9, border[1]-26.55, 25]
        well_offset = 24.9
    elif type == 'TPP24':
        position = [border[0]-14.85, border[1]-15.4, 25]
        well_offset = 18.6
    elif type == 'TPP48':
        position = [border[0]-10.25, border[1]-18.4, 25]
        well_offset = 13
    elif type == 'NUNC48':
        position = [border[0]-10, border[1]-15.5, 25]
        well_offset = 13.5
    elif type == 'FALCON48':
        position = [border[0]-11.0, border[1]-18.5, 25]
        well_offset = 12.85
    else:
        print('Wrong well plate type')
    
    ''' 
    In the well plate, there are multiple wells. The position for each culture is determined by the position in settings.json.
    It is defined like a chess board:
     _____________________________
    | A1 | B1 | C1 | D1 | E1 | F1 |
    | A2 | B2 | C2 | D2 | E2 | F2 |
    | A3 | B3 | C3 | D3 | E3 | F3 |
    | A4 | B4 | C4 | D4 | E4 | F4 |
    | A5 | B5 | C5 | D5 | E5 | F5 |
    | A6 | B6 | C6 | D6 | E6 | F6 |
    | A7 | B7 | C7 | D7 | E7 | F7 |
    | A8 | B8 | C8 | D8 | E8 | F8 |
     ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅
    The letter defines the column (x position), and the number defines the row ( y position).
    
    '''
    if id[0] == 'A':
        position[0] = position[0]
        position[1] = position[1] - (int(id[1])-1)*well_offset
    elif id[0] == 'B':
        position[0] = position[0] - 1*well_offset
        position[1] = position[1] - (int(id[1])-1)*well_offset
    elif id[0] == 'C':
        position[0] = position[0] - 2*well_offset
        position[1] = position[1] - (int(id[1])-1)*well_offset
    elif id[0] == 'D':
        position[0] = position[0] - 3*well_offset
        position[1] = position[1] - (int(id[1])-1)*well_offset
    elif id[0] == 'E':
        position[0] = position[0] - 4*well_offset
        position[1] = position[1] - (int(id[1])-1)*well_offset
    elif id[0] == 'F':
        position[0] = position[0] - 5*well_offset
        position[1] = position[1] - (int(id[1])-1)*well_offset
        
    return position


def spreading_solution_A(self):
    '''
    Manages the substates for the spreading of the solution A.
    '''
    if self.sub_state == 'go to position':
        ''' Moves up (z) to a safe position, as to not break anything, and waits'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once the z-movement is done, we select the proper tip (the second one), and change the substate to go to the vial'''
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.solution_prep_num = 0
            self.sub_state = 'go to sol A'
            self.com_state = 'not send'
            
             
    elif self.sub_state == 'go to sol A':
        '''' Moves to the vial containing the solution A'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the vial containing the solution A, and finally enters'''
            self.anycubic.move_axis_relative(z=self.solution_well['Sol A'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Sol A'][0], y=self.solution_well['Sol A'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Offset"]["Camera"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once it is done entering the vial, changes the substate to pumping'''
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        ''' Pumps the solution A'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps the solution A'''
            self.dyna.write_profile_velocity(self.settings["Solution A"]["Solution A pumping speed"], ID = 2)
            self.pipette_2_pos -= self.settings["Solution A"]["Solution A pumping volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then change the substate to fill well'''
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        '''Moves to the mixing tubes'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the tubes, and finally enters'''
            self.anycubic.move_axis_relative(z=self.mixing_well[self.solution_prep_num][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.mixing_well[self.solution_prep_num][0], y=self.mixing_well[self.solution_prep_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the substate to mix down'''
            self.sub_state = 'dropping'
            self.com_state = 'not send'
            
        
    elif self.sub_state == 'dropping':
        ''' Pumps out the solution A into the mixing tubes'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the solution A'''
            self.dyna.write_profile_velocity(self.settings["Solution A"]["Solution A dropping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, repeats until all of the mixing tubes are full, and then changes
            the substate to preparing the gel'''
            self.solution_prep_num += 1
            
            if self.solution_prep_num < len(self.culture_well) and self.solution_prep_num < self.settings["Well"]["Number of well"]:
                self.sub_state = 'go to sol A'
                self.com_state = 'not send'
                
            else:
                self.state = 'preparing gel'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
    

def preparing_gel(self):
    ''' Prepares the gel'''
    if self.sub_state == 'go to position':
        ''' Moves up (z) to a safe position, as to not break anything, and waits'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once the z-movement is done, we select the proper tip (the second one), and change the substate to go to the vial'''
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.solution_prep_num = 0
            self.sub_state = 'go to sol B'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'go to sol B':
        ''' Moves to the vial containing the solution B'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Sol B'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Sol B'][0], y=self.solution_well['Sol B'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once it is done entering the vial, changes the substate to pumping'''
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        ''' Pumps the solution B'''
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos -= self.settings["Solution B"]["Solution B pumping volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then change the substate to fill well'''
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        ''' Moves to the mixing tubes'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the tubes, and finally enters'''
            self.anycubic.move_axis_relative(z=self.solution_well['Sol B'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.mixing_well[self.well_num][0], y=self.mixing_well[self.well_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the substate to mix down and sets the counter to 0'''
            self.mix = 0
            self.sub_state = 'mix down'
            self.com_state = 'not send'


    elif self.sub_state == 'mix down':
        ''' Pumps out the solution B into the mixing tubes'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the solution B, and then increment the mix counter'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.mix += 1
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to mix up or take gel, depending on the number of mix'''
            if self.mix > self.settings["Gel"]["Number of mix"]:
                self.sub_state = 'take gel'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'mix up'
                self.com_state = 'not send'

            
    elif self.sub_state == 'mix up':
        ''' Pumps the solution B from the mixing tubes'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps the solution B'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty - (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*self.settings["Gel"]["Proportion of mixing volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  

        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to mix down'''
            self.sub_state = 'mix down'
            self.com_state = 'not send'
            
    elif self.sub_state == 'take gel':
        ''' Takes the gel from the mixing tubes'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps the solution B'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty - (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*self.settings["Gel"]["Proportion of mixing volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  

        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to place gel'''
            self.sub_state = 'place gel'
            self.com_state = 'not send'
            
                
    elif self.sub_state == 'place gel':
        ''' Moves to the well plate to place the gel'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the well plate, and finally enters'''
            self.anycubic.move_axis_relative(z=self.mixing_well[self.well_num][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=75, y=140, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.culture_well[self.well_num][0], y=self.culture_well[self.well_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the substate to dropping'''
            self.sub_state = 'dropping'
            self.com_state = 'not send'


    elif self.sub_state == 'dropping':
        ''' Drops the gel into the well plate'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the solution B'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_2_pos + (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*0.8*self.settings["Gel"]["Proportion of mixing volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to washing'''
            # Normal experiment
            self.sub_state = 'washing'
            self.com_state = 'not send'

            # Experiment without washing
            # self.state = 'detect'
            # self.sub_state = 'go to position'
            # self.com_state = 'not send'

            # Only gel prep
            # self.well_num += 1
            # if self.well_num >= len(self.culture_well) or self.well_num >= self.settings["Well"]["Number of well"]:
            #     self.state = 'done'
            #     self.com_state = 'not send'
            # else:
            #     self.state = 'preparing gel'
            #     self.sub_state = 'go to position'
            #     self.com_state = 'not send'


    elif self.sub_state == 'washing':
        ''' Washes the pipette'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the washing vial, and finally enters'''
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Washing'][0], y=self.solution_well['Washing'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the substate to wash up and sets the wash counter to 0'''
            self.wash = 0
            self.sub_state = 'wash up'
            self.com_state = 'not send'
             
             
    elif self.sub_state == 'wash down':
        ''' Pumps out the solution B from the washing vial'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the solution B'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to wash up or exit vial, depending on the number of wash'''
            if self.wash >= self.settings["Gel"]["Number of wash"]:
                self.sub_state = 'exit vial'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'wash up'
                self.com_state = 'not send'
            
            
    elif self.sub_state == 'wash up':
        ''' Pumps the solution B from the washing vial'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the solution B'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_full
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the pumping is done, then changes the substate to wash down and increment the wash counter'''
            self.wash += 1
                
            self.sub_state = 'wash down'
            self.com_state = 'not send'


    elif self.sub_state == 'exit vial':
        ''' Self explanatory'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        if self.anycubic.get_finish_flag():
            self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'  
            
            
def homming(self):
    ''' First state of the machine after the calibration sequence'''
    if self.sub_state == 'go to position':
        ''' Moves up (z) to a safe position, as to not break anything, and waits'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])

            # Calibration test
            # self.anycubic.move_axis_relative(x=well_plate('A1', self.settings["Well"]["Type"])[0], y=well_plate('A1', self.settings["Well"]["Type"])[1], offset=self.settings["Offset"]["Tip one"])
            # self.anycubic.move_axis_relative(x=well_plate('A8', self.settings["Well"]["Type"])[0], y=well_plate('A8', self.settings["Well"]["Type"])[1], offset=self.settings["Offset"]["Tip one"])
            # self.anycubic.move_axis_relative(x=well_plate('F8', self.settings["Well"]["Type"])[0], y=well_plate('F8', self.settings["Well"]["Type"])[1], offset=self.settings["Offset"]["Tip one"])
            # self.anycubic.move_axis_relative(x=well_plate('F1', self.settings["Well"]["Type"])[0], y=well_plate('F1', self.settings["Well"]["Type"])[1], offset=self.settings["Offset"]["Tip one"])

            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once the z-movement is done, defines the different mixing tubes, culture well and solution well's positions, selects the firt tip
            and changes the substate to go to petridish'''
            self.mixing_well = [tube('A'), tube('B'), tube('C'), tube('D'), tube('E'), tube('F')]
            self.culture_well = [well_plate(self.settings["Well"]["Culture 1"], self.settings["Well"]["Type"]), well_plate(self.settings["Well"]["Culture 2"], self.settings["Well"]["Type"]),
                                 well_plate(self.settings["Well"]["Culture 3"], self.settings["Well"]["Type"]), well_plate(self.settings["Well"]["Culture 4"], self.settings["Well"]["Type"]),
                                 well_plate(self.settings["Well"]["Culture 5"], self.settings["Well"]["Type"]), well_plate(self.settings["Well"]["Culture 6"], self.settings["Well"]["Type"])]
            self.solution_well = {'Sol A' : vial('A'), 'Sol B' : vial('B'), 'Washing' : vial('A'), 'Dump' : vial('A')}

            
            self.tip_number = 1
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sub_state = 'go to petridish'
            self.com_state = 'not send'
        
        
    elif self.sub_state == 'go to petridish':
        ''' Moves to the petridish'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(x=self.reset_pos[0], y=self.reset_pos[1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(z=self.reset_pos[2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once it is done entering the petridish, changes the substate to empty pipette'''
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        ''' Sets the speed for the emptying of the pipette, and empties it
        It empties the pipette over the petridish, as the first pipette is the one picking up cells'''
        ###### Est-ce que c'est bien de faire comme ça ? 
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            ''' Waits until the emptying is done, then changes the substate to go to second position'''
            self.sub_state = 'go to second position'
            self.com_state = 'not send'   
            
    
    elif self.sub_state == 'go to second position':
        ''' Moves to the second position'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the second position, and finally enters'''
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once it reached the second position, changes the substate to go to dump'''
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sub_state = 'go to dump'
            self.com_state = 'not send'
    
    
    elif self.sub_state == 'go to dump':
        ''' Moves to the dump vial, as the second pipette is the one responsible for the mixing.'''
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the dump vial, and finally enters'''
            self.anycubic.move_axis_relative(z=self.solution_well['Dump'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Dump'][0], y=self.solution_well['Dump'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            ''' Once it is done entering the vial, changes the substate to empty second pipette'''
            self.sub_state = 'empty second pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty second pipette':
        ''' Sets the speed for the emptying of the pipette, and empties it'''
        print("first purge here ?")
        if self.com_state == 'not send':
            ### METTRE ICI LA PREMIERE PURGE ?
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            ''' Waits until the emptying is done, then changes the substate to exit vial'''
            self.sub_state = 'exit vial'
            self.com_state = 'not send'
                
    elif self.sub_state == 'exit vial':
        ''' self explanatory'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Dump'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        if self.anycubic.get_finish_flag():
            ''' Changes stat  to preparing well if the parameter has been set to true, else changes state to detect'''
            if self.settings["Well"]["Well preparation"]:
                self.state = 'preparing gel'
            else:
                self.state = 'detect'

            self.sub_state = 'go to position'
            self.com_state = 'not send'   