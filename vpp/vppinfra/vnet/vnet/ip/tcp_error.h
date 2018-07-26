#ifndef VNET_VNET_IP_TCP_ERROR_H_
#define VNET_VNET_IP_TCP_ERROR_H_

#define foreach_tcp_error						\
  /* Must be first. */							\
  _ (NONE, "valid tcp packets")						\
									\
  _ (BUF_ADJUST, "buffer to OFP error")							\
  _ (DO_TCP, "tcp processing error")							\
  /* Errors signalled by ip4-input */					\
  _ (TOO_SHORT, "ip4 length < 20 bytes")				\
  _ (BAD_LENGTH, "ip4 length > l2 length")				\
  _ (BAD_CHECKSUM, "bad ip4 checksum")					\
  _ (VERSION, "ip4 version != 4")					\
  _ (OPTIONS, "ip4 options present")					\
  _ (FRAGMENT_OFFSET_ONE, "ip4 fragment offset == 1")			\
  _ (TIME_EXPIRED, "ip4 ttl <= 1")					\
									\
  /* Errors signalled by ip4-rewrite. */				\
  _ (MTU_EXCEEDED, "ip4 MTU exceeded and DF set")			\
  _ (DST_LOOKUP_MISS, "ip4 destination lookup miss")			\
  _ (SRC_LOOKUP_MISS, "ip4 source lookup miss")				\
  _ (ADJACENCY_DROP, "ip4 adjacency drop")				\
  _ (ADJACENCY_PUNT, "ip4 adjacency punt")				\
									\
  /* Errors signalled by ip4-local. */					\
  _ (UNKNOWN_PROTOCOL, "unknown ip protocol")				\
  _ (TCP_CHECKSUM, "bad tcp checksum")					\
  _ (UDP_CHECKSUM, "bad udp checksum")					\
  _ (UDP_LENGTH, "inconsistent udp/ip lengths")				\
									\
  /* Errors signalled by ip4-source-check. */				\
  _ (UNICAST_SOURCE_CHECK_FAILS, "ip4 unicast source check fails")	\
                                                                        \
  /* Spoofed packets in ip4-rewrite-local */                            \
  _(SPOOFED_LOCAL_PACKETS, "ip4 spoofed local-address packet drops")    \
                                                                        \
 /* Erros singalled by ip4-inacl */                                     \
  _ (INACL_TABLE_MISS, "input ACL table-miss drops")                    \
  _ (INACL_SESSION_DENY, "input ACL session deny drops")

typedef enum {
#define _(sym,str) TCP_ERROR_##sym,
  foreach_tcp_error
#undef _
  TCP_N_ERROR,
} tcp_error_t;

#endif /* VNET_VNET_IP_TCP_ERROR_H_ */

