#include <regex>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <span>
#include <unordered_set>
#include <vector>

// Change this to print more logs
constexpr bool kIsVerbose = false;

uint64_t pack(const uint8_t shifts, const uint64_t value) {
    return shifts | value << 8;
}

void unpack(const uint64_t packed, uint8_t &shifts, uint64_t &value) {
    shifts = packed & 0xFF;
    value = packed >> 8;
}

namespace Jixun::AoC2024D17::Simulation {
    constexpr uint8_t kInstADV = 0;
    constexpr uint8_t kInstBXL = 1;
    constexpr uint8_t kInstBST = 2;
    constexpr uint8_t kInstJNZ = 3;
    constexpr uint8_t kInstBXC = 4;
    constexpr uint8_t kInstOUT = 5;
    constexpr uint8_t kInstBDV = 6;
    constexpr uint8_t kInstCDV = 7;

    constexpr size_t kRegA = 0;
    constexpr size_t kRegB = 1;
    constexpr size_t kRegC = 2;

    uint64_t run_ex(const std::span<uint8_t> program, const uint64_t valueA = 0, const uint64_t valueB = 0,
                    const uint64_t valueC = 0) {
        using namespace Jixun::AoC2024D17::Simulation;
        uint64_t result{0};
        uint64_t regs[3] = {valueA, valueB, valueC};

        auto read_operand = [&](const uint8_t operand) -> uint64_t {
            if (operand <= 3) {
                return operand;
            }
            return regs[operand - 4];
        };

        int bits{0};
        const size_t max_pc = program.size();
        for (size_t pc{0}; pc < max_pc;) {
            switch (program[pc++]) {
                case kInstADV:
                    regs[kRegA] = regs[kRegA] >> read_operand(program[pc++]);
                    break;
                case kInstBDV:
                    regs[kRegB] = regs[kRegA] >> read_operand(program[pc++]);
                    break;
                case kInstCDV:
                    regs[kRegC] = regs[kRegA] >> read_operand(program[pc++]);
                    break;

                case kInstBXL:
                    regs[kRegB] ^= read_operand(program[pc++]);
                    break;

                case kInstBXC:
                    regs[kRegB] ^= regs[kRegC];
                    pc++;
                    break;

                case kInstBST:
                    regs[kRegB] = read_operand(program[pc++]) % 8;
                    break;

                case kInstJNZ:
                    pc = regs[kRegA] ? read_operand(program[pc]) : pc + 1;
                    break;

                case kInstOUT:
                    result |= (read_operand(program[pc++]) & 7) << bits;
                    bits += 3;
                    break;

                default:
                    return UINT64_MAX; // invalid opcode
            }
        }

        assert(bits <= 255 && "too many bits?!");

        return pack(bits, result);
    }


    uint64_t run(const std::span<uint8_t> program, const uint64_t valueA = 0, const uint64_t valueB = 0,
                 const uint64_t valueC = 0) {
        uint64_t result{0};
        uint8_t bits{0};
        unpack(run_ex(program, valueA, valueB, valueC), bits, result);
        return result;
    }
}

std::unordered_set<uint64_t> reverse_search(const std::span<uint8_t> program, const uint64_t lookup_value,
                                            const uint64_t octal_digits) {
    using Jixun::AoC2024D17::Simulation::run;

    std::deque<uint64_t> work{}; // value, window_shifts
    for (uint64_t i = 0; i < 077; i++) {
        work.emplace_back(pack(0, i));
    }

    uint8_t window_shifts{};
    uint64_t test_input{};
    std::unordered_set<uint64_t> visited{};
    const uint64_t expected_wnd_shifts = (octal_digits - 2) * 3;

    std::unordered_set<uint64_t> results{};
    for (; !work.empty(); work.pop_front()) {
        auto work_key = work.front();
        unpack(work_key, window_shifts, test_input);
        if (visited.contains(work_key)) {
            continue;
        }
        visited.insert(work_key);

        const auto test_input_base = test_input >> window_shifts;
        const auto expected_digit = static_cast<uint8_t>((lookup_value >> window_shifts) % 8);

#ifndef NDEBUG
        {
            const auto width = window_shifts / 3 + 2;
            std::cout << "scan for 0o?" << std::setw(width) << std::setfill('0') << std::oct << test_input
                    << ", digit = " << static_cast<int>(expected_digit) << "..." << std::endl;
        }
#endif

        // not sure why 8 does not work, but 16 works...
        for (uint64_t prefix = 0; prefix < 16; ++prefix) {
            // auto result = run_prog(test_window);
            const auto actual_digit = static_cast<uint8_t>(run(program, (prefix << 6) | test_input_base) & 7);

            if (expected_digit != actual_digit) {
                continue;
            }

            auto real_input = ((prefix << 6) << window_shifts) | test_input;
            if (window_shifts == expected_wnd_shifts) {
                if (lookup_value == run(program, real_input)) {
                    results.insert(real_input);
                }
            } else if (window_shifts < expected_wnd_shifts) {
                work.emplace_back(pack(window_shifts + 3, real_input));
            }
        }
    }

    return results;
}

std::vector<uint64_t> extract_digits(const std::string &input) {
    const std::regex re(R"(\d+)");
    const std::sregex_iterator begin(input.begin(), input.end(), re);
    const std::sregex_iterator end;
    std::vector<uint64_t> result{};
    result.reserve(input.length() / 4);
    for (auto it = begin; it != end; ++it) {
        result.push_back(std::stoull(it->str()));
    }
    return result;
}

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
    auto numbers = extract_digits(input);

    std::vector<uint8_t> program(numbers.size() - 3);
    std::copy(numbers.cbegin() + 3, numbers.cend(), program.begin());

    // p1
    {
        using Jixun::AoC2024D17::Simulation::run_ex;
        uint8_t bits;
        uint64_t p1_result;
        unpack(run_ex(program, numbers[0], numbers[1], numbers[2]), bits, p1_result);
        std::cout << "simulation: 0o" << std::setfill('0') << std::setw(bits / 3) << std::oct << numbers[0] << " -> 0o"
                << std::setfill('0') << std::setw(bits / 3) << std::oct << p1_result << std::endl;

        char comma = ' ';
        printf("p1:");
        while (p1_result) {
            printf("%c%o", comma, static_cast<int>(p1_result % 8));
            p1_result >>= 3;
            comma = ',';
        }
        printf("\n");
    }

    // p2
    {
        uint64_t expected_value{0};
        int expected_bits{0};
        for (const auto &b: program) {
            expected_value |= static_cast<uint64_t>(b) << expected_bits;
            expected_bits += 3;
        }

#ifndef NDEBUG
        std::cout << "reverse search: 0o" << std::setfill('0') << std::setw(expected_bits / 3) << std::oct
                << expected_value << std::endl;
#endif

        if (auto r = reverse_search(program, expected_value, expected_bits / 3); !r.empty()) {
            auto sorted_results = std::vector(r.cbegin(), r.cend());
            std::ranges::sort(sorted_results);
            std::cout << "p2: " << sorted_results[0] << std::endl;
        } else {
            std::cout << "p2: no solution found!" << std::endl;
        }
    }

    return 0;
}
