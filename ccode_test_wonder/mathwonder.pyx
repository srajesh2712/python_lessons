# This is Cython - A mix of Python and C
def fast_threshold(float[:] pixels, float limit):
    cdef int i
    cdef int n = pixels.shape[0]
    # This loop runs at pure C speed!
    for i in range(n):
        if pixels[i] > limit:
            pixels[i] = 255
        else:
            pixels[i] = 0