from ursina import *

app = Ursina()

class AlienShip(Entity):
    def __init__(self):
        super().__init__(parent = scene, model = 'circle', texture = 'white_cube', y = 5, color = color.red, collider = 'box', x = random.uniform(-4, 5.5))
        self.x_mov = -2.5
        self.xlim = 6.5
        self.y_mov = -1

    def update(self):
        self.x += self.x_mov * time.dt
        if (self.x < -self.xlim) and (self.x_mov < 0):
            self.y += self.y_mov
            self.x_mov = -self.x_mov
        elif (self.x > self.xlim) and (self.x_mov > 0):
            self.y += self.y_mov 
            self.x_mov = -self.x_mov
        
        if random.randrange(1, 7_500) == 1:
            alien_bullets.append(AlienBullet(position = (self.x, self.y - .3)))
        
        if self.y < -6.5:
            quit()
        
        if bullets != []:
            for bullet in bullets:
                if self.intersects(bullet).hit:
                    destroy(self)
                    del alienships[alienships.index(self)]
                    destroy(bullet)
                    del bullets[bullets.index(bullet)]
        
        if self.intersects(player).hit:
            quit()

class Player(Entity):
    def __init__(self):
        super().__init__(parent = scene, model = 'circle', texture = 'white_cube', color = color.green, y = -3, collider = 'box')
        
    def update(self):
        if held_keys['left arrow']:
            self.x -= 2 * time.dt
        elif held_keys['right arrow']:
            self.x += 2 * time.dt

class Bullet(Entity):
    def __init__(self, position):
        super().__init__(parent = scene, model = 'quad', color = color.yellow, scale = (.2, .5), position = position, texture = 'white_cube', collider = 'box')
        
    def update(self):
        self.y += 5 * time.dt
        if self.y > 7:
            destroy(self)
            del bullets[bullets.index(self)]

class AlienBullet(Entity):
    def __init__(self, position):
        super().__init__(parent = scene, model = 'quad', color = color.orange, scale = (.2, .5), position = position, texture = 'white_cube', collider = 'box')
        
    def update(self):
        self.y -= 5 * time.dt
        if self.y < -7:
            destroy(self)
            del alien_bullets[alien_bullets.index(self)]

def input(key):
    if key == 'space':
        bullets.append(Bullet((player.x, player.y + 1)))

def update():
    if random.randrange(1, 300) == 1:
        alienships.append(AlienShip())
    
    if alien_bullets:        
        for alien_bullet in alien_bullets:
            if alien_bullet.intersects(player).hit:
                quit()

player = Player()
alienships = []
bullets = []
alien_bullets = []

app.run()