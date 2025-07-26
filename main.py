# libarary

import pygame as pg
import random as rd
# value

running = 0
FPS = 120
floor_x_pos = 0
g = 0.098
bird_movement = 0  

score = 0
height_score = 0



#set_value
pg.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)
pg.init()
screen = pg.display.set_mode((360, 640))
clock = pg.time.Clock()

bg = pg.image.load("img/background-night.png").convert()
bg = pg.transform.scale(bg, (360, 640))

floor = pg.image.load("img/floor.png")
floor = pg.transform.scale(floor, (360, 120)).convert()

bird_down = pg.image.load("img/yellowbird-downflap.png").convert_alpha()
bird_up = pg.image.load("img/yellowbird-upflap.png").convert_alpha()
bird_mid = pg.image.load("img/yellowbird-midflap.png").convert_alpha()
bird_list = [bird_down, bird_mid, bird_up];
bird_index = 0
bird = bird_list[bird_index]
bird = pg.transform.scale(bird, (34, 24))
bird_rect = bird.get_rect(center=(100, 280))
bird_flap = pg.USEREVENT + 1
pg.time.set_timer(bird_flap, 200)

game_font = pg.font.Font("04B_19.TTF", 31)


pipe_surface = pg.image.load("img/pipe-green.png").convert()
pipe_surface = pg.transform.scale(pipe_surface, (52, 320))
pipe_list = []
pipe_height = [320, 340, 360, 380, 400]
spawn_pipe = pg.USEREVENT
pg.time.set_timer(spawn_pipe, 1000)

game_start = pg.image.load("img/message.png").convert_alpha()
game_start = pg.transform.scale(game_start, (200, 300))
game_start_rect = game_start.get_rect(center=(180, 320))


#function
def draw_floor():
    global floor_x_pos
    floor_x_pos -= 1
    if floor_x_pos <= -360:
        floor_x_pos = 0
    screen.blit(floor, (floor_x_pos, 540))
    screen.blit(floor, (floor_x_pos + 360, 540))
def create_pipe():
    rd_height = rd.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, rd_height))
    top_pipe = pipe_surface.get_rect(midtop=(400, rd_height - 480))
    return bottom_pipe, top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return [pipe for pipe in pipes if pipe.right > 0]
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 540:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pg.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 540:
        return False
    return True
def rotate_bird(bird):
    new_bird = pg.transform.rotozoom(bird, -bird_movement * 4, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect 
def score_display():
    global score, height_score
    if running:
        score += 1
        score_surface = game_font.render(f'Score: {int(score // 100)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(180, 80))
        screen.blit(score_surface, score_rect)
        if score % 100 == 0:
            point_sound.play()
        height_score = max(height_score, int(score // 100))
    else:
        screen.blit(game_start, game_start_rect)

        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(180, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {height_score}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(180, 100))
        screen.blit(high_score_surface, high_score_rect)

flap_sound = pg.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pg.mixer.Sound("sound/sfx_hit.wav")
point_sound = pg.mixer.Sound("sound/sfx_point.wav")
die_sound = pg.mixer.Sound("sound/sfx_die.wav")
# main
def main():
    global running, floor_x_pos, bird_movement, bird_rect, pipe_list, bird, bird_index, bird_rect, score
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit();
                exit();
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and running:
                    bird_movement = -3.7 ;
                    flap_sound.play()
                if event.key == pg.K_SPACE and not running:
                    running = True;
                    pipe_list.clear();
                    bird_rect.center = (100, 280);
                    bird_movement = 0; 
                    score = 0;
                    die_sound.play()
            
            if event.type == spawn_pipe:
                pipe_list.extend(create_pipe())
            if event.type == bird_flap:
                bird_index = (bird_index + 1) % 3
                bird, bird_rect = bird_animation();
        screen.blit(bg, (0, 0));
        if running:
            bird_movement += g;
            rotated_bird = rotate_bird(bird);
            bird_rect.centery += bird_movement;
            screen.blit(rotated_bird, bird_rect);
            pipe_list = move_pipes(pipe_list);
            draw_pipes(pipe_list);
            running = check_collision(pipe_list); 
        score_display();
        draw_floor();
        pg.display.update();
        clock.tick(FPS);
if __name__ == "__main__":
    main()
    pg.quit()