"""

    Drawing module

"""
from collections import namedtuple

from PIL import Image, ImageDraw, ImageFont

from node import Node
from settings import CONN_COLOR, CONN_WIDTH, NUM_SHIFT, DRAW_CALLS, OUTLINE_COLOR
from settings import FONT_FILE, FONT_SIZE, FUNC_NAME_COLOR, LABEL_COLOR, BG_COLOR
from settings import BOUNDARY_COLOR, BOUNDARY_EDGE_COLOR, DRAW_BOUNDARY
from settings import MARGIN, VER_SPACING, TEXT_OUTLINE_SIZE, NODE_OUTLINE_SIZE

FONT = ImageFont.truetype(FONT_FILE, FONT_SIZE)
Point = namedtuple('Point', ['x', 'y'])


def draw_boundary(node: Node, origin: Point, canvas: Image.Image) -> None:
    """
        Group boundary
    """
    if not DRAW_BOUNDARY:
        return

    width = node.right - node.left
    height = node.top - node.bottom

    b_color = BOUNDARY_COLOR
    edge_color = BOUNDARY_EDGE_COLOR
    base_color = (b_color[0], b_color[1], b_color[2], (node.depth + 1) * b_color[3])

    boundary = Image.new(mode="RGBA", size=(width, height), color=base_color)
    draw = ImageDraw.ImageDraw(boundary, "RGBA")
    draw.rectangle((0, 0, width - 1, height - 1), fill=base_color, outline=edge_color)

    left = node.left + origin.x
    top = node.bottom + origin.y

    canvas.alpha_composite(boundary, (left, top))


def draw_node(nodes: list, node_id: int, draw, node_start) -> None:
    """
        Node body drawing
    """
    node = nodes[node_id-1]
    center = Point(node.x + node_start.x, node.y + node_start.y)

    x0 = center.x - node.size[0] // 2 - TEXT_OUTLINE_SIZE
    y0 = center.y - node.size[1] // 2 - TEXT_OUTLINE_SIZE
    x1 = center.x + node.size[0] // 2 + TEXT_OUTLINE_SIZE
    y1 = center.y + node.size[1] // 2 + TEXT_OUTLINE_SIZE

    outline = NODE_OUTLINE_SIZE
    draw.rectangle((x0 - outline, y0 - outline, x1 + outline, y1 + outline), fill=(0, 0, 0, 255))
    draw.rectangle((x0, y0, x1, y1), fill=(133, 181, 232, 255))

    actsize = draw.textsize(text=node.text, font=FONT)
    text_x = center.x - actsize[0] // 2
    text_y = center.y - actsize[1] // 2
    draw.text((text_x, text_y), node.text, font=FONT, fill=FUNC_NAME_COLOR)


def draw_connections(node: Node, origin: Point, draw: ImageDraw.ImageDraw) -> None:
    """
        Draw lines with call number
    """
    if not node.parent:
        return

    start_x = node.parent.x + origin.x
    if node.parent.node_id == 1:
        start_y = node.parent.y + origin.y
    else:
        start_y = node.parent.y + origin.y + node.parent.size[1] // 2 + TEXT_OUTLINE_SIZE

    end_x = node.x + origin.x
    end_y = node.y + origin.y - node.size[1] // 2 - TEXT_OUTLINE_SIZE

    draw.line((start_x, start_y, end_x, end_y), fill=CONN_COLOR, width=CONN_WIDTH)

    if not DRAW_CALLS:
        return

    center = Point((start_x + end_x) // 2, (start_y + end_y) // 2)
    node_id = str(node.node_id)

    minsize = draw.textsize(text='00', font=FONT)
    actsize = draw.textsize(text=node_id, font=FONT)

    size = max(max(actsize[0], minsize[0]), max(actsize[1], minsize[1])) // 2 + NUM_SHIFT

    big = [center.x - size, center.y - size, center.x + size, center.y + size]
    small = [center.x - size + 2, center.y - size + 2, center.x + size - 2, center.y + size - 2]

    draw.ellipse(big, fill=CONN_COLOR)
    draw.ellipse(small, fill=LABEL_COLOR)

    draw.text((center.x - actsize[0] // 2, center.y - actsize[1] // 2), node_id, font=FONT)


def draw_tree(nodes: list, show: bool = True, save: bool = True) -> None:
    """
        Main tree drawing
    """
    if not nodes:
        return

    temp_canv = Image.new(mode='RGB', size=(1, 1))
    temp_draw = ImageDraw.ImageDraw(temp_canv, 'RGB')

    sizes = [temp_draw.textsize(node.text, font=FONT) for node in nodes]
    max_w = max([size[0] for size in sizes])
    max_h = max([size[1] for size in sizes])

    del temp_canv
    del temp_draw

    for node in nodes:
        node.size = (max_w, max_h)

    Node.initial_align(nodes)
    root = nodes[0]

    width = (root.right - root.left) + MARGIN * 2
    height = (root.top - root.bottom) + MARGIN * 2 + VER_SPACING

    origin = Point(abs(root.left) + MARGIN, abs(nodes[-1].bottom) + MARGIN)

    canvas_size = (width, height)
    canvas = Image.new(mode="RGBA", size=canvas_size, color=BG_COLOR)
    draw = ImageDraw.ImageDraw(canvas, "RGBA")
    draw.rectangle((0, 0, canvas_size[0] - 1, canvas_size[1] - 1), outline=OUTLINE_COLOR)

    for node in nodes:
        draw_boundary(node, origin, canvas)
        draw_connections(node, origin, draw)

    for node in nodes:
        draw_node(nodes, node.node_id, draw, origin)

    del draw

    if save:
        try:
            with open('result.png', mode='wb') as file:
                canvas.save(file)
            print('New "result.png" file has been saved.')
        except OSError:
            print('Unable to save "result.png".')

    if show:
        canvas.show()
