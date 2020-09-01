import os

class MessageSizeExcedeedError(Exception):
    pass

class BlockSizeExcedeedError(Exception):
    pass

class InterleaveTooBigError(Exception):
    pass

def validate_params(path, message, block_size, offset, interleave):

    if not os.path.exists(path):
        raise FileNotFoundError('Carrier file not found in path {}'.format(path))
    if not os.path.exists(message):
        raise FileNotFoundError('Message file not found in path {}'.format(message))

    # each pixel is 3 bytes, not including alpha
    bytes_offset = int(offset) * 3
    bytes_interleave = int(interleave) * 3

    # The actual available size is the total size of the file
    # minus the offset we wish to start from
    usable_file_size = (os.stat(path).st_size - bytes_offset)
    msg_size = os.stat(message).st_size

    if msg_size > usable_file_size:
        raise MessageSizeExcedeedError('Message is too long for file')
    if block_size > usable_file_size:
        raise BlockSizeExcedeedError('Block size is bigger than file')
    if (msg_size * bytes_interleave) > usable_file_size:
        raise InterleaveTooBigError('Interleave is too big for available size')