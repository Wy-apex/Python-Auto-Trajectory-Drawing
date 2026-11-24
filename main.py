
import csv
import math
import turtle
from pathlib import Path


# 一、读取轨迹数据
def read_data():
    file_path = Path(__file__).parent / "data.txt"
    commands = []

    with open(file_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if row:
                commands.append([float(x) for x in row])

    return commands


# 二、根据轨迹指令计算坐标
def calculate_track(commands):
    x, y = -30, -120
    angle = 0

    points = [(x, y)]
    segments = []

    for distance, direction, turn, r, g, b in commands:
        new_x = x + distance * math.cos(math.radians(angle))
        new_y = y + distance * math.sin(math.radians(angle))

        segments.append((
            (x, y),
            (new_x, new_y),
            (r, g, b)
        ))

        points.append((new_x, new_y))

        x, y = new_x, new_y

        if direction == 0:
            angle += turn
        else:
            angle -= turn

    return points, segments


# 三、绘制多边形轮廓
def draw_polygon(pen, points):
    pen.penup()
    pen.goto(points[0])
    pen.pendown()

    pen.pencolor("black")
    pen.pensize(2)

    for point in points[1:] + points[:1]:
        pen.goto(point)


# 四、计算关于指定直线的对称点
def reflect_point(point, a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    px = point[0] - a[0]
    py = point[1] - a[1]

    ratio = (px * dx + py * dy) / (dx * dx + dy * dy)

    proj_x = a[0] + ratio * dx
    proj_y = a[1] + ratio * dy

    return (2 * proj_x - point[0],
            2 * proj_y - point[1])


# 五、自动绘制
def main():
    commands = read_data()

    if len(commands) != 6:
        print("错误：data.txt 应包含6条轨迹指令")
        return

    points, segments = calculate_track(commands)

    screen = turtle.Screen()
    screen.setup(1000, 650)
    screen.title("自动轨迹绘制")

    turtle.colormode(1.0)

    pen = turtle.Turtle()
    pen.speed(8)
    pen.hideturtle()

    # 右侧五边形轮廓
    right = [
        points[0],
        points[2],
        points[4],
        points[1],
        points[3]
    ]

    # 左侧相邻五边形轮廓
    left = [
        points[0],
        points[2],
        reflect_point(points[4], points[0], points[2]),
        reflect_point(points[1], points[0], points[2]),
        reflect_point(points[3], points[0], points[2])
    ]

    draw_polygon(pen, left)
    draw_polygon(pen, right)

    # 按文件中的RGB颜色绘制轨迹
    pen.pensize(4)

    for start, end, color in segments:
        pen.penup()
        pen.goto(start)
        pen.pencolor(color)
        pen.pendown()
        pen.goto(end)

    print("轨迹绘制完成！")
    print(f"成功读取 {len(commands)} 条轨迹指令")

    turtle.done()


if __name__ == "__main__":
    main()
