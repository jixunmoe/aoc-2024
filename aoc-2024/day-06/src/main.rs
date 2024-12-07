use std::{env, fs};

const DIR_UP: u8 = b'^';
const DIR_DOWN: u8 = b'v';
const DIR_LEFT: u8 = b'<';
const DIR_RIGHT: u8 = b'>';
const WALL: u8 = b'#';
const EMPTY: u8 = b'.';
const EXIT: u8 = 0;

const MAX_WIDTH: usize = 256;
const MAX_HEIGHT: usize = 256;

const BIT_UP: u8 = 1;
const BIT_DOWN: u8 = 2;
const BIT_LEFT: u8 = 4;
const BIT_RIGHT: u8 = 8;

fn dir_to_mask(dir: u8) -> u8 {
    match dir {
        DIR_UP => BIT_UP,
        DIR_DOWN => BIT_DOWN,
        DIR_LEFT => BIT_LEFT,
        DIR_RIGHT => BIT_RIGHT,
        _ => panic!("Invalid direction"),
    }
}

fn rotate_right(dir: u8) -> u8 {
    match dir {
        BIT_UP => BIT_RIGHT,
        BIT_RIGHT => BIT_DOWN,
        BIT_DOWN => BIT_LEFT,
        BIT_LEFT => BIT_UP,
        _ => panic!("Invalid direction"),
    }
}

struct Game {
    board: [[u8; MAX_WIDTH]; MAX_HEIGHT],
    player_x: usize,
    player_y: usize,
    player_dir: u8,
}

enum WalkResult {
    HitWall,
    NewPos(usize, usize),
    Exit,
}

impl Game {
    pub fn new() -> Game {
        Game {
            board: [[0; MAX_WIDTH]; MAX_HEIGHT],
            player_x: 0,
            player_y: 0,
            player_dir: 0,
        }
    }

    pub fn load(&mut self, data: &str) {
        for (y, line) in data.split('\n').enumerate() {
            for (x, &c) in line.as_bytes().iter().enumerate() {
                let is_player = c == DIR_UP || c == DIR_DOWN || c == DIR_LEFT || c == DIR_RIGHT;
                if is_player {
                    self.player_x = x;
                    self.player_y = y;
                    self.player_dir = dir_to_mask(c);
                    self.board[y][x] = EMPTY;
                } else {
                    self.board[y][x] = c;
                }
            }
        }
    }

    fn walk(
        &self,
        board: &[[u8; MAX_WIDTH]; MAX_HEIGHT],
        pos: (usize, usize),
        dir: u8,
    ) -> WalkResult {
        let (x, y) = pos;
        let (x, y) = match dir {
            BIT_UP => {
                if y == 0 {
                    return WalkResult::Exit;
                }
                (x, y - 1)
            }
            BIT_DOWN => (x, y + 1),
            BIT_LEFT => {
                if x == 0 {
                    return WalkResult::Exit;
                }
                (x - 1, y)
            }
            BIT_RIGHT => (x + 1, y),
            _ => panic!("Invalid direction"),
        };

        if x >= MAX_WIDTH || y >= MAX_HEIGHT {
            return WalkResult::Exit;
        }

        match board[y][x] {
            EXIT => WalkResult::Exit,
            WALL => WalkResult::HitWall,
            _ => WalkResult::NewPos(x, y),
        }
    }

    fn can_exit(
        &self,
        board: &[[u8; MAX_WIDTH]; MAX_HEIGHT],
        visited: &mut [[u8; MAX_WIDTH]; MAX_HEIGHT],
    ) -> bool {
        // let mut visited = [[0u8; MAX_WIDTH]; MAX_HEIGHT];
        visited[self.player_y][self.player_x] = self.player_dir;

        let mut pos = (self.player_x, self.player_y);
        let mut dir = self.player_dir;

        loop {
            match self.walk(board, pos, dir) {
                WalkResult::HitWall => {
                    dir = rotate_right(dir);
                }
                WalkResult::NewPos(x, y) => {
                    pos = (x, y);
                }
                WalkResult::Exit => return true,
            }

            let (x, y) = pos;
            if visited[y][x] & dir != 0 {
                // recursed
                return false;
            }
            visited[y][x] |= dir;
        }
    }

    pub fn solve(&self) -> (usize, usize) {
        let mut visited = [[0u8; MAX_WIDTH]; MAX_HEIGHT];
        self.can_exit(&self.board, &mut visited); // discard the result

        // don't bother with the player position.
        visited[self.player_y][self.player_x] = 0;

        let mut p1_answer = 1; // include the initial player position
        let mut p2_answer = 0;
        for (y, row) in visited.iter().enumerate() {
            for (x, &cell) in row.iter().enumerate() {
                // never visited, skip
                if cell == 0 {
                    continue;
                }

                p1_answer += 1;

                let mut board_copy = self.board;
                board_copy[y][x] = WALL;
                let mut tmp = [[0u8; MAX_WIDTH]; MAX_HEIGHT];
                if !self.can_exit(&board_copy, &mut tmp) {
                    p2_answer += 1;
                }
            }
        }

        (p1_answer, p2_answer)
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let input_file = args.get(1).unwrap_or("sample.txt".into());

    let input = fs::read_to_string(input_file).expect("Cannot read input file");
    let mut game = Game::new();
    game.load(input.trim());
    let (p1, p2) = game.solve();
    println!("Part 1: {}", p1);
    println!("Part 2: {}", p2);
}
