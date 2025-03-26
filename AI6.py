class BlockWorldGSP:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state.copy()
        self.goal_state = goal_state
        self.plan = []
    
    def is_goal_reached(self):
        return set(self.initial_state) == set(self.goal_state)
    
    def apply_action(self, action):
        if action[0] == 'unstack':
            block, from_block = action[1], action[2]
            if ('on', block, from_block) in self.initial_state:
                self.initial_state.remove(('on', block, from_block))
                self.initial_state.append(('ontable', block))
        elif action[0] == 'stack':
            block, to_block = action[1], action[2]
            if ('ontable', block) in self.initial_state:
                self.initial_state.remove(('ontable', block))
                self.initial_state.append(('on', block, to_block))
        elif action[0] == 'pickup':
            block = action[1]
            if ('ontable', block) in self.initial_state:
                self.initial_state.remove(('ontable', block))
        elif action[0] == 'putdown':
            block = action[1]
            self.initial_state.append(('ontable', block))
    
    def generate_plan(self):
        goal_stack = list(reversed(self.goal_state))
        while goal_stack:
            goal = goal_stack.pop()
            if goal in self.initial_state:
                continue
            if goal[0] == 'on':
                block, below = goal[1], goal[2]
                if ('ontable', block) in self.initial_state:
                    self.plan.append(('pickup', block))
                else:
                    self.plan.append(('unstack', block, self.find_below(block)))
                self.plan.append(('stack', block, below))
                self.initial_state.append(goal)
            elif goal[0] == 'ontable':
                block = goal[1]
                if ('on', block, self.find_below(block)) in self.initial_state:
                    self.plan.append(('unstack', block, self.find_below(block)))
                    self.plan.append(('putdown', block))
                self.initial_state.append(goal)
    
    def find_below(self, block):
        for relation in self.initial_state:
            if relation[0] == 'on' and relation[1] == block:
                return relation[2]
        return None
    
    def execute_plan(self):
        print("\n=== completion plan ===")
        for action in self.plan:
            if action[0] == 'unstack':
                print(f"Unstack {action[1]}, {action[2]}")
            elif action[0] == 'stack':
                print(f"Stack {action[1]}, {action[2]}")
            elif action[0] == 'pickup':
                print(f"Pickup {action[1]}")
            elif action[0] == 'putdown':
                print(f"Putdown {action[1]}")
        print("\n=== Goals ===")
        for state in self.goal_state:
            print(state)

# Input Inisial
initial_state = [
    ('ontable', 2), ('on', 4, 2), ('ontable', 1), ('on', 3, 1),
    ('ontable', 5), ('on', 6, 5), ('ontable', 7), ('on', 8, 7),
    ('ontable', 9), ('on', 10, 9)
]

# Input Goals
goal_state = [
    ('ontable', 2), ('on', 4, 2), ('on', 6, 4), ('on', 8, 6),
    ('on', 10, 8), ('ontable', 1), ('on', 3, 1), ('on', 5, 3),
    ('on', 7, 5), ('on', 9, 7)
]

# Jalankan Algoritma GSP
solver = BlockWorldGSP(initial_state, goal_state)
solver.generate_plan()
solver.execute_plan()
