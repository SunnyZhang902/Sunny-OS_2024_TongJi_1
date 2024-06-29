# 2024/5/5 by 2253230 张正阳
import sys
import time
from functools import partial
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Elevator_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 整体布局
        whole_layout = QHBoxLayout()
        grid_elevator_external = QGridLayout()
        grid_elevator_internal = QGridLayout()

        grid_elevator_internal.setSpacing(1)
        grid_elevator_external.setSpacing(1)

        widget_left = QWidget()
        widget_right = QWidget()
        widget_left.setLayout(grid_elevator_internal)
        widget_right.setLayout(grid_elevator_external)
        whole_layout.addWidget(widget_left)
        whole_layout.addWidget(widget_right)

        self.setLayout(whole_layout)

        # 楼层信息
        floor_name = [('%s' % i) for i in range(1, 21)]
        floor_button_positions = [(10 - i, j) for j in range(2) for i in range(10)]
        button_up = [('▲') for i in range(1, 21)]
        button_down = [('▼') for i in range(1, 21)]

        # 内部楼层按钮
        for i in range(5):
            self.label_floor = QLabel()
            self.label_floor.setObjectName("Floor{0}".format(i + 1))
            grid_elevator_internal.addWidget(self.label_floor, 0, 4 * i, 2, 2)
            self.space = QLabel(self)
            grid_elevator_internal.addWidget(self.space, 0, 4 * i + 2, 15, 1)
            self.label_floor.setStyleSheet("color: #FFE6E6; background-color: #9783AA")
            self.label_floor.setFont(QFont("SimSun", 20, QFont.Bold))
            self.label_floor.setAlignment(Qt.AlignCenter)

        # 内部楼层按钮
        for i in range(5):
            j = 1
            for position, name in zip(floor_button_positions, floor_name):
                if name == '':
                    continue
                self.button = QPushButton(name)
                self.button.setFixedSize(60, 60)
                self.button.setFont(QFont("SimSun", 11, QFont.Bold))
                self.button.setObjectName("{0}+{1}".format(i + 1, j))
                self.button.setStyleSheet("background-color: #ADD8E6")
                self.button.clicked.connect(partial(Set_Elevator_Goal_Internal, i + 1, j))
                j = j + 1
                grid_elevator_internal.addWidget(self.button, position[0] + 2, position[1] + i * 4)

        # 设置行高
        for i in range(grid_elevator_internal.rowCount()):
            grid_elevator_internal.setRowMinimumHeight(i, 60)

        # 电梯门状态
        for i in range(5):
            self.label = QLabel()
            self.label.setObjectName("open{0}".format(i + 1))
            self.label.setMinimumHeight(80)
            self.label.setStyleSheet("background-image: url(door_close.jpg);background-position: center")
            label_space = QLabel(self)
            grid_elevator_internal.addWidget(label_space, 13, 4 * i, 1, 2)
            grid_elevator_internal.addWidget(self.label, 13 + 1, 4 * i, 1, 2)

        # 电梯停用按钮
        for i in range(5):
            self.button = QPushButton("停用")
            self.button.setFont(QFont("SimSun", 12))
            self.button.setStyleSheet("background-color: #FFF2CC")
            self.button.setObjectName("停用{0}".format(i + 1))
            self.button.setMinimumHeight(40)
            self.button.clicked.connect(partial(Elevator_Pause, i + 1))
            label_space = QLabel(self)
            grid_elevator_internal.addWidget(label_space, 13 + 2, 0, 1, 2)
            grid_elevator_internal.addWidget(self.button, 13 + 3, 4 * i, 1, 2)

        # 外部按钮
        for i in range(1, 21):
            label = QLabel("F" + str(i)+"  ")
            label.setAlignment(Qt.AlignCenter)
            font = QFont("SimSun", 10)
            font.setBold(True)
            label.setFont(font)
            grid_elevator_external.addWidget(label, 21 - i, 0)

        num_i = 0
        for i in button_up:
            if num_i == 19:
                break
            self.button = QPushButton(i)
            self.button.setFont(QFont("SimSun",7))
            self.button.setObjectName("up{0}".format(num_i + 1))
            self.button.setMinimumHeight(42)
            self.button.setFixedWidth(42)
            self.button.setStyleSheet("background-color: #ADD8E6")
            self.button.clicked.connect(partial(Set_Elevator_Goal_External_Up, num_i + 1))
            grid_elevator_external.addWidget(self.button, 20 - num_i, 3)
            num_i = num_i + 1

        num_i = 0
        for i in button_down:
            if num_i == 0:
                num_i = num_i + 1
                continue
            self.button = QPushButton(i)
            self.button.setFont(QFont("SimSun",9))
            self.button.setObjectName("down{0}".format(num_i + 1))
            self.button.setMinimumHeight(42)
            self.button.setFixedWidth(42)
            self.button.setStyleSheet("background-color: #ADD8E6")
            self.button.clicked.connect(partial(Set_Elevator_Goal_External_Down, num_i + 1))
            grid_elevator_external.addWidget(self.button, 20 - num_i, 5)
            num_i = num_i + 1

        # 设置窗口样式和标题
        self.setStyleSheet("background-color: #FFE6E6")
        self.setWindowTitle('电梯调度 by 2253230 张正阳')
        self.move(100, 100)
        self.show()

