import os
import neat
import visualize
import math
import random as rand
import pygame as pg

import Player, Enemy, Coin
import Var

os.environ["PATH"] += os.pathsep + 'D:/Graphviz/bin'

pg.init()
pg.font.init()

pg.display.set_caption("Jump ML with Coins")

clock = pg.time.Clock()

WIN = pg.display.set_mode((Var.SCREEN_WIDTH, Var.SCREEN_HEIGHT))

FONT = pg.font.SysFont("comicsans", 40)

player = Player.Player(100, 425, 50, 50, WIN)
enemy = Enemy.Enemy(Var.SCREEN_WIDTH, 400, 50, 75, WIN)
coin = Coin.Coin(rand.randint(50, Var.SCREEN_WIDTH - 50), 300, 30, 30, WIN)

def draw_window(score, max_score, players, enemies, coins):
    """ Draws all the objects and text on screen """
    WIN.fill(Var.WHITE)

    # GROUND #
    pg.draw.rect(WIN, Var.BLACK, (0, 475, Var.SCREEN_WIDTH, 600))

    player.draw_players(players)
    enemy.draw_mult(enemies)
    coin.draw_mult(coins)

    score_text = FONT.render("Total Gen Score: " + str(score), 1, Var.BLACK)
    max_score_text = FONT.render("Total Gen Max Score: " + str(max_score), 1, Var.BLACK)

    WIN.blit(score_text, (10, 10))
    WIN.blit(max_score_text, (10, 40))

def handle_collision(players, enemies, coins, score):
    """ 
    Checks to see if a player collides with an enemy or coin
    Decreases player fitness if enemy collision occurs
    Increases player fitness and score if coin collision occurs
    and the coin is removes
    """
    for enemy in enemies:
        for x, player in enumerate(players):
            if enemy.check_collision(player, enemy):
                ge[x].fitness -= 3
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
    for coin in coins:
        for x, player in enumerate(players):
            if coin.check_collision(player, coin):
                pg.event.post(pg.event.Event(COIN_HIT))
                ge[x].fitness += 1
                score += 1
                coin.delete = True
    coins[:] = [coin for coin in coins if not coin.delete]
    return score

def stats(players, ge):
    """ Displays how many players are alive and what the current generation is """
    alive_text = FONT.render(f'Players Alive:  {str(len(players))}', True, (0, 0, 0))
    gen_text = FONT.render(f'Generation:  {p.generation+1}', True, (0, 0, 0))
    WIN.blit(alive_text, (Var.SCREEN_WIDTH//2, 10))
    WIN.blit(gen_text, (Var.SCREEN_WIDTH//2, 40))

def distance(pos_a, pos_b):
    """ Calculates the distance between two objects """
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)

# Creates event for coin collision
COIN_HIT = pg.USEREVENT + 1

max_score = 0

def main(genomes, config):
    """ Handles the operation of the player learning to jump over the enemy and collecting coins"""
    global players, enemies, coins, ge, nets, max_score, score

    enemy = Enemy.Enemy(Var.SCREEN_WIDTH, 400, 50, 75, WIN)

    nets = []
    ge = []
    players = []
    enemies = []
    coins = []

    for g_id, g in genomes:
        players.append(Player.Player(100, 425, 50, 50, WIN))
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ge.append(g)
        g.fitness = 0

    score = 0

    running = True
    while running:
        clock.tick(75)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        for x, player in enumerate(players):
            player.update_player()
            for enemy in enemies:
                for coin in coins:
                    output = nets[x].activate(
                        (
                            player.x,
                            player.y,
                            distance((player.x, player.y), enemy.rect.midtop),
                            distance((player.x, player.y), coin.rect.center)
                        )
                    )
                    if output[0] > 0.5:
                        player.jump()
                    if output[1] > 0.5:
                        player.move_left()
                    if output[2] > 0.5:
                        player.move_right()

        # Sets the max score
        if score > max_score:
                max_score = score

        # Spawns an enemy when there are no enemies on screen
        if len(enemies) == 0:
            enemies.append(enemy)
        
        # Moves to next generation when there are no players left
        if len(players) == 0:
            break
        
        # Creates ten coins on screen
        if len(coins) < 10:
            coins.append(Coin.Coin(rand.randint(50, Var.SCREEN_WIDTH - 50), 300, 30, 30, WIN))

        draw_window(score, max_score, players, enemies, coins)

        enemy.move_enemies(enemies)

        ge = enemy.out_enemy(enemies, ge)

        score = handle_collision(players, enemies, coins, score)
        
        stats(players, ge)

        pg.display.update()

# ML #
def run(config_path):
    """ 
    Sets up NEAT and displays statistics
    Creates visualizations after last generation
    """
    global p

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))

    node_names = {-1:'Player x-value', -2: 'Player y-value', -3:'Player dist from coin', -4: 'Player dist from enemy', 0:'Jump', 1:'Move left', 2:'Move right'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat")
    run(config_path)
