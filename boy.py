from unittest.mock import right

from pico2d import load_image, get_time
from state_machine import StateMachine, space_down, time_out, left_up, right_up, left_down, right_down, autorun_down


class Idle:
    @staticmethod
    def entry(boy, event):
        boy.frame = 0
        #시작 시각을 기록
        boy.start_time = get_time()
        if boy.dir >= 0:
            boy.action = 3
        elif boy.dir < 0:
            boy.action = 2
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            # 이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT',0))
    @staticmethod
    def exit(boy, event):
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def entry(boy, event):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def exit(boy, event):
        pass
    @staticmethod
    def draw(boy):
        if boy.dir >= 0:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        elif boy.dir < 0:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)

class Run:
    @staticmethod
    def entry(boy, event):
        boy.frame = 0
        if right_down(event) or left_up(event):
            boy.action = 1
            boy.dir = 1
        elif left_down(event) or right_up(event):
            boy.action = 0
            boy.dir = -1
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 8
    @staticmethod
    def exit(boy, event):
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def entry(boy, event):
        boy.frame = 0
        if boy.dir >= 0:
            boy.action = 1
            boy.dir = 1
        elif boy.dir < 0:
            boy.action = 0
        boy.auto_time = get_time()
    @staticmethod
    def do(boy):
        if get_time() - boy.auto_time > 5:
            boy.state_machine.add_event(('TIME_OUT',0))
        boy.frame = (boy.frame + 1) % 8
        if boy.x >= 780:
            boy.dir = -1
            boy.action = 0
        if boy.x <= 20:
            boy.dir = 1
            boy.action = 1
        boy.x += boy.dir * 88
    @staticmethod
    def exit(boy, event):
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 60, 300, 300)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 어떤 객체를 위한 상태머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle) # 객체를 생성한 것이 아니라, 직접 Idle 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Sleep, left_down: Run, right_down: Run,autorun_down: AutoRun},
                #Idle: {time_out: Sleep, left_down: Run, right_down: Run, left_up: Run, right_up: Run},
                Sleep: {space_down: Idle, left_down: Run, right_down: Run, left_up: Idle, right_up: Idle},
                Run:{left_up: Idle, right_up: Idle, left_down: Idle, right_down: Idle, autorun_down: AutoRun},
                AutoRun: {time_out: Idle, left_down: Run, right_down: Run}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        #state machine event : (이벤트 종류, 값) 으로 변경
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()