class Elevator_Thread(QThread):
    update_signal = pyqtSignal(int)
    open_signal = pyqtSignal(int, int)

    def __init__(self, elevator_num):
        super(Elevator_Thread, self).__init__()
        self.int = elevator_num
        self.update_signal.connect(Elevator_Update)
        self.open_signal.connect(Open_Door)

    def run(self):
        while (1):
            # 发送更新信号
            self.update_signal.emit(self.int)
            time.sleep(1)

            # 如果需要打开门，则发送打开门信号
            if open_door[self.int - 1] == 1:
                self.open_signal.emit(0, self.int)
                time.sleep(0.2)
                self.open_signal.emit(1, self.int)
                time.sleep(0.5)
                self.open_signal.emit(0, self.int)
                time.sleep(0.2)
                self.open_signal.emit(2, self.int)
                time.sleep(0.5)
                open_door[self.int - 1] = 0

# 打开、关闭、半开门的逻辑处理
def Open_Door(type, elevator_num):
    if type == 0:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_half.jpg);background-position: center}")
    elif type == 1:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_open.jpg);background-position: center}")
    elif type == 2:
        My_Elevator_Window.findChild(QLabel, "open{0}".format(elevator_num)).setStyleSheet(
            "QLabel{background-image: url(door_close.jpg);background-position: center}")

# 电梯状态更新
def Elevator_Update(elevator_num_1):
    elevator_num = elevator_num_1 - 1

    if pause[elevator_num] == 0:
        return

    if state[elevator_num] == -1:
        floor[elevator_num] -= 1
    elif state[elevator_num] == 1:
        floor[elevator_num] += 1

    if floor[elevator_num] in elevator_goal_internal[elevator_num]:
        open_door[elevator_num] = 1
        My_Elevator_Window.findChild(QPushButton, "{0}+{1}".format(elevator_num_1, floor[elevator_num])).setStyleSheet(
            "QPushButton{background-color: #ADD8E6}")
        elevator_goal_internal[elevator_num].discard(floor[elevator_num])

    if elevator_goal_total[elevator_num]:
        if (state[elevator_num] == 1 or min(elevator_goal_total[elevator_num]) >= floor[elevator_num]) \
                and floor[elevator_num] in elevator_goal_external_up[elevator_num]:
            open_door[elevator_num] = 1
            My_Elevator_Window.findChild(QPushButton, "up{0}".format(floor[elevator_num])).setStyleSheet(
                "QPushButton{background-color: #ADD8E6}")
            elevator_goal_external_up[elevator_num].discard(floor[elevator_num])
            external_up.discard(floor[elevator_num])

        if (state[elevator_num] == -1 or max(elevator_goal_total[elevator_num]) <= floor[elevator_num]) \
                and floor[elevator_num] in elevator_goal_external_down[elevator_num]:
            open_door[elevator_num] = 1
            My_Elevator_Window.findChild(QPushButton, "down{0}".format(floor[elevator_num])).setStyleSheet(
                "QPushButton{background-color: #ADD8E6}")
            elevator_goal_external_down[elevator_num].discard(floor[elevator_num])
            external_down.discard(floor[elevator_num])

        if state[elevator_num] == 0:
            if floor[elevator_num] in elevator_goal_external_up[elevator_num]:
                open_door[elevator_num] = 1
                My_Elevator_Window.findChild(QPushButton, "up{0}".format(floor[elevator_num])).setStyleSheet(
                    "QPushButton{background-color: #ADD8E6}")
                elevator_goal_external_up[elevator_num].discard(floor[elevator_num])
                external_up.discard(floor[elevator_num])
            elif floor[elevator_num] in elevator_goal_external_down[elevator_num]:
                open_door[elevator_num] = 1
                My_Elevator_Window.findChild(QPushButton, "down{0}".format(floor[elevator_num])).setStyleSheet(
                    "QPushButton{background-color: #ADD8E6}")
                elevator_goal_external_down[elevator_num].discard(floor[elevator_num])
                external_down.discard(floor[elevator_num])

        elevator_goal_total[elevator_num] = elevator_goal_internal[elevator_num].union(
            elevator_goal_external_up[elevator_num]).union(elevator_goal_external_down[elevator_num])

    goal_internal_list = list(elevator_goal_internal[elevator_num])
    goal_list = list(elevator_goal_internal[elevator_num].union(elevator_goal_external_up[elevator_num]).union(
        elevator_goal_external_down[elevator_num]))

    if len(goal_list) == 0:
        state[elevator_num] = 0
    elif state[elevator_num] == 0:
        to_floor = 1
        if len(goal_internal_list) != 0:
            to_floor = goal_internal_list[0]
        else:
            to_floor = goal_list[0]
        if to_floor > floor[elevator_num]:
            state[elevator_num] = 1
        else:
            state[elevator_num] = -1
    elif state[elevator_num] == 1:
        tag = 0
        for to_floor in goal_list:
            if to_floor > floor[elevator_num]:
                tag = 1
                break
        if tag == 0:
            state[elevator_num] = -1
    else:
        tag = 0
        for to_floor in goal_list:
            if to_floor < floor[elevator_num]:
                tag = 1
                break
        if tag == 0:
            state[elevator_num] = 1

    label_floor = My_Elevator_Window.findChild(QLabel, "Floor{0}".format(elevator_num_1))

    if state[elevator_num] == -1:
        label_floor.setText("↓" + str(floor[elevator_num]))
    elif state[elevator_num] == 1:
        label_floor.setText("↑" + str(floor[elevator_num]))
    else:
        label_floor.setText(str(floor[elevator_num]))

