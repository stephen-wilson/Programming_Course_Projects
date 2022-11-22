#!/usr/bin/env python3

##################
# Game Constants #
##################

# other than TILE_SIZE, feel free to move, modify, or delete these constants as
# you see fit.

TILE_SIZE = 128

# vertical movement
GRAVITY = -9
MAX_DOWNWARD_SPEED = -48
# PLAYER_JUMP_SPEED = 62
PLAYER_JUMP_SPEED = 53
PLAYER_JUMP_DURATION = 3
PLAYER_BORED_THRESHOLD = 60

# horizontal movement
PLAYER_DRAG = 6
PLAYER_MAX_HORIZONTAL_SPEED = 48
PLAYER_HORIZONTAL_ACCELERATION = 10


# the following maps single-letter strings to the name of the object they
# represent, for use with deserialization in Game.__init__.
SPRITE_MAP = {
    "p": "player",
    "c": "cloud",
    "=": "floor",
    "B": "building",
    "C": "castle",
    "u": "cactus",
    "t": "tree",
}

TEXTURE_MAP = {
    'B': 'classical_building',
    'u': 'cactus',
    'C': 'castle',
    'c': 'cloud',
    '=': 'black_large_square',
    't': 'tree'
}


##########################
# Classes and Game Logic #
##########################


