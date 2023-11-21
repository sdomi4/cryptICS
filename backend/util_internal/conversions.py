def bytearray_to_blocks(data: bytearray, block_size: int) -> list:
        return [data[i:i+block_size] for i in range(0, len(data), block_size)]