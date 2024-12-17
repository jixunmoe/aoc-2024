#include <cstdint>
#include <fstream>
#include <cstring>
#include <deque>
#include <unordered_map>
#include <unordered_set>
#include <vector>

constexpr uint8_t kEmpty = ' ';
constexpr uint8_t kWall = '#';

constexpr uint8_t kDirNorth = 0;
constexpr uint8_t kDirEast = 1;
constexpr uint8_t kDirSouth = 2;
constexpr uint8_t kDirWest = 3;

struct position_t {
    uint8_t x;
    uint8_t y;
};

// board size: 141x141, use 256x256 to make addressing faster.
constexpr size_t kMaxWidth = 256;
constexpr size_t kMaxHeight = 256;

typedef uint8_t board_t[kMaxHeight][kMaxWidth];

typedef uint32_t node_t;
typedef uint64_t node_with_cost_t;

inline node_t make_node(const uint8_t x, const uint8_t y, const uint8_t direction = 0) {
    return static_cast<node_t>(direction) << 16 | static_cast<node_t>(x) << 8 | static_cast<node_t>(y);
}

inline void parse_node(uint8_t &x, uint8_t &y, uint8_t &direction, const node_t key) {
    direction = static_cast<uint8_t>(key >> 16);
    x = static_cast<uint8_t>(key >> 8);
    y = static_cast<uint8_t>(key);
}

inline node_with_cost_t make_node_with_cost(const uint8_t x, const uint8_t y, const uint8_t direction,
                                            const uint32_t cost) {
    return static_cast<node_with_cost_t>(cost) << 32 | static_cast<node_with_cost_t>(make_node(x, y, direction));
}

inline void parse_node_with_cost(uint8_t &x, uint8_t &y, uint8_t &direction, uint32_t &cost,
                                 const node_with_cost_t node) {
    cost = static_cast<uint32_t>(node >> 32);
    parse_node(x, y, direction, static_cast<node_t>(node));
}

uint8_t normalize_direction(const uint8_t direction) {
    return direction & 3;
}

class Board {
public:
    explicit Board(const std::string &input) {
        memset(board_, kWall, sizeof(board_));

        size_t x = 0, y = 0;
        size_t width = 0;
        for (const char c: input) {
            switch (c) {
                case 0:
                case '\r': break;

                case '\n':
                    ++y;
                    width = x;
                    x = 0;
                    break;
                case '.':
                    board_[y][x++] = kEmpty;
                    break;
                case '#':
                    board_[y][x++] = kWall;
                    break;
                case 'S':
                    start_ = {static_cast<uint8_t>(x), static_cast<uint8_t>(y)};
                    board_[y][x++] = kEmpty;
                    break;
                case 'E':
                    end_ = {static_cast<uint8_t>(x), static_cast<uint8_t>(y)};
                    board_[y][x++] = kEmpty;
                    break;
                default:
                    printf("invalid character: %c (0x%02x)\n", isprint(c) ? c : '.', static_cast<int>(c));
            }
        }

        size_ = {static_cast<uint8_t>(width), static_cast<uint8_t>(y)};
    }

    [[nodiscard]] std::pair<std::unordered_map<node_t, uint32_t>, std::unordered_map<node_t, std::vector<node_t> > >
    build_dijkstra() const {
        std::unordered_map<node_t, uint32_t> costs{};
        std::unordered_map<node_t, std::vector<node_t> > parents{};

        std::deque work{make_node_with_cost(start_.x, start_.y, kDirEast, 0)};


        //                            N   E  S   W
        constexpr int8_t dx_list[] = {+0, 1, 0, -1};
        constexpr int8_t dy_list[] = {-1, 0, 1, +0};

        auto explore_node = [&](const node_t current_node, const uint8_t x, const uint8_t y, const uint8_t new_dir,
                                const uint32_t new_cost) {
            if (board_[y][x] == kWall) {
                return;
            }

            // ReSharper disable once CppTooWideScopeInitStatement
            const auto next_node = make_node(x, y, new_dir);

            if (!costs.contains(next_node) || new_cost < costs[next_node]) {
                costs[next_node] = new_cost;
                parents[next_node] = {current_node};
                work.push_back(make_node_with_cost(x, y, new_dir, new_cost));
            } else if (new_cost == costs[next_node]) {
                parents[next_node].push_back(current_node);
            }
        };


        uint8_t cx, cy, cd;
        uint32_t cost;
        for (; !work.empty(); work.pop_front()) {
            const auto current_node = static_cast<node_t>(work.front());
            parse_node_with_cost(cx, cy, cd, cost, work.front());

            explore_node(current_node, cx + dx_list[cd], cy + dy_list[cd], cd, cost + 1);
            explore_node(current_node, cx, cy, normalize_direction(cd + 1), cost + 1000);
            explore_node(current_node, cx, cy, normalize_direction(cd + 3), cost + 1000);
        }

        return {costs, parents};
    }

    [[nodiscard]] std::pair<uint32_t, uint32_t> solve() const {
        auto [costs, parents] = build_dijkstra();

        uint32_t min_cost = UINT32_MAX;
        std::unordered_map<uint32_t, std::deque<node_t> > cache{};
        for (uint8_t i = 0; i < 4; i++) {
            auto const node = make_node(end_.x, end_.y, i);
            if (auto it = costs.find(node); it != costs.end()) {
                min_cost = std::min(min_cost, it->second);
                cache[it->second].push_back(node);
            }
        }

        // Did not find a path.
        if (min_cost == UINT32_MAX) {
            return {0, {}};
        }

        std::unordered_set visited{make_node(start_.x, start_.y), make_node(end_.x, end_.y)};
        uint8_t x, y, d;
        for (auto work = std::move(cache[min_cost]); !work.empty(); work.pop_front()) {
            const auto node = work.front();
            parse_node(x, y, d, node);

            for (const auto &parent_node: parents[node]) {
                visited.insert(make_node(x, y));
                work.push_back(parent_node);
            }
            parents[node].clear();
        }

        return {min_cost, static_cast<uint32_t>(visited.size())};
    }

private:
    position_t size_{};
    position_t start_{};
    position_t end_{};
    board_t board_{};
};

int main(const int argc, char **argv) {
    const char *input_file_path = argc > 1 ? argv[1] : "sample.txt";
    std::ifstream ifs(input_file_path);
    if (!ifs.is_open()) {
        printf("error: unable to open file %s\n", input_file_path);
        return 1;
    }

    ifs.seekg(0, std::ios::end);
    std::string input(ifs.tellg(), 0);
    ifs.seekg(0, std::ios::beg);
    ifs.read(input.data(), static_cast<std::streamsize>(input.size()));

    const Board board(input);
    const auto [p1, p2] = board.solve();
    printf("p1: %u\n", p1);
    printf("p2: %u\n", p2);

    return 0;
}