class Rectangle:
    """
    A rectangle object to help with collision detection and resolution.
    """

    def __init__(self, x, y, w, h):
        """
        Initialize a new rectangle.

        `x` and `y` are the coordinates of the bottom-left corner. `w` and `h`
        are the dimensions of the rectangle.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def __contains__(self, p):
        """
        Contains dunder method.
        """
        px, py = p
        return self.x <= px <= self.x + self.h and self.y <= py <= self.y + self.h

    def intersects(self, other):
        """
        Check whether `self` and `other` (another Rectangle) overlap.

        Rectangles are open on the top and right sides, and closed on the
        bottom and left sides; concretely, this means that the rectangle
        [0, 0, 1, 1] does not intersect either of [0, 1, 1, 1] or [1, 0, 1, 1].
        
        Check 
        """        
        return (self.x < other.x + other.w and self.x + self.w > other.x
            and self.y < other.y + other.h and self.y + self.h > other.y)

    @staticmethod
    def translation_vector(r1, r2):
        """
        Compute how much `r2` needs to move to stop intersecting `r1`.

        If `r2` does not intersect `r1`, return `None`.  Otherwise, return a
        minimal pair `(x, y)` such that translating `r2` by `(x, y)` would
        suppress the overlap. `(x, y)` is minimal in the sense of the "L1"
        distance; in other words, the sum of `abs(x)` and `abs(y)` should be
        as small as possible.

        When two pairs `(x1, y1)` and `(x2, y2)` are tied in terms of this
        metric, return the one whose first element has the smallest
        magnitude.
        """
        if not r2.intersects(r1):
            return None
        
        # subtract from 4 sides, L,R,U,D:
        candidate_vecs = [(0, r1.y - (r2.y + r2.h)), (0, (r1.y + r1.h) - r2.y),
                          (r1.x - (r2.x + r2.w), 0), ((r1.x + r1.w) - r2.x, 0)]
        
        temp_vecs = []
        for vec in candidate_vecs:
            if not Rectangle(r2.x + vec[0], r2.y + vec[1], r2.w, r2.h).intersects(r1):
                temp_vecs.append(vec)
        
        # print(temp_vecs)
        return min(temp_vecs, key=lambda x: (abs(x[1]) + abs(x[0])))


class Game:
    def __init__(self, level_map):
        """
        Initialize a new game, populated with objects from `level_map`.

        `level_map` is a 2D array of 1-character strings; all possible strings
        (and some others) are listed in the SPRITE_MAP dictionary.  Each
        character in `level_map` corresponds to a sprite of size `TILE_SIZE *
        TILE_SIZE`.

        This function is free to store `level_map`'s data however it wants.
        For example, it may choose to just keep a copy of `level_map`; or it
        could choose to read through `level_map` and extract the position of
        each sprite listed in `level_map`.

        Any choice is acceptable, as long as it works with the implementation
        of `timestep` and `render` below.
        """
        # might want to choose to store locations
        self.x_velocity = 0
        self.y_velocity = 0
        # self.x_acc = 0
        # self.y_acc = 0
        self.map = {}
        self.player_pos = []
        self.bored_time = PLAYER_BORED_THRESHOLD
        self.game_state = 'ongoing'
        
        for i in range(len(level_map)):
            for j in range(len(level_map[i])):
                token = level_map[i][j]
                if token in SPRITE_MAP:
                    coords = j * TILE_SIZE, (len(level_map) - 1 - i) * TILE_SIZE
                    if token == 'p':
                        self.player_pos = list(coords)
                    else:
                        self.map[coords] = token
        
    def event_handling(self, keys, events):
        """
        Handles key press events.
        """
        # find current events/currently pressed keys
        for key in keys:
            if key in events:
                events[key] = True
                
        if events['up']:
            self.y_velocity = PLAYER_JUMP_SPEED
        if events['left'] and events['right']:
            self.x_acc = 0
        elif events['left']:
            self.x_acc = -PLAYER_HORIZONTAL_ACCELERATION
        elif events['right']:
            self.x_acc = PLAYER_HORIZONTAL_ACCELERATION 
            
        # for idling animation
        if not (events['up'] or events['left'] or events['right']):
            self.bored_time -= 1
        else:
            self.bored_time = PLAYER_BORED_THRESHOLD
            
    def apply_drag(self, events):
        """
        Apply drag to the velocity.
        """
        # direction of velocity
        if self.x_velocity == 0:
            vel_sign = 0
        else:
            vel_sign = -1 if self.x_velocity < 0 else 1
            
        # print(f'before: {self.x_velocity}')
        if not events['left'] and not events['right']:
            # apply drag
            if PLAYER_DRAG >= abs(self.x_velocity):
                self.x_velocity -= self.x_velocity
            else:
                self.x_velocity += -vel_sign * PLAYER_DRAG
                
        self.x_velocity = vel_sign * min(PLAYER_MAX_HORIZONTAL_SPEED, abs(self.x_velocity))

    def resolve_collisions(self):
        """
        Resolve the collisions between *only* dynamic and static sprites.
        
        Algorithm (from writeup):
        # Resolve vertical collisions first
        for each dynamic sprite s1 and each static sprite s2:
        if s1 and s2 intersect:
            v = minimal translation vector for s1 to stop intersecting s2
            if v is vertical:
                move s1 along v

        # Resolve horizontal collisions second
        for each dynamic sprite s1 and each static sprite s2:
        if s1 and s2 intersect:
            move s1 along the minimal translation vector to stop intersecting s2
        """
        sign = lambda x: x / abs(x)
        player_bound = Rectangle(self.player_pos[0], self.player_pos[1], TILE_SIZE, TILE_SIZE)
        # vertical collision resolution
        for sprite_pos in self.map:
            sprite = Rectangle(sprite_pos[0], sprite_pos[1], TILE_SIZE, TILE_SIZE)
            if player_bound.intersects(sprite):
                # check if the player is intersecting the castle (victory state)
                if self.map[sprite_pos] == 'C':
                    self.game_state = 'victory'
                elif self.map[sprite_pos] == 'u':
                    self.game_state = 'defeat'
                
                v = Rectangle.translation_vector(sprite, player_bound)
                if v[0] == 0:
                    self.player_pos[1] += v[1]
                    player_bound.y += v[1]
                    if self.y_velocity != 0 and v[1] != 0 and sign(self.y_velocity) != sign(v[1]):
                        self.y_velocity = 0
            
        # horizontal collision resolution
        for sprite_pos in self.map:
            sprite = Rectangle(sprite_pos[0], sprite_pos[1], TILE_SIZE, TILE_SIZE)
            if player_bound.intersects(sprite):
                v = Rectangle.translation_vector(sprite, player_bound)
                self.player_pos[0] += v[0]
                if self.x_velocity != 0 and v[0] != 0 and sign(self.x_velocity) != sign(v[0]):
                    self.x_velocity = 0
                

    def timestep(self, keys):
        """
        Simulate the evolution of the game state over one time step.  `keys` is
        a list of currently pressed keys.
        """
        if self.game_state == 'ongoing':
            # accelerations reset to 0 each time step
            self.x_acc = 0
            self.y_acc = 0
            events = {'up': False,
                    'left': False,
                    'right': False,
                    }
            
            # gravity acceleration calculation
            self.y_velocity = max(self.y_velocity + GRAVITY, MAX_DOWNWARD_SPEED)
            
            self.event_handling(keys, events)
                
            self.x_velocity += self.x_acc
            
            self.apply_drag(events)    
            
            self.player_pos[0] += self.x_velocity
            self.player_pos[1] += self.y_velocity
            
            self.resolve_collisions()
            
            # check for out of bounds
            if self.player_pos[1] < -TILE_SIZE:
                self.game_state = 'defeat'
                
        

    def get_game_state(self):
        """
        Determines the state of the game.
        rType::Str
        """
        return 'ongoing' # for now

    def render(self, w, h):
        """
        Report status and list of sprite dictionaries for sprites with a
        horizontal distance of w//2 from player.  See writeup for details.
        rType::Tuple[str, List[Dict]]
        """
        # state = self.get_game_state()
        px,py = self.player_pos
        render_map = (self.game_state, []) # for now can be at 'ongoing' until later in the lab
        # set texture
        if self.game_state == 'victory':
            texture = 'partying_face'
        elif self.game_state == 'defeat':
            texture = 'injured'
        else:
            texture = 'slight_smile' if self.bored_time >= 0 else 'sleeping'
        
        if -TILE_SIZE < py < h:
            render_map[1].append({'texture': texture,
                            'pos': self.player_pos,
                            'player': True})
        for (bx, by) in self.map:
            # if px - w//2 - TILE_SIZE < bx < px + w//2 and -TILE_SIZE < by < h:
            if Rectangle(bx, by, TILE_SIZE, TILE_SIZE).intersects(Rectangle(px - w//2,-TILE_SIZE,w,h)):
                render_map[1].append({'texture': TEXTURE_MAP[self.map[(bx,by)]],
                                      'pos': (bx,by),
                                      'player': False})
                
        return render_map


if __name__ == "__main__":
    pass
