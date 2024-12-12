#include <cinttypes>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <ranges>

void dict_add(std::unordered_map<int64_t, int64_t> &d, int64_t key, int64_t value) {
    if (const auto it = d.find(key); it != d.end()) {
        it->second += value;
    } else {
        d[key] = value;
    }
}

class Stones {
public:
    explicit Stones(const std::vector<int64_t> &from_vec) {
        for (const auto &value: from_vec) {
            add(value, 1);
        }
    }

    void add(const int64_t key, const int64_t value) {
        dict_add(data_, key, value);
    }

    int64_t sum() const {
        int64_t result{0};
        for (const auto &value: std::views::values(data_)) {
            result += value;
        }
        return result;
    }

    void blink() {
        std::unordered_map<int64_t, int64_t> next_stones{};
        for (auto &[value, count]: data_) {
            if (value == 0) {
                dict_add(next_stones, 1, count);
                continue;
            }

            auto value_str = std::to_string(value);
            if (value_str.length() % 2 == 0) {
                auto mid = value_str.length() / 2;

                dict_add(next_stones, stoll(value_str.substr(0, mid)), count);
                dict_add(next_stones, stoll(value_str.substr(mid)), count);
                continue;
            }

            dict_add(next_stones, value * 2024, count);
        }
        data_ = std::move(next_stones);
    }

private:
    std::unordered_map<int64_t, int64_t> data_{};
};

std::vector<std::string> split(const std::string &s, const std::string &delimiter) {
    size_t pos_start = 0;
    size_t pos_end;
    size_t delim_len = delimiter.length();

    std::vector<std::string> res{};
    while ((pos_end = s.find(delimiter, pos_start)) != std::string::npos) {
        std::string token = s.substr(pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back(token);
    }
    res.push_back(s.substr(pos_start));
    return res;
}

int main(int argc, char **argv) {
    std::ifstream ifs(argc > 1 ? argv[1] : "sample.txt");
    ifs.seekg(0, std::ios::end);
    std::string input(ifs.tellg(), 0);
    ifs.seekg(0, std::ios::beg);
    ifs.read(input.data(), static_cast<std::streamsize>(input.size()));

    std::vector<int64_t> input_data{};
    for (const auto& v : split(input, " ")) {
        input_data.push_back(stoll(v));
    }
    Stones stones(input_data);

    for (int i = 1; i <= 75; i++) {
        stones.blink();

        switch (i) {
            case 25:
                std::cout << "p1: " << stones.sum() << std::endl;
                break;
            case 75:
                std::cout << "p2: " << stones.sum() << std::endl;
                break;

            default:
                break;
        }
    }

    return 0;
}
