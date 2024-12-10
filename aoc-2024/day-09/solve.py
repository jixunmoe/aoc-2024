import argparse

EMPTY = -1


class Disk:
    data: list[int] = []
    pos_data: list[tuple[int, int]] = []
    free_data: list[tuple[int, int]] = []

    def __init__(self, disk_map: str):
        self.data = []
        self.pos_data = []

        block_id = 0
        for (i, size) in enumerate(map(int, disk_map)):
            if i % 2 == 0:
                self.pos_data.append((len(self.data), size))
                self.data += [block_id] * size
                block_id += 1
            else:
                self.free_data.append((len(self.data), size))
                self.data += [EMPTY] * size
        self.top_block_id = block_id

    def compact_disk_p1(self):
        result = self.data.copy()

        i = 0
        j = len(result) - 1
        while i < j:
            if result[i] != EMPTY:
                i += 1
                continue
            if result[j] == EMPTY:
                j -= 1
                continue
            result[i] = result[j]
            result[j] = EMPTY
        return result

    def compact_and_checksum(self):
        pos_data = self.pos_data.copy()
        free_data = self.free_data.copy()

        # The free space does not merge automatically, and we don't bother with the free space
        #   after current position, so we don't need to worry about merging empty spaces.
        for (blk_id, (blk_idx, blk_size)) in reversed(list(enumerate(pos_data))):
            for (j, (free_idx, free_size)) in enumerate(free_data):
                if free_idx >= blk_idx: break

                if free_size >= blk_size:
                    pos_data[blk_id] = (free_idx, blk_size)
                    free_data[j] = (free_idx + blk_size, free_size - blk_size)
                    break

        # Implement the checksum over the compacted disk
        checksum = 0
        for (blk_id, (blk_idx, blk_size)) in enumerate(pos_data):
            for i in range(blk_size):
                checksum += blk_id * blk_idx
                blk_idx += 1
        return checksum

    @staticmethod
    def checksum(data: list[int]):
        return sum([i * disk_id for (i, disk_id) in enumerate(data) if disk_id != EMPTY])


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    disk = Disk(input_text)

    p1 = disk.checksum(disk.compact_disk_p1())
    print(f'p1 = {p1}')

    p2 = disk.compact_and_checksum()
    print(f'p2 = {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
