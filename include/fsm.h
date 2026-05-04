#pragma once

enum fsm_state_t{
    ST_IDLE,
    ST_START,
    ST_STREAM,
    ST_DONE
};

extern fsm_state_t fsm_state;
void fsm_tick(bool start);
