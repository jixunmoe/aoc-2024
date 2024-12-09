#include <cinttypes>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

constexpr int16_t kEmptyItem = -1;

class Disk {
public:
    explicit Disk(std::string &input) {
        std::vector buffer(input.length() * 9, kEmptyItem);
        std::vector<std::pair<size_t, size_t> > block_pos_sizes;
        block_pos_sizes.reserve(input.length() / 2 + 1);

        bool is_free = true;
        int16_t block_id = 0;
        size_t offset = 0;
        for (const char &c: input) {
            // filter invalid characters
            if (!isdigit(c)) {
                continue;
            }

            is_free = !is_free;
            size_t block_len = static_cast<size_t>(c) - '0';
            if (!is_free) {
                std::fill_n(buffer.begin() + static_cast<int>(offset), block_len, block_id);
                block_pos_sizes.emplace_back(offset, block_len);
                block_id++;
            }
            offset += block_len;
        }
        buffer.resize(offset);

        max_block_id_ = static_cast<int16_t>(block_id - 1);
        data_ = std::move(buffer);
        pos_data_ = std::move(block_pos_sizes);
    }

    uint64_t checksum() {
        uint64_t checksum = 0;
        uint64_t idx = 0;
        for (auto it = data_.begin(); it != data_.end(); ++it, ++idx) {
            if (*it != -1) {
                checksum += idx * *it;
            }
        }
        return checksum;
    }

    [[nodiscard]] Disk compact_v1() const {
        Disk disk(*this);
        disk.compact_v1_mut();
        return disk;
    }

    [[nodiscard]] Disk compact_v2() const {
        Disk disk(*this);
        disk.compact_v2_mut();
        return disk;
    }

    void compact_v1_mut() {
        auto left = data_.begin();
        auto right = data_.rbegin();
        while (left < right.base()) {
            if (*left != kEmptyItem) {
                ++left;
                continue;
            }
            if (*right == kEmptyItem) {
                ++right;
                continue;
            }
            *left = *right;
            *right = kEmptyItem;
        }
    }

    void compact_v2_mut() {
        for (int16_t block_id{max_block_id_}; block_id >= 0; --block_id) {
            auto [blk_idx, blk_len] = pos_data_[block_id];

            int continues_free = 0;
            auto end = data_.begin() + static_cast<int>(blk_idx);
            for (auto it = data_.begin(); it != end; ++it) {
                if (*it == -1) {
                    continues_free++;
                } else {
                    continues_free = 0;
                }
                if (continues_free == blk_len) {
                    std::fill_n(it + 1 - continues_free, blk_len, block_id);
                    std::fill_n(data_.begin() + static_cast<int>(blk_idx), blk_len, -1);
                    break;
                }
            }

            // printf("blk=%d, idx=%d -- ", block_id % 10, blk_idx);
            // print();
        }
    }

    void print() const {
        for (const auto &c: data_) {
            const char ch = c == -1 ? '.' : static_cast<char>('0' + c % 10);
            putchar(ch);
        }
        putchar('\n');
    }

private:
    int16_t max_block_id_{-1};
    std::vector<int16_t> data_{};
    std::vector<std::pair<size_t, size_t> > pos_data_{};
};

int main(int argc, char **argv) {
    std::string input_path = argc > 1 ? argv[1] : "sample.txt";

    std::ifstream ifs(input_path);
    ifs.seekg(0, std::ios::end);
    std::string input(ifs.tellg(), 0);
    ifs.seekg(0, std::ios::beg);
    ifs.read(input.data(), static_cast<std::streamsize>(input.size()));

    const Disk disk(input);
    const auto p1 = disk.compact_v1().checksum();
    const auto p2 = disk.compact_v2().checksum();

    printf("p1: %" PRIu64 "\n", p1);
    printf("p2: %" PRIu64 "\n", p2);

    return 0;
}
