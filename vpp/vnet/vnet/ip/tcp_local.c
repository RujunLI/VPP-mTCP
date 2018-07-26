#include <vnet/ip/ip.h>
#include <vnet/ethernet/ethernet.h>
#include <vnet/ppp/ppp.h>
#include <vnet/hdlc/hdlc.h>
#include "tcp_local.h"
#include "tcp_error.h"
#include <mtcp_api.h>

typedef enum {
  TCP_INPUT_NEXT_DROP,
  TCP_INPUT_NEXT_PUNT,
  TCP_INPUT_N_NEXT,
} tcp_input_next_t;

extern int sched_getcpu(void);

typedef struct{
	u8 packet_data[20];
}tcp_input_trace_t;

u8 * format_tcp_header (u8 * s, va_list * args)
{
        s = format(s, "tcp format will support later!");
        return s;
}

static u8 * format_tcp_input_trace (u8 * s, va_list * va)
{
  CLIB_UNUSED (vlib_main_t * vm) = va_arg (*va, vlib_main_t *);
  CLIB_UNUSED (vlib_node_t * node) = va_arg (*va, vlib_node_t *);
  tcp_input_trace_t * t = va_arg (*va, tcp_input_trace_t *);
  
   s = format (s, "%U",
              format_tcp_header,
              t->packet_data, sizeof (t->packet_data));

  return s;
}

static char * tcp_error_strings[] = {
#define _(sym,string) string,
  foreach_tcp_error
#undef _
};

VLIB_REGISTER_NODE (tcp_input_node) = {
  .function = ip4_tcp_input,
  .name = "tcp-input",
  .vector_size = sizeof (u32),
  .n_errors = TCP_N_ERROR,
  .error_strings = tcp_error_strings,

  .n_next_nodes = TCP_INPUT_N_NEXT,
  .next_nodes = {
    [TCP_INPUT_NEXT_DROP] = "error-drop",
    [TCP_INPUT_NEXT_PUNT] = "error-punt",
  },

  .format_buffer = format_tcp_header,
  .format_trace = format_tcp_input_trace,
};

static uword ip4_tcp_input(vlib_main_t * vm,
		vlib_node_runtime_t * node,
		vlib_frame_t * frame){
        int cpu_id = os_get_cpu_number();
        printf("cpu %d", cpu_id);
        cpu_id = sched_getcpu();
        printf("cpu %d", cpu_id);
        //mtcp_create_context(cpu_id);
	flag3 = 1;
	return 0;
}

