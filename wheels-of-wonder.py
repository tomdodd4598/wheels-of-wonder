# -------------------------------#
# ========== SETTINGS ========== #
# -------------------------------#

# Note: initial positions are counted clockwise from the bottom for the left wheel/console,
# and anti-clockwise from the bottom for the right wheel/console, zero-indexed.

# Note: left wheel is numbered 0, right wheel is numbered 1.

# Number of positions on the wheels and their respective consoles.
wheel_size_left = 6  # default = 6
wheel_size_right = 6  # default = 6

# Starting wheel and position of the crystal ball.
start_wheel = 0  # default = 0
start_position = 0  # default = 0

# Target wheel and position the crystal ball must fall through.
target_wheel = 1  # default = 1
target_position = 4  # default = 4

# Positions on the wheels which can hold the crystal ball.
holding_positions_left = [0, 2, 4]  # default = [0, 2, 4]
holding_positions_right = [1, 3, 5]  # default = [1, 3, 5]

# Jump points and targets from left to right and right to left.
jumps_left_to_right = {0: 0, 3: 3, 4: 4, 5: 5}  # default = {0: 0, 3: 3, 4: 4, 5: 5}
jumps_right_to_left = {0: 0, 3: 3, 4: 4, 5: 5}  # default = {0: 0, 3: 3, 4: 4, 5: 5}

# Positions on the console which can not hold a peg
blocked_pegs_left = [0, 2]  # default = [0, 2]
blocked_pegs_right = [0]  # default = [0]

# -------------------------------#
# ========== INTERNAL ========== #
# -------------------------------#

set_holding_positions_left = set(holding_positions_left)
set_holding_positions_right = set(holding_positions_right)

set_blocked_pegs_left = set(blocked_pegs_left)
set_blocked_pegs_right = set(blocked_pegs_right)

available_pegs_left = set(range(wheel_size_left)) - set_blocked_pegs_left
available_pegs_right = set(range(wheel_size_right)) - set_blocked_pegs_right


class Wheel:
    def __init__(self, size, raw_holding_positions: set):
        self.size = size
        self.raw_holding_positions = raw_holding_positions
        self.rotation = 0

    def rotate(self):
        self.rotation += 1
        self.rotation %= self.size

    def is_holding_position(self, position):
        position += (self.size - self.rotation)
        return position % self.size in self.raw_holding_positions


class Console:
    def __init__(self, size, pegs: set):
        self.size = size
        self.pegs = pegs
        self.current_position = 0

    def increment_position(self):
        self.current_position += 1
        self.current_position %= self.size


class Puzzle:
    def __init__(self, wheel_left: Wheel, wheel_right: Wheel, console_left: Console, console_right: Console):
        self.wheel_left = wheel_left
        self.wheel_right = wheel_right
        self.console_left = console_left
        self.console_right = console_right
        self.ball_wheel = start_wheel
        self.ball_position = start_position

    def current_wheel(self):
        return self.wheel_left if self.ball_wheel == 0 else self.wheel_right

    def current_console(self):
        return self.console_left if self.ball_wheel == 0 else self.console_right

    def get_jumps(self) -> dict:
        return jumps_left_to_right if self.ball_wheel == 0 else jumps_right_to_left

    def try_jump(self):
        console = self.current_console()
        if console.current_position in console.pegs:
            jumps = self.get_jumps()
            if self.ball_position in jumps:
                self.ball_position = jumps[self.ball_position]
                self.ball_wheel = 1 - self.ball_wheel
                console.pegs.remove(console.current_position)
                wheel = self.current_wheel()
                if wheel.is_holding_position(self.ball_position):
                    return 0
                if self.ball_wheel == target_wheel and self.ball_position == target_position:
                    return 1
                return -1
            return -1
        return 0

    def invalid_state(self):
        wheel = self.current_wheel()
        if not wheel.is_holding_position(self.ball_position):
            return True
        console = self.current_console()
        if len(console.pegs) == 0 or max(console.pegs) < console.current_position:
            return True
        return False

    def move(self):
        wheel = self.current_wheel()
        wheel.rotate()
        self.ball_position += (wheel.size - 1)
        self.ball_position %= wheel.size
        self.current_console().increment_position()

    def simulate(self):
        while True:
            while True:
                jump = self.try_jump()
                if jump == 1:
                    return len(self.console_left.pegs) == 0 and len(self.console_right.pegs) == 0
                if jump == -1:
                    return False
                break
            if self.invalid_state():
                return False
            self.move()


def subsets(s, n):
    import itertools
    return map(lambda x: set(x), itertools.combinations(s, n))


def is_solution(pegs_left, pegs_right):
    wheel_left = Wheel(wheel_size_left, set_holding_positions_left)
    wheel_right = Wheel(wheel_size_right, set_holding_positions_right)
    console_left = Console(wheel_size_left, pegs_left)
    console_right = Console(wheel_size_right, pegs_right)
    return Puzzle(wheel_left, wheel_right, console_left, console_right).simulate()


def main():
    for i in range(0, 1 + len(available_pegs_left)):
        for j in range(0, 1 + len(available_pegs_right)):
            for left in subsets(available_pegs_left, i):
                for right in subsets(available_pegs_right, j):
                    if is_solution(left.copy(), right.copy()):
                        print(list(left), list(right))


if __name__ == '__main__':
    main()
