# event(종류 문자열, 입력 값)
from sdl2 import SDL_KEYUP, SDLK_SPACE, SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDLK_a


def space_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE
def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT
def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT
def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT
def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT
def autorun_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_a
def time_out(event):
    return event[0] == 'TIME_OUT'


# 상태 머신을 처리 관리해주는 클래스
class StateMachine:
    def __init__(self, obj):
        self.obj = obj # boy의 self가 전달, self.obj: 상태 머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는 큐

    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듬
        self.cur_state = start_state # Idle
        # 새로운 상태로 시작했기 때문에, entry를 실행해야 한다.
        self.cur_state.entry(self.obj, ('START', 0))
        print(f'Enter into {self.cur_state}')

    def update(self):
        self.cur_state.do(self.obj) # Idle.do()
        # 이벤트 발생 여부 확인, 그에 따른 상태변환 수행
        if self.event_que: # list에 요소가 있으면, list 값은 True
            event = self.event_que.pop(0) # list의 첫 번째 요소 꺼냄
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(event): # event가 현재 check_event라면?
                    self.cur_state.exit(self.obj, event)
                    print(f'Exit from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.entry(self.obj, event)
                    print(f'Entry into {next_state}')
                    return
    def draw(self):
        self.cur_state.draw(self.obj)
    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, event):
        self.event_que.append(event) #상태머신용 이벤트 추가
        print(f'    DEBUG: new event {event} is added')
