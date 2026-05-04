#include "fsm.h"

fsm_state_t fsm_state = ST_IDLE;

void fsm_tick(bool start){
    switch(fsm_state){
        case ST_IDLE: if(start) fsm_state = ST_START; break;
        case ST_START: fsm_state = ST_STREAM; break;
        case ST_STREAM: break; // pipeline handles pixel stream
        case ST_DONE: break;
    }
}
