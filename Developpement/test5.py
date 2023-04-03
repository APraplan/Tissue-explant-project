import pygame
import pygame_gui
from time import sleep
import cv2
import numpy as np


pygame.init()

pygame.display.set_caption('Tissue explant')
window_surface = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)


background = pygame.Surface((1080, 720))
background.fill(pygame.Color('#1e1e1e'))

manager = pygame_gui.UIManager((1080, 720), 'theme1.json')

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Parameters',
                                            manager=manager)

slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((350, 375), (200, 20)),
                                                start_value=0,
                                                value_range=(0,10),
                                                manager=manager)

button_layout_rect = pygame.Rect(0, 0, 100, 20)
button_layout_rect3 = pygame.Rect(50, 50, 150, 20)
button_layout_rect.bottomright = (-30, -20)

hello_button2 = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
        text='Hello', manager=manager,
        anchors={'right': 'right',
                'bottom': 'bottom'})

hello_button3 = pygame_gui.elements.UIButton(relative_rect=button_layout_rect3,
        text='max', manager=manager)

clock = pygame.time.Clock()
is_running = True
full_screen = False

# def make_1080p():
#     cap.set(3, 1920)
#     cap.set(4, 1080)
    
# def make_720p():
#     cap.set(3, 1280)
#     cap.set(4, 720)

# cap = cv2.VideoCapture(0) 

# make_720p()

# Check if camera opened successfully
# if not cap.isOpened():
#     print("Error opening video stream or file")
    
# ret, frame = cap.read()

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            # window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            # background = pygame.Surface((1080, 720))
            # background.fill(pygame.Color('#1e1e1e'))
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                # DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.WINDOWMINIMIZED)
                pass
            if event.ui_element == hello_button2:
                pass
            if event.ui_element == hello_button3:
                full_screen = not full_screen
                if full_screen:
                    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    DISPLAYSURF = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
                    
    # Keyboard                
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_F11]:
        DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    if keys[pygame.K_ESCAPE]:
        DISPLAYSURF = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
            
            
    # display
    window_surface.fill(pygame.Color('#1e1e1e'))
    window_surface.blit(background, (0, 0))
    
    # _, frame = cap.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # xs, ys = window_surface.get_size()
    # frame=pygame.surfarray.make_surface(frame)
    # size_x = xs/1.2
    # size_y = size_x*9/16
    # frame = pygame.transform.scale(frame, (size_x, size_y))
    # xf, yf = frame.get_size()
    # window_surface.blit(frame, (xs-xf-10, ys-yf-10))


    manager.process_events(event)

    manager.update(time_delta)
    
    manager.draw_ui(window_surface)

    pygame.display.update()
    
    sleep(0.02)