# 控制电梯暂停/启动
def Elevator_Pause(elevator_num):
    if pause[elevator_num - 1] == 0:
        pause[elevator_num - 1] = 1
        My_Elevator_Window.findChild(QPushButton, "停用{0}".format(elevator_num)).setText("停用")
    else:
        pause[elevator_num - 1] = 0
        My_Elevator_Window.findChild(QPushButton, "停用{0}".format(elevator_num)).setText("启用")

# 设置内部目标楼层
def Set_Elevator_Goal_Internal(elevator_num, to_floor):
    My_Elevator_Window.findChild(QPushButton, "{0}+{1}".format(elevator_num, to_floor)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")
    elevator_goal_internal[elevator_num - 1].add(to_floor)
    elevator_goal_total[elevator_num - 1].add(to_floor)

# 设置外部向上按钮目标楼层
def Set_Elevator_Goal_External_Up(to_floor):
    if to_floor in external_up:
        return

    external_up.add(to_floor)

    My_Elevator_Window.findChild(QPushButton, "up{0}".format(to_floor)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")

    for i in range(5):
        if state[i] == 0:
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    for i in range(5):
        if state[i] == 1 and floor[i] <= to_floor:
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    min_floor = min(floor)
    lowest_elevator = floor.index(min_floor)

    if min_floor <= to_floor:
        elevator_goal_external_up[lowest_elevator].add(to_floor)
        elevator_goal_total[lowest_elevator].add(to_floor)
        return

    for i in range(5):
        if(state[i] == -1):
            elevator_goal_external_up[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    max_floor = max(floor)
    highest_elevator = floor.index(max_floor)
    elevator_goal_external_up[highest_elevator].add(to_floor)
    elevator_goal_total[highest_elevator].add(to_floor)

# 设置外部向下按钮目标楼层
def Set_Elevator_Goal_External_Down(to_floor):
    if to_floor in external_down:
        return

    external_down.add(to_floor)

    My_Elevator_Window.findChild(QPushButton, "down{0}".format(to_floor)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")

    for i in range(5):
        if state[i] == 0:
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    for i in range(5):
        if state[i] == -1 and floor[i] >= to_floor:
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    max_floor = max(floor)
    highest_elevator = floor.index(max_floor)

    if max_floor >= to_floor:
        elevator_goal_external_down[highest_elevator].add(to_floor)
        elevator_goal_total[highest_elevator].add(to_floor)
        return

    for i in range(5):
        if (state[i] == 1):
            elevator_goal_external_down[i].add(to_floor)
            elevator_goal_total[i].add(to_floor)
            return

    min_floor = min(floor)
    lowest_elevator = floor.index(min_floor)
    elevator_goal_external_down[lowest_elevator].add(to_floor)
    elevator_goal_total[lowest_elevator].add(to_floor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    My_Elevator_Window = Elevator_Window()

    # 电梯目标楼层列表初始化
    elevator_goal_internal = []
    elevator_goal_external_up = []
    elevator_goal_external_down = []
    elevator_goal_total = []
    external_up = set([])
    external_down = set([])

    for i in range(5):
        elevator_goal_internal.append(set([]))
        elevator_goal_external_up.append(set([]))
        elevator_goal_external_down.append(set([]))
        elevator_goal_total.append(set([]))

    # 电梯状态初始化
    state = []
    pause = []
    floor = []
    open_door = []

    for i in range(5):
        state.append(0)
        pause.append(1)
        floor.append(1)
        open_door.append(0)

    # 启动电梯线程
    My_Elevator_Thread = []
    for i in range(1,6):
        My_Elevator_Thread.append(Elevator_Thread(i))

    for i in range(5):
        My_Elevator_Thread[i].start()

    sys.exit(app.exec_())
