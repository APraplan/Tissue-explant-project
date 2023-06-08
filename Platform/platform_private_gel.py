
def vial(name):
    if name == 'A':
        return [72, 217, 60]
    elif name == 'B':
        return [99, 217, 60]
    else:
        print('Wrong vial name')
        
        
def tube(name):
    pos = [122, 217, 42]
    offset = 16
    
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
    

def well_plate(id, type='48'):
    
    if type == '48':
        position = [195.5, 193.3, 25]
        well_offset = 13.45
    elif type == '24':
        position = [193, 194, 25]
        well_offset = 97/5
    elif type == '12':
        position = [187, 183.5, 25]
        well_offset = 74/3
    elif type == '6':
        position = [195.5, 193.3, 25] # need to be changed
        well_offset = 76/2
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
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
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
            self.anycubic.move_axis_relative(z=self.solution_well['Sol A'][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.solution_well['Sol A'][0], y=self.solution_well['Sol A'][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_A_pumping_speed, ID = 2)
            self.pipette_2_pos -= self.solution_A_pumping_volume
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.mixing_well[self.solution_prep_num][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.mixing_well[self.solution_prep_num][0], y=self.mixing_well[self.solution_prep_num][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'dropping'
            self.com_state = 'not send'
            
        
    elif self.sub_state == 'dropping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_A_dropping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.solution_prep_num += 1
            
            if self.solution_prep_num < len(self.culture_well) and self.solution_prep_num < self.number_of_well:
                self.sub_state = 'go to sol A'
                self.com_state = 'not send'
                
            else:
                self.state = 'preparing gel'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
    

def preparing_gel(self):
        
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
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
            self.anycubic.move_axis_relative(z=self.solution_well['Sol B'][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.solution_well['Sol B'][0], y=self.solution_well['Sol B'][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'pumping'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'pumping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos -= self.solution_B_pumping_volume
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'fill well'
            self.com_state = 'not send'   
            
            
    elif self.sub_state == 'fill well':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.mixing_well[self.well_num][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.mixing_well[self.well_num][0], y=self.mixing_well[self.well_num][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.mix = 0
            self.sub_state = 'mix down'
            self.com_state = 'not send'


    elif self.sub_state == 'mix down':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.sub_state = 'mix up'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'mix up':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_empty - (self.solution_A_pumping_volume + self.solution_B_pumping_volume)*0.75
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.mix += 1
            
            if self.mix > self.num_mix:
                self.sub_state = 'place gel'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'mix down'
                self.com_state = 'not send'
                
                
    elif self.sub_state == 'place gel':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.mixing_well[self.well_num][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.culture_well[self.well_num][0], y=self.culture_well[self.well_num][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'dropping'
            self.com_state = 'not send'


    elif self.sub_state == 'dropping':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_2_pos + (self.solution_A_pumping_volume + self.solution_B_pumping_volume)*0.75
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            # self.sub_state = 'washing'
            self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'


    elif self.sub_state == 'washing':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.solution_well['Washing'][0], y=self.solution_well['Washing'][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.wash = 0
            self.sub_state = 'wash up'
            self.com_state = 'not send'
             
             
    elif self.sub_state == 'wash down':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            
            if self.wash > self.num_wash:
                self.state = 'detect'
                self.sub_state = 'go to position'
                self.com_state = 'not send'               
            else:     
                self.sub_state = 'wash up'
                self.com_state = 'not send'
            
            
    elif self.sub_state == 'wash up':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.solution_B_pumping_speed, ID = 2)
            self.pipette_2_pos = self.pipette_full
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            self.wash += 1
                
            self.sub_state = 'wash down'
            self.com_state = 'not send'
            
            
def homming(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 1
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sub_state = 'go to petridish'
            self.com_state = 'not send'
        
        
    elif self.sub_state == 'go to petridish':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(x=self.reset_pos[0], y=self.reset_pos[1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.reset_pos[2], f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go to second position'
            self.com_state = 'not send'   
            
    
    elif self.sub_state == 'go to second position':
            
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 2
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sub_state = 'go to dump'
            self.com_state = 'not send'
    
    
    elif self.sub_state == 'go to dump':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Dump'][2], f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.solution_well['Dump'][0], y=self.solution_well['Dump'][1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.solution_pumping_height, f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty second pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty second pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_2_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_2_pos, ID = 2)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_2_pos, ID = 2):
            if self.well_preparation:
                # self.state = 'spreading solution A'
                self.state = 'preparing gel'
            else:
                self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'   