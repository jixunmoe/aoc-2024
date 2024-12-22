#include <array>
#include <cassert>
#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#define PRINT_PATTERNS (1)

std::vector<uint32_t> extract_code(const std::string &input) {
    std::vector<uint32_t> result;
    std::istringstream stream(input);
    std::string line;
    while (std::getline(stream, line)) {
        result.push_back(static_cast<uint32_t>(std::stoul(line)));
    }
    return result;
}

inline uint32_t derive_secret(uint32_t secret) {
    secret = (secret ^ (secret << 6)) & 0xFF'FFFF;
    secret = (secret ^ (secret >> 5)) & 0xFF'FFFF;
    secret = (secret ^ (secret << 11)) & 0xFF'FFFF;
    return secret;
}

constexpr size_t kPatternSize = 1 << 20;
constexpr uint32_t kPatternSizeMask = kPatternSize - 1;

inline uint32_t derive_secret_at(uint8_t *patterns, const uint32_t seed, const size_t n = 2000) {
    uint32_t cost_pattern{0};

    auto secret = seed;
    uint8_t secret_digit = seed % 10;
    for (size_t i = 0; i < n; i++) {
        const auto next_secret = derive_secret(secret);
        const auto next_secret_digit = static_cast<uint8_t>(next_secret % 10);
        const uint8_t price_delta = 9 + next_secret_digit - secret_digit; // always positive
        assert(((price_delta & 0b1110'0000) == 0) && "price_delta is too large!");

        cost_pattern = ((cost_pattern << 5) | price_delta) & kPatternSizeMask;
        if (i >= 3 && (patterns[cost_pattern] & 0x80) == 0) {
            patterns[cost_pattern] = next_secret_digit | 0x80;
        }

        secret = next_secret;
        secret_digit = next_secret_digit;
    }
    return secret;
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

    uint64_t p1{0};
    const auto initial_secrets = extract_code(input);

    std::vector<uint32_t> sums_container(kPatternSize);
    auto* sums = sums_container.data();

#if PRINT_PATTERNS
    std::vector<std::array<uint8_t, kPatternSize>> pattern_cache(initial_secrets.size());
    auto pattern_cache_it = pattern_cache.begin();
#else
    std::vector<uint8_t> pattern_cache(kPatternSize);
#endif

    for (const auto initial_secret : initial_secrets) {
#if PRINT_PATTERNS
        auto* patterns = pattern_cache_it++->data();
#else
        auto* patterns = pattern_cache.data();
        std::fill(pattern_cache.begin(), pattern_cache.end(), 0);
#endif
        p1 += derive_secret_at(patterns, initial_secret);

        // Loop this way to hint the compiler to use vector instructions for scanning.
        for (size_t i = 0; i < kPatternSize; i++) {
            sums[i] += static_cast<uint32_t>(patterns[i]) & 0x7F;
        }
    }
    printf("p1: %" PRIu64 "\n", p1);

    // Find the best score, also keep a copy of the pattern that made the score for visual.
    uint32_t best_score{0};
    uint32_t best_pattern{0};
    for (size_t i = 0; i < kPatternSize; i++) {
        if (const auto value = sums[i]; value > best_score) {
            best_pattern = i;
            best_score = value;
        }
    }

    printf("p2 = %d\n", best_score);

    // Print for visual
    int best_patterns[4]{};
    for (int i = 0; i < 4; i++) {
        constexpr int kLast5BitsMask = (1 << 5) - 1;
        best_patterns[i] = static_cast<int>((best_pattern >> (5 * (3 - i))) & kLast5BitsMask) - 9;
    }

    printf("best is %d (pattern = %d,%d,%d,%d%s", best_score,
           best_patterns[0], best_patterns[1], best_patterns[2], best_patterns[3],
#if PRINT_PATTERNS
           ", scores "
#else
           ")\n"
#endif
    );

#if PRINT_PATTERNS
    char c = '=';
    for (auto &p: pattern_cache) {
        printf("%c %d", c, static_cast<uint32_t>(p[best_pattern] & 0x7f));
        c = ',';
    }
    printf(")\n");
#endif
}
