# -*- coding: utf-8 -*-

#from psychopy import visual, event, core
from _game import Game
import multiprocessing as mp
import pygame
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()
                
                
####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pygame.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

    def Main():
    
        game = Game()
        game.newGame()
        exit_game = False

        while not exit_game:
        
            while game.run:
                
                pygame.time.delay(20)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        
                if exit_game:
                    break
                
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_ESCAPE]:
                    game.lose()
                
                if blink.value == 1: #you can put any event you want over here to jump
                    game.move()
                    blink.value = 0
                
                game.manageEvents()
                
                for _ in range(5):
                    game.renderFrame()
                
                if not game.run:
                    pygame.time.delay(1000)
                    
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
            
            keys = pygame.key.get_pressed()
            
            if blink.value == 1: #you can put any event you want over here to start new game
                game.newGame()
                blink.value = 0
            
            if keys[pygame.K_ESCAPE]:
                break
        
        pygame.quit()


    if __name__ == "__main__":
        Main()

# Zakończenie podprocesów
    proc_blink_det.join()
