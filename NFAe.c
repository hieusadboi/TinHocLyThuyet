#include <stdio.h>
#include <stdbool.h>

#define MAX_STATES 3
#define MAX_INPUT_LENGTH 100

void epsilon_closure(int state, bool closure[MAX_STATES]) {
    if (closure[state]) return;

    closure[state] = true;

    if (state == 0) {
        epsilon_closure(1, closure);
        epsilon_closure(2, closure);
    }
    if (state == 1) {
        epsilon_closure(2, closure);
    }
}

void delta(int state, char input, bool next_states[MAX_STATES]) {
    for (int i = 0; i < MAX_STATES; i++) {
        next_states[i] = false;
    }

    if (state == 0) {
        if (input == '0') {
            next_states[0] = true;
        } else if (input == '1') {
            next_states[1] = true;
        } else if (input == '2') {
            next_states[2] = true;
        }
    } else if (state == 1) {
        if (input == '1') {
            next_states[1] = true;
        } else if (input == '2') {
            next_states[2] = true;
        }
    } else if (state == 2) {
        if (input == '2') {
            next_states[2] = true;
        }
    }
}

bool simulate_nfa(char *input, int start_state, int final_state) {
    bool closure[MAX_STATES] = {false};
    bool next_states[MAX_STATES] = {false};

    epsilon_closure(start_state, closure);

    for (int i = 0; input[i] != '\0'; i++) {
        char c = input[i];
        bool temp_states[MAX_STATES] = {false};

        for (int state = 0; state < MAX_STATES; state++) {
            if (closure[state]) {
                delta(state, c, next_states);
                for (int j = 0; j < MAX_STATES; j++) {
                    if (next_states[j]) {
                        temp_states[j] = true;
                    }
                }
            }
        }

        for (int j = 0; j < MAX_STATES; j++) {
            closure[j] = false;
        }

        for (int state = 0; state < MAX_STATES; state++) {
            if (temp_states[state]) {
                epsilon_closure(state, closure);
            }
        }
    }

    return closure[final_state];
}

int main() {
    char input[MAX_INPUT_LENGTH];
    int start_state = 0;
    int final_state = 2;

    printf("INPUT: ");
    scanf("%s", input);

    if (simulate_nfa(input, start_state, final_state)) {
        printf("YES\n");
    } else {
        printf("NO\n");
    }

    return 0;
}
