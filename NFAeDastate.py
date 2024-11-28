import os

print("Current Working Directory:", os.getcwd())

# Thay đổi thư mục làm việc về nơi chứa file NFAe
os.chdir(r'C:\Users\Hiếu\OneDrive\Máy tính\Khoa Học Máy Tính K48\Tin Học Lý Thuyết\Đồ Án')


class NFAe:
    def __init__(self, states, alphabet, transitions, start_states, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_states = start_states 
        self.accept_states = accept_states
        self.epsilon_closures = {}

    def compute_epsilon_closures(self):
        """Tính epsilon-closure cho tất cả các trạng thái."""
        for state in self.states:
            self.epsilon_closures[state] = self.epsilon_closure(state)

    def epsilon_closure(self, state):
        """Tính epsilon-closure cho một trạng thái."""
        closure = set([state])  # Bắt đầu từ chính trạng thái đó
        stack = [state]         # Sử dụng stack để duyệt tất cả các trạng thái liên quan

        while stack:
            current = stack.pop()
            # Kiểm tra tất cả các trạng thái có thể đạt qua epsilon-transition
            for next_state in self.transitions.get((current, ''), []): #nếu có key thì trả về giá trị ngược lại trả về ds rỗng
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def simulate(self, input_string):
        """Mô phỏng NFAε với chuỗi đầu vào."""
        self.compute_epsilon_closures()  # Tính epsilon-closure một lần trước khi bắt đầu
        print("\nEpsilon-closures của tất cả các trạng thái:")
        for state, closure in self.epsilon_closures.items():
            print(f"  Epsilon-closure({state}) = {closure}")

        print("\nBắt đầu mô phỏng:")

        # Tính epsilon-closure của tất cả các trạng thái bắt đầu
        current_states = set()
        for start in self.start_states:
            current_states.update(self.epsilon_closures[start])

        print(f"  Trạng thái ban đầu: {self.start_states}, Epsilon-closure: {current_states}")

        steps = []  # Lưu các bước chuyển

        for symbol in input_string:
            next_states = set()
            # Từ epsilon-closure của trạng thái hiện tại, xét các chuyển đổi qua ký tự
            for state in current_states:
                next_states.update(self.transitions.get((state, symbol), []))

            # Hiển thị trạng thái sau khi qua ký tự nhưng chưa tính epsilon-closure
            print(f"  Qua nhãn '{symbol}', từ {current_states} đạt trạng thái: {next_states}")

            # Tính epsilon-closure của các trạng thái vừa đạt được
            closure_after_symbol = set()
            for state in next_states:
                closure_after_symbol.update(self.epsilon_closures[state])

            # Hiển thị kết quả sau khi tính epsilon-closure
            steps.append((symbol, current_states, next_states, closure_after_symbol))
            print(f"  Sau khi tính Epsilon-closure: {closure_after_symbol}")
            current_states = closure_after_symbol

        # Kiểm tra trạng thái kết thúc có chứa trạng thái chấp nhận
        accepted_states = current_states.intersection(self.accept_states)
        
        if accepted_states:
            print(f"\nVì {accepted_states} có trong tập các trạng thái chấp nhận là {self.accept_states} =>")
            print("NFAe chấp nhận chuỗi!")
        else:
            print("\nNFAe không chấp nhận chuỗi!")

        return 


def read_nfae_from_file(filename):
    """Đọc thông tin NFAe từ file."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    #Tách chuỗi thành list qua dấu : và lấy phần sau dấu :, xóa khoảng trắng đầu cuối, tách chuỗi thành ds qua dấu , sau đó chuyển về set.
    states = set(lines[0].split(':')[1].strip().split(','))
    alphabet = set(lines[1].split(':')[1].strip().split(','))
    start_states = set(lines[2].split(':')[1].strip().split(',')) 
    accept_states = set(lines[3].split(':')[1].strip().split(','))
    transitions = {}

    for line in lines[5:]:  # Bỏ qua 4 dòng đầu tiên
        #Mỗi dòng đều xóa khoảng trắng đầu cuối, tách chuỗi thành ds qua dấu , gáng lần lượt cho state1, input_char, state2
        state1, input_char, state2 = line.strip().split(',')
        # nếu khóa chưa có thì thêm key và giá trị là 1 ds rỗng vào từ điển.
        if (state1, input_char) not in transitions:
            transitions[(state1, input_char)] = []
        # thêm giá trị cho key của từ điển (cuối ds)
        transitions[(state1, input_char)].append(state2)
    print("Từ File =>\n")
    print(f"Các Trạng Thái {states}\n")
    print(f"Bộ Chữ Cái {alphabet}\n")
    print(f"Trạng Thái Bắt Đầu: {start_states}\n")
    print(f"Các Trạng Thái Được Chấp Nhận: {accept_states}\n")
    print(f"Các Trạng Hàm Chuyển {transitions}\n")

    return NFAe(states, alphabet, transitions, start_states, accept_states)


def print_nfae_file(filename):
    """In nội dung của file NFAe trước khi mô phỏng."""
    print(f"\nNội dung file '{filename}':\n")
    with open(filename, 'r') as file:
        content = file.read()
        print(content)


# Đọc NFAe từ file
filename = "nfae1.txt"
print_nfae_file(filename)  # In nội dung file trước khi chạy thuật toán
nfae = read_nfae_from_file(filename)

# Kiểm tra với các chuỗi đầu vào
while True:
    input_string = input("\nNhập chuỗi để kiểm tra (hoặc nhập 'exit' để thoát): ").strip()
    if input_string.lower() == 'exit':
        print("Chương trình kết thúc!")
        break
    print(f"\nMô phỏng cho chuỗi: '{input_string}'")
    nfae.simulate(input_string)