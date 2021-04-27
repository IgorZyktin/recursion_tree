"""

    Drawing module

"""
import os
from io import StringIO
from recursion_tree.node import Node, analyze_nodes


def draw_boundary(node: Node) -> None:
    """
    Group boundary
    """
    if node.draw_boundary:
        width = node.right - node.left
        height = node.top - node.bottom

        opacity = round(((node.depth + 1) * 16) / 255, 3)

        left = node.left + Node.origin_x
        top = node.bottom + Node.origin_y

        draw('rect', ('fill-opacity', opacity), rx=node.node_bound_radius, x=left,
             y=top, width=width, height=height, fill=node.color_boundary,
             stroke=node.color_boundary_stroke, container=Node.svg)


def draw_node(nodes: list, node_id: int) -> None:
    """
    Node body drawing
    """
    node = nodes[node_id-1]

    left_edge = Node.origin_x + node.x - node.width // 2
    right_edge = Node.origin_x + node.x + node.width // 2

    center_x = Node.origin_x + node.x
    center_y = Node.origin_y + node.y

    node_x = center_x - node.width // 2
    node_y = center_y - node.height // 2

    draw('rect', ('stroke-width', node.node_stroke_width), ('fill-opacity', node.node_opacity),
         x=node_x, y=node_y, width=node.width, rx=node.node_radius, height=node.height,
         fill=node.color_node_body, stroke=node.color_node_stroke, container=Node.svg)

    labels = node.text.split('\n')
    if len(labels) > 1:
        label = f'<tspan x="{center_x}" dy="0">{labels[0]}</tspan>'
        for each in labels[1:]:
            label += f'<tspan x="{center_x}" dy="1.5em">{each}</tspan>'

        draw('line', ('stroke-width', node.node_stroke_width), x1=left_edge, y1=center_y,
             x2=right_edge, y2=center_y, stroke=node.color_node_stroke, container=Node.svg)

        text(x=center_x, y=center_y - 7, label=label, fill=node.color_text, container=Node.svg)

    else:
        text(x=center_x, y=center_y + 5, label=node.text, fill=node.color_text, container=Node.svg)


def draw_connections(node: Node) -> None:
    """
    Draw connection lines with call number
    """
    if not node.parent:
        return

    start_x = node.parent.x + Node.origin_x
    start_y = node.parent.y + Node.origin_y + node.parent.height // 2

    end_x = node.x + Node.origin_x
    end_y = node.y + Node.origin_y - node.height // 2

    if node.node_stroke_bezier:
        shift = 100
        m = f"M{start_x}, {start_y}"
        c = f"C{start_x}, {start_y + shift} {end_x}, {end_y - shift} {end_x} {end_y}"
        d = m + ' ' + c
        draw('path', ('stroke-width', node.node_conn_width), d=d, fill='transparent',
             stroke=node.color_connection, container=Node.svg)
    else:
        draw('line', ('stroke-width', node.node_conn_width), x1=start_x, y1=start_y,
             x2=end_x, y2=end_y, stroke=node.color_connection, container=Node.svg)

    if not node.draw_calls:
        return

    center_x = (start_x + end_x) // 2
    center_y = (start_y + end_y) // 2

    min_rad = node.char_width * len(str(node.node_id)) / 1.8
    radius = max(min_rad, node.node_num_radius)

    draw('circle', ('stroke-width', node.node_conn_width), cx=center_x, cy=center_y,
         r=radius, fill=node.color_num_background, stroke=node.color_connection,
         container=Node.svg)

    text(x=center_x, y=center_y + 5, fill=node.color_num_text,
         label=node.node_id, container=Node.svg)


def draw(shape, *pairs, container: list = None, **kwargs) -> str:
    """
    Abstract drawing function
    """
    par_1 = [f'{pair[0]}="{pair[1]}"' for pair in pairs]
    par_2 = [f'{key}="{value}"' for key, value in kwargs.items()]
    result = f'<{shape} ' + ' '.join(par_1 + par_2) + ' />'

    if container is not None:
        container.append(result)

    return result


def text(label: str, anchor: str = 'middle', container: list = None, **kwargs) -> str:
    """
    Add text
    """
    par_2 = [f'{key}="{value}"' for key, value in kwargs.items()]
    result = f'<text ' + ' '.join(par_2) + f' text-anchor="{anchor}">{label}</text>'

    if container is not None:
        container.append(result)

    return result


def draw_tree(func_name: str, nodes: list, settings: dict) -> None:
    """
    Main tree drawing
    """
    if not nodes:
        return

    nodes = analyze_nodes(nodes, settings)

    Node.initial_align(nodes, settings)
    root = nodes[0]

    width = (root.right - root.left) + settings['margin'] * 2
    height = (root.top - root.bottom) + settings['margin'] * 2 + settings['ver_spacing']

    Node.origin_x = abs(root.left) + settings['margin']
    Node.origin_y = abs(nodes[-1].bottom) + settings['margin']

    header = f'''
    <svg version="1.1" 
        width="{width}pt" 
        height="{height}pt" 
        viewBox="0 0 {width} {height}"
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns="http://www.w3.org/2000/svg">
        <style> text {{ font-size: 16px; font-family: Arial,sans-serif; }} </style>
    '''
    Node.svg.append(header)

    draw('rect', x=0, y=0, width=width, height=height,
         fill=settings['color_background'], container=Node.svg)

    for node in nodes:
        draw_boundary(node)
        draw_connections(node)
        draw_node(nodes, node.node_id)

    Node.svg.append('</svg>')
    result = '\n'.join(Node.svg)

    if isinstance(settings['file'], StringIO):
        settings['file'].write(result)
        return

    if isinstance(settings['file'], str):
        filename = settings['file'].lower().rstrip('.svg')
    else:
        filename = func_name

    i = 1
    while os.path.exists(filename + f'_{i:03d}.svg'):
        i += 1

    try:
        with open(filename + f'_{i:03d}.svg', mode='w', encoding='UTF-8') as file:
            file.write(result)
        print(f'New "{filename}_{i:03d}.svg" file has been saved.')
    except OSError:
        print(f'Unable to save "{filename}_{i:03d}.svg"')

    if settings['autostart']:
        try:
            os.startfile(filename + f'_{i:03d}.svg')
        except OSError:
            print(f'Unable to launch "{filename}_{i:03d}.svg"')
