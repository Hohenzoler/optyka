import pygame

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

def do_lines_intersect(line1_start, line1_end, line2_start, line2_end):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    def on_segment(p, q, r):
        return (
            (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]))
            and (q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))
        )

    o1 = orientation(line1_start, line1_end, line2_start)
    o2 = orientation(line1_start, line1_end, line2_end)
    o3 = orientation(line2_start, line2_end, line1_start)
    o4 = orientation(line2_start, line2_end, line1_end)

    if o1 != o2 and o3 != o4:
        return True  # Intersect

    if o1 == 0 and on_segment(line1_start, line2_start, line1_end):
        return True  # Collinear and overlapping
    if o2 == 0 and on_segment(line1_start, line2_end, line1_end):
        return True  # Collinear and overlapping
    if o3 == 0 and on_segment(line2_start, line1_start, line2_end):
        return True  # Collinear and overlapping
    if o4 == 0 and on_segment(line2_start, line1_end, line2_end):
        return True  # Collinear and overlapping

    return False  # Doesn't intersect

def draw_thick_line(surface, x1, y1, x2, y2, color, THICC):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        for offset in range(THICC):
            pygame.gfxdraw.line(surface, x1, y1 + offset, x2, y2 + offset, color)
    else:
        for offset in range(THICC):
            pygame.gfxdraw.line(surface, x1 + offset, y1, x2 + offset, y2, color)