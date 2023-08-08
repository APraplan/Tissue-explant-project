
def vial(name):
    if name == 'A':
        return [25.5, 120, 60]
    elif name == 'B':
        return [54.5, 120, 60]
    else:
        print('Wrong vial name')
        
        
def tube(name):
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
    

def well_plate(id, type='TPP48'):
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
        
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.solution_prep_num = 0
            self.sub_state = 'go to sol A'
            self.com_state = 'not send'
            
             
    elif self.sub_state == 'go to sol A':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Sol A'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Sol A'][0], y=self.solution_well['Sol A'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Offset"]["Camera"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution A"]["Solution A pumping speed"], ID = 2)
            self.pipette_2_pos -= self.settings["Solution A"]["Solution A pumping volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.mixing_well[self.solution_prep_num][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.mixing_well[self.solution_prep_num][0], y=self.mixing_well[self.solution_prep_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'dropping'
            self.com_state = 'not send'
            
        
    elif self.sub_state == 'dropping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution A"]["Solution A dropping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.solution_prep_num += 1
            
            if self.solution_prep_num < len(self.culture_well) and self.solution_prep_num < self.settings["Well"]["Number of well"]:
                self.sub_state = 'go to sol A'
                self.com_state = 'not send'
                
            else:
                self.state = 'preparing gel'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
    

def preparing_gel(self):
        
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.solution_prep_num = 0
            self.sub_state = 'go to sol B'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'go to sol B':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Sol B'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Sol B'][0], y=self.solution_well['Sol B'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos -= self.settings["Solution B"]["Solution B pumping volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Sol B'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.mixing_well[self.well_num][0], y=self.mixing_well[self.well_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.mix = 0
            self.sub_state = 'mix down'
            self.com_state = 'not send'


    elif self.sub_state == 'mix down':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.mix += 1
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            
            if self.mix > self.settings["Gel"]["Number of mix"]:
                self.sub_state = 'take gel'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'mix up'
                self.com_state = 'not send'

            
    elif self.sub_state == 'mix up':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty - (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*self.settings["Gel"]["Proportion of mixing volume"]
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  

        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'mix down'
            self.com_state = 'not send'
            
    elif self.sub_state == 'take gel':
    
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty - (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*0.9
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  

        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'place gel'
            self.com_state = 'not send'
            
                
    elif self.sub_state == 'place gel':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.mixing_well[self.well_num][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=75, y=140, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.culture_well[self.well_num][0], y=self.culture_well[self.well_num][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Well plate pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'dropping'
            self.com_state = 'not send'


    elif self.sub_state == 'dropping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_2_pos + (self.settings["Solution A"]["Solution A pumping volume"] + self.settings["Solution B"]["Solution B pumping volume"])*0.85
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
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
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Washing'][0], y=self.solution_well['Washing'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.wash = 0
            self.sub_state = 'wash up'
            self.com_state = 'not send'
             
             
    elif self.sub_state == 'wash down':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            
            if self.wash > self.settings["Gel"]["Number of wash"]:
                self.sub_state = 'exit vial'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'wash up'
                self.com_state = 'not send'
            
            
    elif self.sub_state == 'wash up':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 2)
            self.pipette_2_pos = self.pipette_full
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.wash += 1
                
            self.sub_state = 'wash down'
            self.com_state = 'not send'


    elif self.sub_state == 'exit vial':
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        if self.anycubic.get_finish_flag():
            self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'  
            
            
def homming(self):
    
    if self.sub_state == 'go to position':
        
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
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(x=self.reset_pos[0], y=self.reset_pos[1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(z=self.reset_pos[2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go to second position'
            self.com_state = 'not send'   
            
    
    elif self.sub_state == 'go to second position':
            
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sub_state = 'go to dump'
            self.com_state = 'not send'
    
    
    elif self.sub_state == 'go to dump':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Dump'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(x=self.solution_well['Dump'][0], y=self.solution_well['Dump'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty second pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty second pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            
                self.sub_state = 'exit vial'
                self.com_state = 'not send'
                
    elif self.sub_state == 'exit vial':
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Dump'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip two"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        if self.anycubic.get_finish_flag():
            if self.settings["Well"]["Well preparation"]:
                self.state = 'preparing gel'
            else:
                self.state = 'detect'

            self.sub_state = 'go to position'
            self.com_state = 'send'   