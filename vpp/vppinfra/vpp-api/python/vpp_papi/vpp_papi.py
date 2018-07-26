

#
# AUTO-GENERATED FILE. PLEASE DO NOT EDIT.
#
import sys, time, threading, signal, os, logging
from struct import *
from collections import namedtuple

#
# Import C API shared object
#
import vpp_api

context = 0
results = {}
waiting_for_reply = False

#
# XXX: Make this return a unique number
#
def get_context(id):
    global context
    context += 1
    return context

def msg_handler(msg):
    global result, context, event_callback, waiting_for_reply
    if not msg:
        logging.warning('vpp_api.read failed')
        return

    id = unpack('>H', msg[0:2])
    logging.debug('Received message', id[0])
    if id[0] == VL_API_RX_THREAD_EXIT:
        logging.info("We got told to leave")
        return;

    #
    # Decode message and returns a tuple.
    #
    logging.debug('api_func', api_func_table[id[0]])
    r = api_func_table[id[0]](msg)
    if not r:
        logging.warning('Message decode failed', id[0])
        return

    if 'context' in r._asdict():
        if r.context > 0:
            context = r.context

    #
    # XXX: Call provided callback for event
    # Are we guaranteed to not get an event during processing of other messages?
    # How to differentiate what's a callback message and what not? Context = 0?
    #
    logging.debug('R:', context, r, waiting_for_reply)
    if waiting_for_reply == False:
        event_callback(r)
        return

    #
    # Collect results until control ping
    #
    if id[0] == VL_API_CONTROL_PING_REPLY:
        results[context]['e'].set()
        waiting_for_reply = False
        return
    if not context in results:
        logging.warning('Not expecting results for this context', context)
        return
    if 'm' in results[context]:
        results[context]['r'].append(r)
        return

    results[context]['r'] = r
    results[context]['e'].set()
    waiting_for_reply = False

def connect(name):
    signal.alarm(3) # 3 second
    rv = vpp_api.connect(name, msg_handler)
    signal.alarm(0)
    logging.info("Connect:", rv)
    return rv

def disconnect():
    rv = vpp_api.disconnect()
    logging.info("Disconnected")
    return rv

def register_event_callback(callback):
    global event_callback
    event_callback = callback

VL_API_MEMCLNT_CREATE = 1
VL_API_MEMCLNT_CREATE_REPLY = 2
VL_API_MEMCLNT_DELETE = 3
VL_API_MEMCLNT_DELETE_REPLY = 4
VL_API_RX_THREAD_EXIT = 5
VL_API_RPC_CALL = 6
VL_API_RPC_REPLY = 7
VL_API_GET_FIRST_MSG_ID = 8
VL_API_GET_FIRST_MSG_ID_REPLY = 9
VL_API_WANT_INTERFACE_EVENTS = 10
VL_API_WANT_INTERFACE_EVENTS_REPLY = 11
VL_API_SW_INTERFACE_DETAILS = 12
VL_API_SW_INTERFACE_SET_FLAGS = 13
VL_API_SW_INTERFACE_SET_FLAGS_REPLY = 14
VL_API_SW_INTERFACE_DUMP = 15
VL_API_SW_INTERFACE_ADD_DEL_ADDRESS = 16
VL_API_SW_INTERFACE_ADD_DEL_ADDRESS_REPLY = 17
VL_API_SW_INTERFACE_SET_TABLE = 18
VL_API_SW_INTERFACE_SET_TABLE_REPLY = 19
VL_API_TAP_CONNECT = 20
VL_API_TAP_CONNECT_REPLY = 21
VL_API_TAP_MODIFY = 22
VL_API_TAP_MODIFY_REPLY = 23
VL_API_TAP_DELETE = 24
VL_API_TAP_DELETE_REPLY = 25
VL_API_SW_INTERFACE_TAP_DUMP = 26
VL_API_SW_INTERFACE_TAP_DETAILS = 27
VL_API_CREATE_VLAN_SUBIF = 28
VL_API_CREATE_VLAN_SUBIF_REPLY = 29
VL_API_IP_ADD_DEL_ROUTE = 30
VL_API_IP_ADD_DEL_ROUTE_REPLY = 31
VL_API_MPLS_GRE_ADD_DEL_TUNNEL = 32
VL_API_MPLS_GRE_ADD_DEL_TUNNEL_REPLY = 33
VL_API_MPLS_ADD_DEL_ENCAP = 34
VL_API_MPLS_ADD_DEL_ENCAP_REPLY = 35
VL_API_MPLS_ADD_DEL_DECAP = 36
VL_API_MPLS_ADD_DEL_DECAP_REPLY = 37
VL_API_PROXY_ARP_ADD_DEL = 38
VL_API_PROXY_ARP_ADD_DEL_REPLY = 39
VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE = 40
VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE_REPLY = 41
VL_API_IP_NEIGHBOR_ADD_DEL = 42
VL_API_IP_NEIGHBOR_ADD_DEL_REPLY = 43
VL_API_RESET_VRF = 44
VL_API_RESET_VRF_REPLY = 45
VL_API_IS_ADDRESS_REACHABLE = 46
VL_API_WANT_STATS = 47
VL_API_WANT_STATS_REPLY = 48
VL_API_VNET_INTERFACE_COUNTERS = 49
VL_API_VNET_IP4_FIB_COUNTERS = 50
VL_API_VNET_IP6_FIB_COUNTERS = 51
VL_API_VNET_GET_SUMMARY_STATS = 52
VL_API_VNET_SUMMARY_STATS_REPLY = 53
VL_API_OAM_EVENT = 54
VL_API_WANT_OAM_EVENTS = 55
VL_API_WANT_OAM_EVENTS_REPLY = 56
VL_API_OAM_ADD_DEL = 57
VL_API_OAM_ADD_DEL_REPLY = 58
VL_API_RESET_FIB = 59
VL_API_RESET_FIB_REPLY = 60
VL_API_DHCP_PROXY_CONFIG = 61
VL_API_DHCP_PROXY_CONFIG_REPLY = 62
VL_API_DHCP_PROXY_SET_VSS = 63
VL_API_DHCP_PROXY_SET_VSS_REPLY = 64
VL_API_SET_IP_FLOW_HASH = 65
VL_API_SET_IP_FLOW_HASH_REPLY = 66
VL_API_SW_INTERFACE_IP6ND_RA_CONFIG = 67
VL_API_SW_INTERFACE_IP6ND_RA_CONFIG_REPLY = 68
VL_API_SW_INTERFACE_IP6ND_RA_PREFIX = 69
VL_API_SW_INTERFACE_IP6ND_RA_PREFIX_REPLY = 70
VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE = 71
VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE_REPLY = 72
VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS = 73
VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS_REPLY = 74
VL_API_SW_INTERFACE_SET_UNNUMBERED = 75
VL_API_SW_INTERFACE_SET_UNNUMBERED_REPLY = 76
VL_API_CREATE_LOOPBACK = 77
VL_API_CREATE_LOOPBACK_REPLY = 78
VL_API_DELETE_LOOPBACK = 79
VL_API_DELETE_LOOPBACK_REPLY = 80
VL_API_CONTROL_PING = 81
VL_API_CONTROL_PING_REPLY = 82
VL_API_CLI_REQUEST = 83
VL_API_CLI_REPLY = 84
VL_API_SET_ARP_NEIGHBOR_LIMIT = 85
VL_API_SET_ARP_NEIGHBOR_LIMIT_REPLY = 86
VL_API_L2_PATCH_ADD_DEL = 87
VL_API_L2_PATCH_ADD_DEL_REPLY = 88
VL_API_SR_TUNNEL_ADD_DEL = 89
VL_API_SR_TUNNEL_ADD_DEL_REPLY = 90
VL_API_SR_POLICY_ADD_DEL = 91
VL_API_SR_POLICY_ADD_DEL_REPLY = 92
VL_API_SR_MULTICAST_MAP_ADD_DEL = 93
VL_API_SR_MULTICAST_MAP_ADD_DEL_REPLY = 94
VL_API_SW_INTERFACE_SET_VPATH = 95
VL_API_SW_INTERFACE_SET_VPATH_REPLY = 96
VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL = 97
VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_REPLY = 98
VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2 = 99
VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2_REPLY = 100
VL_API_SW_INTERFACE_SET_L2_XCONNECT = 101
VL_API_SW_INTERFACE_SET_L2_XCONNECT_REPLY = 102
VL_API_SW_INTERFACE_SET_L2_BRIDGE = 103
VL_API_SW_INTERFACE_SET_L2_BRIDGE_REPLY = 104
VL_API_L2FIB_ADD_DEL = 105
VL_API_L2FIB_ADD_DEL_REPLY = 106
VL_API_L2_FLAGS = 107
VL_API_L2_FLAGS_REPLY = 108
VL_API_BRIDGE_FLAGS = 109
VL_API_BRIDGE_FLAGS_REPLY = 110
VL_API_BD_IP_MAC_ADD_DEL = 111
VL_API_BD_IP_MAC_ADD_DEL_REPLY = 112
VL_API_CLASSIFY_ADD_DEL_TABLE = 113
VL_API_CLASSIFY_ADD_DEL_TABLE_REPLY = 114
VL_API_CLASSIFY_ADD_DEL_SESSION = 115
VL_API_CLASSIFY_ADD_DEL_SESSION_REPLY = 116
VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE = 117
VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE_REPLY = 118
VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES = 119
VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES_REPLY = 120
VL_API_GET_NODE_INDEX = 121
VL_API_GET_NODE_INDEX_REPLY = 122
VL_API_ADD_NODE_NEXT = 123
VL_API_ADD_NODE_NEXT_REPLY = 124
VL_API_DHCP_PROXY_CONFIG_2 = 125
VL_API_DHCP_PROXY_CONFIG_2_REPLY = 126
VL_API_L2TPV3_CREATE_TUNNEL = 127
VL_API_L2TPV3_CREATE_TUNNEL_REPLY = 128
VL_API_L2TPV3_SET_TUNNEL_COOKIES = 129
VL_API_L2TPV3_SET_TUNNEL_COOKIES_REPLY = 130
VL_API_SW_IF_L2TPV3_TUNNEL_DETAILS = 131
VL_API_SW_IF_L2TPV3_TUNNEL_DUMP = 132
VL_API_L2_FIB_CLEAR_TABLE = 133
VL_API_L2_FIB_CLEAR_TABLE_REPLY = 134
VL_API_L2_INTERFACE_EFP_FILTER = 135
VL_API_L2_INTERFACE_EFP_FILTER_REPLY = 136
VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE = 137
VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE_REPLY = 138
VL_API_L2TPV3_SET_LOOKUP_KEY = 139
VL_API_L2TPV3_SET_LOOKUP_KEY_REPLY = 140
VL_API_VXLAN_ADD_DEL_TUNNEL = 141
VL_API_VXLAN_ADD_DEL_TUNNEL_REPLY = 142
VL_API_VXLAN_TUNNEL_DUMP = 143
VL_API_VXLAN_TUNNEL_DETAILS = 144
VL_API_GRE_ADD_DEL_TUNNEL = 145
VL_API_GRE_ADD_DEL_TUNNEL_REPLY = 146
VL_API_GRE_TUNNEL_DUMP = 147
VL_API_GRE_TUNNEL_DETAILS = 148
VL_API_L2_INTERFACE_VLAN_TAG_REWRITE = 149
VL_API_L2_INTERFACE_VLAN_TAG_REWRITE_REPLY = 150
VL_API_CREATE_VHOST_USER_IF = 151
VL_API_CREATE_VHOST_USER_IF_REPLY = 152
VL_API_MODIFY_VHOST_USER_IF = 153
VL_API_MODIFY_VHOST_USER_IF_REPLY = 154
VL_API_DELETE_VHOST_USER_IF = 155
VL_API_DELETE_VHOST_USER_IF_REPLY = 156
VL_API_CREATE_SUBIF = 157
VL_API_CREATE_SUBIF_REPLY = 158
VL_API_SHOW_VERSION = 159
VL_API_SHOW_VERSION_REPLY = 160
VL_API_SW_INTERFACE_VHOST_USER_DETAILS = 161
VL_API_SW_INTERFACE_VHOST_USER_DUMP = 162
VL_API_IP_ADDRESS_DETAILS = 163
VL_API_IP_ADDRESS_DUMP = 164
VL_API_IP_DETAILS = 165
VL_API_IP_DUMP = 166
VL_API_L2_FIB_TABLE_ENTRY = 167
VL_API_L2_FIB_TABLE_DUMP = 168
VL_API_VXLAN_GPE_ADD_DEL_TUNNEL = 169
VL_API_VXLAN_GPE_ADD_DEL_TUNNEL_REPLY = 170
VL_API_LISP_ADD_DEL_LOCATOR_SET = 171
VL_API_LISP_ADD_DEL_LOCATOR_SET_REPLY = 172
VL_API_LISP_ADD_DEL_LOCATOR = 173
VL_API_LISP_ADD_DEL_LOCATOR_REPLY = 174
VL_API_LISP_ADD_DEL_LOCAL_EID = 175
VL_API_LISP_ADD_DEL_LOCAL_EID_REPLY = 176
VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY = 177
VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY_REPLY = 178
VL_API_LISP_ADD_DEL_MAP_RESOLVER = 179
VL_API_LISP_ADD_DEL_MAP_RESOLVER_REPLY = 180
VL_API_LISP_GPE_ENABLE_DISABLE = 181
VL_API_LISP_GPE_ENABLE_DISABLE_REPLY = 182
VL_API_LISP_ENABLE_DISABLE = 183
VL_API_LISP_ENABLE_DISABLE_REPLY = 184
VL_API_LISP_GPE_ADD_DEL_IFACE = 185
VL_API_LISP_GPE_ADD_DEL_IFACE_REPLY = 186
VL_API_LISP_ADD_DEL_REMOTE_MAPPING = 187
VL_API_LISP_ADD_DEL_REMOTE_MAPPING_REPLY = 188
VL_API_LISP_LOCATOR_SET_DETAILS = 189
VL_API_LISP_LOCATOR_SET_DUMP = 190
VL_API_LISP_LOCAL_EID_TABLE_DETAILS = 191
VL_API_LISP_LOCAL_EID_TABLE_DUMP = 192
VL_API_LISP_GPE_TUNNEL_DETAILS = 193
VL_API_LISP_GPE_TUNNEL_DUMP = 194
VL_API_LISP_MAP_RESOLVER_DETAILS = 195
VL_API_LISP_MAP_RESOLVER_DUMP = 196
VL_API_LISP_ENABLE_DISABLE_STATUS_DETAILS = 197
VL_API_LISP_ENABLE_DISABLE_STATUS_DUMP = 198
VL_API_INTERFACE_NAME_RENUMBER = 199
VL_API_INTERFACE_NAME_RENUMBER_REPLY = 200
VL_API_WANT_IP4_ARP_EVENTS = 201
VL_API_WANT_IP4_ARP_EVENTS_REPLY = 202
VL_API_IP4_ARP_EVENT = 203
VL_API_BRIDGE_DOMAIN_ADD_DEL = 204
VL_API_BRIDGE_DOMAIN_ADD_DEL_REPLY = 205
VL_API_BRIDGE_DOMAIN_DUMP = 206
VL_API_BRIDGE_DOMAIN_DETAILS = 207
VL_API_BRIDGE_DOMAIN_SW_IF_DETAILS = 208
VL_API_DHCP_CLIENT_CONFIG = 209
VL_API_DHCP_CLIENT_CONFIG_REPLY = 210
VL_API_INPUT_ACL_SET_INTERFACE = 211
VL_API_INPUT_ACL_SET_INTERFACE_REPLY = 212
VL_API_IPSEC_SPD_ADD_DEL = 213
VL_API_IPSEC_SPD_ADD_DEL_REPLY = 214
VL_API_IPSEC_INTERFACE_ADD_DEL_SPD = 215
VL_API_IPSEC_INTERFACE_ADD_DEL_SPD_REPLY = 216
VL_API_IPSEC_SPD_ADD_DEL_ENTRY = 217
VL_API_IPSEC_SPD_ADD_DEL_ENTRY_REPLY = 218
VL_API_IPSEC_SAD_ADD_DEL_ENTRY = 219
VL_API_IPSEC_SAD_ADD_DEL_ENTRY_REPLY = 220
VL_API_IPSEC_SA_SET_KEY = 221
VL_API_IPSEC_SA_SET_KEY_REPLY = 222
VL_API_IKEV2_PROFILE_ADD_DEL = 223
VL_API_IKEV2_PROFILE_ADD_DEL_REPLY = 224
VL_API_IKEV2_PROFILE_SET_AUTH = 225
VL_API_IKEV2_PROFILE_SET_AUTH_REPLY = 226
VL_API_IKEV2_PROFILE_SET_ID = 227
VL_API_IKEV2_PROFILE_SET_ID_REPLY = 228
VL_API_IKEV2_PROFILE_SET_TS = 229
VL_API_IKEV2_PROFILE_SET_TS_REPLY = 230
VL_API_IKEV2_SET_LOCAL_KEY = 231
VL_API_IKEV2_SET_LOCAL_KEY_REPLY = 232
VL_API_DHCP_COMPL_EVENT = 233
VL_API_MAP_ADD_DOMAIN = 234
VL_API_MAP_ADD_DOMAIN_REPLY = 235
VL_API_MAP_DEL_DOMAIN = 236
VL_API_MAP_DEL_DOMAIN_REPLY = 237
VL_API_MAP_ADD_DEL_RULE = 238
VL_API_MAP_ADD_DEL_RULE_REPLY = 239
VL_API_MAP_DOMAIN_DUMP = 240
VL_API_MAP_DOMAIN_DETAILS = 241
VL_API_MAP_RULE_DUMP = 242
VL_API_MAP_RULE_DETAILS = 243
VL_API_MAP_SUMMARY_STATS = 244
VL_API_MAP_SUMMARY_STATS_REPLY = 245
VL_API_COP_INTERFACE_ENABLE_DISABLE = 246
VL_API_COP_INTERFACE_ENABLE_DISABLE_REPLY = 247
VL_API_COP_WHITELIST_ENABLE_DISABLE = 248
VL_API_COP_WHITELIST_ENABLE_DISABLE_REPLY = 249
VL_API_GET_NODE_GRAPH = 250
VL_API_GET_NODE_GRAPH_REPLY = 251
VL_API_SW_INTERFACE_CLEAR_STATS = 252
VL_API_SW_INTERFACE_CLEAR_STATS_REPLY = 253
VL_API_TRACE_PROFILE_ADD = 254
VL_API_TRACE_PROFILE_ADD_REPLY = 255
VL_API_TRACE_PROFILE_APPLY = 256
VL_API_TRACE_PROFILE_APPLY_REPLY = 257
VL_API_TRACE_PROFILE_DEL = 258
VL_API_TRACE_PROFILE_DEL_REPLY = 259
VL_API_AF_PACKET_CREATE = 260
VL_API_AF_PACKET_CREATE_REPLY = 261
VL_API_AF_PACKET_DELETE = 262
VL_API_AF_PACKET_DELETE_REPLY = 263
VL_API_POLICER_ADD_DEL = 264
VL_API_POLICER_ADD_DEL_REPLY = 265
def want_interface_events_decode(msg):
    n = namedtuple('want_interface_events', 'vl_msg_id, client_index, context, enable_disable, pid')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def want_interface_events(enable_disable, pid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_INTERFACE_EVENTS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_WANT_INTERFACE_EVENTS, 0, context, enable_disable, pid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_interface_events_reply_decode(msg):
    n = namedtuple('want_interface_events_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def want_interface_events_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_INTERFACE_EVENTS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_WANT_INTERFACE_EVENTS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_details_decode(msg):
    n = namedtuple('sw_interface_details', 'vl_msg_id, context, sw_if_index, sup_sw_if_index, l2_address_length, l2_address, interface_name, admin_up_down, link_up_down, link_duplex, link_speed, link_mtu, sub_id, sub_dot1ad, sub_number_of_tags, sub_outer_vlan_id, sub_inner_vlan_id, sub_exact_match, sub_default, sub_outer_vlan_id_any, sub_inner_vlan_id_any, vtr_op, vtr_push_dot1q, vtr_tag1, vtr_tag2')
    if not n:
        return None
    
    tr = unpack('>HIIII8s64sBBBBHIBBHHBBBBIIII', msg[:126])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],tr[15],tr[16],tr[17],tr[18],tr[19],tr[20],tr[21],tr[22],tr[23],tr[24],))
    if not r:
        return None
    return r
    
def sw_interface_details(sup_sw_if_index, l2_address_length, l2_address, interface_name, admin_up_down, link_up_down, link_duplex, link_speed, link_mtu, sub_id, sub_dot1ad, sub_number_of_tags, sub_outer_vlan_id, sub_inner_vlan_id, sub_exact_match, sub_default, sub_outer_vlan_id_any, sub_inner_vlan_id_any, vtr_op, vtr_push_dot1q, vtr_tag1, vtr_tag2, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII8s64sBBBBHIBBHHBBBBIIII', VL_API_SW_INTERFACE_DETAILS, 0, context, sup_sw_if_index, l2_address_length, l2_address, interface_name, admin_up_down, link_up_down, link_duplex, link_speed, link_mtu, sub_id, sub_dot1ad, sub_number_of_tags, sub_outer_vlan_id, sub_inner_vlan_id, sub_exact_match, sub_default, sub_outer_vlan_id_any, sub_inner_vlan_id_any, vtr_op, vtr_push_dot1q, vtr_tag1, vtr_tag2))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_flags_decode(msg):
    n = namedtuple('sw_interface_set_flags', 'vl_msg_id, client_index, context, sw_if_index, admin_up_down, link_up_down, deleted')
    if not n:
        return None
    
    tr = unpack('>HIIIBBB', msg[:17])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def sw_interface_set_flags(sw_if_index, admin_up_down, link_up_down, deleted, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_FLAGS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBB', VL_API_SW_INTERFACE_SET_FLAGS, 0, context, sw_if_index, admin_up_down, link_up_down, deleted))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_flags_reply_decode(msg):
    n = namedtuple('sw_interface_set_flags_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_flags_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_FLAGS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_FLAGS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_dump_decode(msg):
    n = namedtuple('sw_interface_dump', 'vl_msg_id, client_index, context, name_filter_valid, name_filter')
    if not n:
        return None
    
    tr = unpack('>HIIB49s', msg[:60])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def sw_interface_dump(name_filter_valid, name_filter, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIIB49s', VL_API_SW_INTERFACE_DUMP, 0, context, name_filter_valid, name_filter))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_add_del_address_decode(msg):
    n = namedtuple('sw_interface_add_del_address', 'vl_msg_id, client_index, context, sw_if_index, is_add, is_ipv6, del_all, address_length, address')
    if not n:
        return None
    
    tr = unpack('>HIIIBBBB16s', msg[:34])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def sw_interface_add_del_address(sw_if_index, is_add, is_ipv6, del_all, address_length, address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_ADD_DEL_ADDRESS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBBB16s', VL_API_SW_INTERFACE_ADD_DEL_ADDRESS, 0, context, sw_if_index, is_add, is_ipv6, del_all, address_length, address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_add_del_address_reply_decode(msg):
    n = namedtuple('sw_interface_add_del_address_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_add_del_address_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_ADD_DEL_ADDRESS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_ADD_DEL_ADDRESS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_table_decode(msg):
    n = namedtuple('sw_interface_set_table', 'vl_msg_id, client_index, context, sw_if_index, is_ipv6, vrf_id')
    if not n:
        return None
    
    tr = unpack('>HIIIBI', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def sw_interface_set_table(sw_if_index, is_ipv6, vrf_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_TABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBI', VL_API_SW_INTERFACE_SET_TABLE, 0, context, sw_if_index, is_ipv6, vrf_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_table_reply_decode(msg):
    n = namedtuple('sw_interface_set_table_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_table_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_TABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_TABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_connect_decode(msg):
    n = namedtuple('tap_connect', 'vl_msg_id, client_index, context, use_random_mac, tap_name, mac_address, renumber, custom_dev_instance')
    if not n:
        return None
    
    tr = unpack('>HIIB64s6sBI', msg[:86])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def tap_connect(use_random_mac, tap_name, mac_address, renumber, custom_dev_instance, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_CONNECT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64s6sBI', VL_API_TAP_CONNECT, 0, context, use_random_mac, tap_name, mac_address, renumber, custom_dev_instance))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_connect_reply_decode(msg):
    n = namedtuple('tap_connect_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def tap_connect_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_CONNECT_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_TAP_CONNECT_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_modify_decode(msg):
    n = namedtuple('tap_modify', 'vl_msg_id, client_index, context, sw_if_index, use_random_mac, tap_name, mac_address, renumber, custom_dev_instance')
    if not n:
        return None
    
    tr = unpack('>HIIIB64s6sBI', msg[:90])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def tap_modify(sw_if_index, use_random_mac, tap_name, mac_address, renumber, custom_dev_instance, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_MODIFY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB64s6sBI', VL_API_TAP_MODIFY, 0, context, sw_if_index, use_random_mac, tap_name, mac_address, renumber, custom_dev_instance))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_modify_reply_decode(msg):
    n = namedtuple('tap_modify_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def tap_modify_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_MODIFY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_TAP_MODIFY_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_delete_decode(msg):
    n = namedtuple('tap_delete', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def tap_delete(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_DELETE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_TAP_DELETE, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def tap_delete_reply_decode(msg):
    n = namedtuple('tap_delete_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def tap_delete_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_TAP_DELETE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_TAP_DELETE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_tap_dump_decode(msg):
    n = namedtuple('sw_interface_tap_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_tap_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_TAP_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_SW_INTERFACE_TAP_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_tap_details_decode(msg):
    n = namedtuple('sw_interface_tap_details', 'vl_msg_id, context, sw_if_index, dev_name')
    if not n:
        return None
    
    tr = unpack('>HII64s', msg[:74])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def sw_interface_tap_details(dev_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_TAP_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s', VL_API_SW_INTERFACE_TAP_DETAILS, 0, context, dev_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_vlan_subif_decode(msg):
    n = namedtuple('create_vlan_subif', 'vl_msg_id, client_index, context, sw_if_index, vlan_id')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def create_vlan_subif(sw_if_index, vlan_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_VLAN_SUBIF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_CREATE_VLAN_SUBIF, 0, context, sw_if_index, vlan_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_vlan_subif_reply_decode(msg):
    n = namedtuple('create_vlan_subif_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def create_vlan_subif_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_VLAN_SUBIF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_CREATE_VLAN_SUBIF_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_add_del_route_decode(msg):
    n = namedtuple('ip_add_del_route', 'vl_msg_id, client_index, context, next_hop_sw_if_index, vrf_id, lookup_in_vrf, resolve_attempts, classify_table_index, create_vrf_if_needed, resolve_if_needed, is_add, is_drop, is_ipv6, is_local, is_classify, is_multipath, not_last, next_hop_weight, dst_address_length, dst_address, next_hop_address')
    if not n:
        return None
    
    tr = unpack('>HIIIIIIIBBBBBBBBBBB16s16s', msg[:73])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],tr[15],tr[16],tr[17],tr[18],tr[19],tr[20],))
    if not r:
        return None
    return r
    
def ip_add_del_route(next_hop_sw_if_index, vrf_id, lookup_in_vrf, resolve_attempts, classify_table_index, create_vrf_if_needed, resolve_if_needed, is_add, is_drop, is_ipv6, is_local, is_classify, is_multipath, not_last, next_hop_weight, dst_address_length, dst_address, next_hop_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_ADD_DEL_ROUTE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIIIBBBBBBBBBBB16s16s', VL_API_IP_ADD_DEL_ROUTE, 0, context, next_hop_sw_if_index, vrf_id, lookup_in_vrf, resolve_attempts, classify_table_index, create_vrf_if_needed, resolve_if_needed, is_add, is_drop, is_ipv6, is_local, is_classify, is_multipath, not_last, next_hop_weight, dst_address_length, dst_address, next_hop_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_add_del_route_reply_decode(msg):
    n = namedtuple('ip_add_del_route_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ip_add_del_route_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_ADD_DEL_ROUTE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IP_ADD_DEL_ROUTE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_gre_add_del_tunnel_decode(msg):
    n = namedtuple('mpls_gre_add_del_tunnel', 'vl_msg_id, client_index, context, inner_vrf_id, outer_vrf_id, is_add, l2_only, src_address, dst_address, intfc_address, intfc_address_length')
    if not n:
        return None
    
    tr = unpack('>HIIIIBB4s4s4sB', msg[:33])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],))
    if not r:
        return None
    return r
    
def mpls_gre_add_del_tunnel(inner_vrf_id, outer_vrf_id, is_add, l2_only, src_address, dst_address, intfc_address, intfc_address_length, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_GRE_ADD_DEL_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBB4s4s4sB', VL_API_MPLS_GRE_ADD_DEL_TUNNEL, 0, context, inner_vrf_id, outer_vrf_id, is_add, l2_only, src_address, dst_address, intfc_address, intfc_address_length))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_gre_add_del_tunnel_reply_decode(msg):
    n = namedtuple('mpls_gre_add_del_tunnel_reply', 'vl_msg_id, context, retval, tunnel_sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def mpls_gre_add_del_tunnel_reply(tunnel_sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_GRE_ADD_DEL_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_MPLS_GRE_ADD_DEL_TUNNEL_REPLY, 0, context, tunnel_sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_add_del_encap_decode(msg):
    n = namedtuple('mpls_add_del_encap', 'vl_msg_id, client_index, context, vrf_id, dst_address, is_add, nlabels, labels')
    if not n:
        return None
    
    tr = unpack('>HIII4sBB', msg[:20])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],msg[20:],))
    if not r:
        return None
    return r
    
def mpls_add_del_encap(vrf_id, dst_address, is_add, nlabels, labels, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ADD_DEL_ENCAP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII4sBB', VL_API_MPLS_ADD_DEL_ENCAP, 0, context, vrf_id, dst_address, is_add, nlabels) + labels)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_add_del_encap_reply_decode(msg):
    n = namedtuple('mpls_add_del_encap_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def mpls_add_del_encap_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ADD_DEL_ENCAP_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MPLS_ADD_DEL_ENCAP_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_add_del_decap_decode(msg):
    n = namedtuple('mpls_add_del_decap', 'vl_msg_id, client_index, context, rx_vrf_id, tx_vrf_id, label, next_index, s_bit, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIIIBB', msg[:28])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def mpls_add_del_decap(rx_vrf_id, tx_vrf_id, label, next_index, s_bit, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ADD_DEL_DECAP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIIBB', VL_API_MPLS_ADD_DEL_DECAP, 0, context, rx_vrf_id, tx_vrf_id, label, next_index, s_bit, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_add_del_decap_reply_decode(msg):
    n = namedtuple('mpls_add_del_decap_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def mpls_add_del_decap_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ADD_DEL_DECAP_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MPLS_ADD_DEL_DECAP_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def proxy_arp_add_del_decode(msg):
    n = namedtuple('proxy_arp_add_del', 'vl_msg_id, client_index, context, vrf_id, is_add, low_address, hi_address')
    if not n:
        return None
    
    tr = unpack('>HIIIB4s4s', msg[:23])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def proxy_arp_add_del(vrf_id, is_add, low_address, hi_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_PROXY_ARP_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB4s4s', VL_API_PROXY_ARP_ADD_DEL, 0, context, vrf_id, is_add, low_address, hi_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def proxy_arp_add_del_reply_decode(msg):
    n = namedtuple('proxy_arp_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def proxy_arp_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_PROXY_ARP_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_PROXY_ARP_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def proxy_arp_intfc_enable_disable_decode(msg):
    n = namedtuple('proxy_arp_intfc_enable_disable', 'vl_msg_id, client_index, context, sw_if_index, enable_disable')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def proxy_arp_intfc_enable_disable(sw_if_index, enable_disable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE, 0, context, sw_if_index, enable_disable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def proxy_arp_intfc_enable_disable_reply_decode(msg):
    n = namedtuple('proxy_arp_intfc_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def proxy_arp_intfc_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_neighbor_add_del_decode(msg):
    n = namedtuple('ip_neighbor_add_del', 'vl_msg_id, client_index, context, vrf_id, sw_if_index, is_add, is_ipv6, is_static, mac_address, dst_address')
    if not n:
        return None
    
    tr = unpack('>HIIIIBBB6s16s', msg[:43])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def ip_neighbor_add_del(vrf_id, sw_if_index, is_add, is_ipv6, is_static, mac_address, dst_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_NEIGHBOR_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBBB6s16s', VL_API_IP_NEIGHBOR_ADD_DEL, 0, context, vrf_id, sw_if_index, is_add, is_ipv6, is_static, mac_address, dst_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_neighbor_add_del_reply_decode(msg):
    n = namedtuple('ip_neighbor_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ip_neighbor_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_NEIGHBOR_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IP_NEIGHBOR_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def reset_vrf_decode(msg):
    n = namedtuple('reset_vrf', 'vl_msg_id, client_index, context, is_ipv6, vrf_id')
    if not n:
        return None
    
    tr = unpack('>HIIBI', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def reset_vrf(is_ipv6, vrf_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_RESET_VRF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBI', VL_API_RESET_VRF, 0, context, is_ipv6, vrf_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def reset_vrf_reply_decode(msg):
    n = namedtuple('reset_vrf_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def reset_vrf_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_RESET_VRF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_RESET_VRF_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def is_address_reachable_decode(msg):
    n = namedtuple('is_address_reachable', 'vl_msg_id, client_index, context, next_hop_sw_if_index, is_known, is_ipv6, is_error, address')
    if not n:
        return None
    
    tr = unpack('>HIIIBBB16s', msg[:33])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def is_address_reachable(next_hop_sw_if_index, is_known, is_ipv6, is_error, address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IS_ADDRESS_REACHABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBB16s', VL_API_IS_ADDRESS_REACHABLE, 0, context, next_hop_sw_if_index, is_known, is_ipv6, is_error, address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_stats_decode(msg):
    n = namedtuple('want_stats', 'vl_msg_id, client_index, context, enable_disable, pid')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def want_stats(enable_disable, pid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_STATS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_WANT_STATS, 0, context, enable_disable, pid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_stats_reply_decode(msg):
    n = namedtuple('want_stats_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def want_stats_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_STATS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_WANT_STATS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vnet_interface_counters_decode(msg):
    n = namedtuple('vnet_interface_counters', 'vl_msg_id, vnet_counter_type, is_combined, first_sw_if_index, count, data')
    if not n:
        return None
    
    tr = unpack('>HBBII', msg[:12])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],msg[12:],))
    if not r:
        return None
    return r
    
def vnet_interface_counters(first_sw_if_index, count, data, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VNET_INTERFACE_COUNTERS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HBBII', VL_API_VNET_INTERFACE_COUNTERS, 0, context, first_sw_if_index, count) + data)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vnet_ip4_fib_counters_decode(msg):
    n = namedtuple('vnet_ip4_fib_counters', 'vl_msg_id, vrf_id, count, c')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],msg[10:],))
    if not r:
        return None
    return r
    
def vnet_ip4_fib_counters(c, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VNET_IP4_FIB_COUNTERS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_VNET_IP4_FIB_COUNTERS, 0, context, ) + c)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vnet_ip6_fib_counters_decode(msg):
    n = namedtuple('vnet_ip6_fib_counters', 'vl_msg_id, vrf_id, count, c')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],msg[10:],))
    if not r:
        return None
    return r
    
def vnet_ip6_fib_counters(c, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VNET_IP6_FIB_COUNTERS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_VNET_IP6_FIB_COUNTERS, 0, context, ) + c)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vnet_get_summary_stats_decode(msg):
    n = namedtuple('vnet_get_summary_stats', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def vnet_get_summary_stats(async = False):
    global waiting_for_reply
    context = get_context(VL_API_VNET_GET_SUMMARY_STATS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_VNET_GET_SUMMARY_STATS, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vnet_summary_stats_reply_decode(msg):
    n = namedtuple('vnet_summary_stats_reply', 'vl_msg_id, context, retval, total_pkts, total_bytes, vector_rate')
    if not n:
        return None
    
    tr = unpack('>HIiQQQQd', msg[:50])
    r = n._make((tr[0],tr[1],tr[2],tr[3:5],tr[5:7],tr[7],))
    if not r:
        return None
    return r
    
def vnet_summary_stats_reply(total_pkts, total_bytes, vector_rate, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VNET_SUMMARY_STATS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiQQQQd', VL_API_VNET_SUMMARY_STATS_REPLY, 0, context, total_pkts, total_bytes, vector_rate))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def oam_event_decode(msg):
    n = namedtuple('oam_event', 'vl_msg_id, dst_address, state')
    if not n:
        return None
    
    tr = unpack('>H4sB', msg[:7])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def oam_event(async = False):
    global waiting_for_reply
    context = get_context(VL_API_OAM_EVENT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>H4sB', VL_API_OAM_EVENT, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_oam_events_decode(msg):
    n = namedtuple('want_oam_events', 'vl_msg_id, client_index, context, enable_disable, pid')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def want_oam_events(enable_disable, pid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_OAM_EVENTS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_WANT_OAM_EVENTS, 0, context, enable_disable, pid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_oam_events_reply_decode(msg):
    n = namedtuple('want_oam_events_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def want_oam_events_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_OAM_EVENTS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_WANT_OAM_EVENTS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def oam_add_del_decode(msg):
    n = namedtuple('oam_add_del', 'vl_msg_id, client_index, context, vrf_id, src_address, dst_address, is_add')
    if not n:
        return None
    
    tr = unpack('>HIII4s4sB', msg[:23])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def oam_add_del(vrf_id, src_address, dst_address, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_OAM_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII4s4sB', VL_API_OAM_ADD_DEL, 0, context, vrf_id, src_address, dst_address, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def oam_add_del_reply_decode(msg):
    n = namedtuple('oam_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def oam_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_OAM_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_OAM_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def reset_fib_decode(msg):
    n = namedtuple('reset_fib', 'vl_msg_id, client_index, context, vrf_id, is_ipv6')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def reset_fib(vrf_id, is_ipv6, async = False):
    global waiting_for_reply
    context = get_context(VL_API_RESET_FIB)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_RESET_FIB, 0, context, vrf_id, is_ipv6))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def reset_fib_reply_decode(msg):
    n = namedtuple('reset_fib_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def reset_fib_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_RESET_FIB_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_RESET_FIB_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_config_decode(msg):
    n = namedtuple('dhcp_proxy_config', 'vl_msg_id, client_index, context, vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address')
    if not n:
        return None
    
    tr = unpack('>HIIIBBB16s16s', msg[:49])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def dhcp_proxy_config(vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_CONFIG)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBB16s16s', VL_API_DHCP_PROXY_CONFIG, 0, context, vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_config_reply_decode(msg):
    n = namedtuple('dhcp_proxy_config_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def dhcp_proxy_config_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_CONFIG_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DHCP_PROXY_CONFIG_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_set_vss_decode(msg):
    n = namedtuple('dhcp_proxy_set_vss', 'vl_msg_id, client_index, context, tbl_id, oui, fib_id, is_ipv6, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIIBB', msg[:24])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def dhcp_proxy_set_vss(tbl_id, oui, fib_id, is_ipv6, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_SET_VSS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIBB', VL_API_DHCP_PROXY_SET_VSS, 0, context, tbl_id, oui, fib_id, is_ipv6, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_set_vss_reply_decode(msg):
    n = namedtuple('dhcp_proxy_set_vss_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def dhcp_proxy_set_vss_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_SET_VSS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DHCP_PROXY_SET_VSS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def set_ip_flow_hash_decode(msg):
    n = namedtuple('set_ip_flow_hash', 'vl_msg_id, client_index, context, vrf_id, is_ipv6, src, dst, sport, dport, proto, reverse')
    if not n:
        return None
    
    tr = unpack('>HIIIBBBBBBB', msg[:21])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],))
    if not r:
        return None
    return r
    
def set_ip_flow_hash(vrf_id, is_ipv6, src, dst, sport, dport, proto, reverse, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SET_IP_FLOW_HASH)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBBBBBB', VL_API_SET_IP_FLOW_HASH, 0, context, vrf_id, is_ipv6, src, dst, sport, dport, proto, reverse))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def set_ip_flow_hash_reply_decode(msg):
    n = namedtuple('set_ip_flow_hash_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def set_ip_flow_hash_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SET_IP_FLOW_HASH_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SET_IP_FLOW_HASH_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6nd_ra_config_decode(msg):
    n = namedtuple('sw_interface_ip6nd_ra_config', 'vl_msg_id, client_index, context, sw_if_index, surpress, managed, other, ll_option, send_unicast, cease, is_no, default_router, max_interval, min_interval, lifetime, initial_count, initial_interval')
    if not n:
        return None
    
    tr = unpack('>HIIIBBBBBBBBIIIII', msg[:42])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],tr[15],tr[16],))
    if not r:
        return None
    return r
    
def sw_interface_ip6nd_ra_config(sw_if_index, surpress, managed, other, ll_option, send_unicast, cease, is_no, default_router, max_interval, min_interval, lifetime, initial_count, initial_interval, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6ND_RA_CONFIG)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBBBBBBBIIIII', VL_API_SW_INTERFACE_IP6ND_RA_CONFIG, 0, context, sw_if_index, surpress, managed, other, ll_option, send_unicast, cease, is_no, default_router, max_interval, min_interval, lifetime, initial_count, initial_interval))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6nd_ra_config_reply_decode(msg):
    n = namedtuple('sw_interface_ip6nd_ra_config_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_ip6nd_ra_config_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6ND_RA_CONFIG_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_IP6ND_RA_CONFIG_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6nd_ra_prefix_decode(msg):
    n = namedtuple('sw_interface_ip6nd_ra_prefix', 'vl_msg_id, client_index, context, sw_if_index, address, address_length, use_default, no_advertise, off_link, no_autoconfig, no_onlink, is_no, val_lifetime, pref_lifetime')
    if not n:
        return None
    
    tr = unpack('>HIII16sBBBBBBBII', msg[:45])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],))
    if not r:
        return None
    return r
    
def sw_interface_ip6nd_ra_prefix(sw_if_index, address, address_length, use_default, no_advertise, off_link, no_autoconfig, no_onlink, is_no, val_lifetime, pref_lifetime, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6ND_RA_PREFIX)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII16sBBBBBBBII', VL_API_SW_INTERFACE_IP6ND_RA_PREFIX, 0, context, sw_if_index, address, address_length, use_default, no_advertise, off_link, no_autoconfig, no_onlink, is_no, val_lifetime, pref_lifetime))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6nd_ra_prefix_reply_decode(msg):
    n = namedtuple('sw_interface_ip6nd_ra_prefix_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_ip6nd_ra_prefix_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6ND_RA_PREFIX_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_IP6ND_RA_PREFIX_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6_enable_disable_decode(msg):
    n = namedtuple('sw_interface_ip6_enable_disable', 'vl_msg_id, client_index, context, sw_if_index, enable')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def sw_interface_ip6_enable_disable(sw_if_index, enable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE, 0, context, sw_if_index, enable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6_enable_disable_reply_decode(msg):
    n = namedtuple('sw_interface_ip6_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_ip6_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6_set_link_local_address_decode(msg):
    n = namedtuple('sw_interface_ip6_set_link_local_address', 'vl_msg_id, client_index, context, sw_if_index, address, address_length')
    if not n:
        return None
    
    tr = unpack('>HIII16sB', msg[:31])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def sw_interface_ip6_set_link_local_address(sw_if_index, address, address_length, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII16sB', VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS, 0, context, sw_if_index, address, address_length))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_ip6_set_link_local_address_reply_decode(msg):
    n = namedtuple('sw_interface_ip6_set_link_local_address_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_ip6_set_link_local_address_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_unnumbered_decode(msg):
    n = namedtuple('sw_interface_set_unnumbered', 'vl_msg_id, client_index, context, sw_if_index, unnumbered_sw_if_index, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIB', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def sw_interface_set_unnumbered(sw_if_index, unnumbered_sw_if_index, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_UNNUMBERED)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIB', VL_API_SW_INTERFACE_SET_UNNUMBERED, 0, context, sw_if_index, unnumbered_sw_if_index, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_unnumbered_reply_decode(msg):
    n = namedtuple('sw_interface_set_unnumbered_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_unnumbered_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_UNNUMBERED_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_UNNUMBERED_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_loopback_decode(msg):
    n = namedtuple('create_loopback', 'vl_msg_id, client_index, context, mac_address')
    if not n:
        return None
    
    tr = unpack('>HII6s', msg[:16])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def create_loopback(mac_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_LOOPBACK)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII6s', VL_API_CREATE_LOOPBACK, 0, context, mac_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_loopback_reply_decode(msg):
    n = namedtuple('create_loopback_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def create_loopback_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_LOOPBACK_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_CREATE_LOOPBACK_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def delete_loopback_decode(msg):
    n = namedtuple('delete_loopback', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def delete_loopback(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DELETE_LOOPBACK)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_DELETE_LOOPBACK, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def delete_loopback_reply_decode(msg):
    n = namedtuple('delete_loopback_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def delete_loopback_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DELETE_LOOPBACK_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DELETE_LOOPBACK_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def control_ping_decode(msg):
    n = namedtuple('control_ping', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def control_ping(async = False):
    global waiting_for_reply
    context = get_context(VL_API_CONTROL_PING)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def control_ping_reply_decode(msg):
    n = namedtuple('control_ping_reply', 'vl_msg_id, context, retval, client_index, vpe_pid')
    if not n:
        return None
    
    tr = unpack('>HIiII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def control_ping_reply(client_index, vpe_pid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CONTROL_PING_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiII', VL_API_CONTROL_PING_REPLY, 0, context, client_index, vpe_pid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cli_request_decode(msg):
    n = namedtuple('cli_request', 'vl_msg_id, client_index, context, cmd_in_shmem')
    if not n:
        return None
    
    tr = unpack('>HIIQ', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def cli_request(cmd_in_shmem, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLI_REQUEST)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIQ', VL_API_CLI_REQUEST, 0, context, cmd_in_shmem))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cli_reply_decode(msg):
    n = namedtuple('cli_reply', 'vl_msg_id, context, retval, reply_in_shmem')
    if not n:
        return None
    
    tr = unpack('>HIIQ', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def cli_reply(reply_in_shmem, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLI_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIQ', VL_API_CLI_REPLY, 0, context, reply_in_shmem))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def set_arp_neighbor_limit_decode(msg):
    n = namedtuple('set_arp_neighbor_limit', 'vl_msg_id, client_index, context, is_ipv6, arp_neighbor_limit')
    if not n:
        return None
    
    tr = unpack('>HIIBI', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def set_arp_neighbor_limit(is_ipv6, arp_neighbor_limit, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SET_ARP_NEIGHBOR_LIMIT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBI', VL_API_SET_ARP_NEIGHBOR_LIMIT, 0, context, is_ipv6, arp_neighbor_limit))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def set_arp_neighbor_limit_reply_decode(msg):
    n = namedtuple('set_arp_neighbor_limit_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def set_arp_neighbor_limit_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SET_ARP_NEIGHBOR_LIMIT_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SET_ARP_NEIGHBOR_LIMIT_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_patch_add_del_decode(msg):
    n = namedtuple('l2_patch_add_del', 'vl_msg_id, client_index, context, rx_sw_if_index, tx_sw_if_index, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIB', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def l2_patch_add_del(rx_sw_if_index, tx_sw_if_index, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_PATCH_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIB', VL_API_L2_PATCH_ADD_DEL, 0, context, rx_sw_if_index, tx_sw_if_index, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_patch_add_del_reply_decode(msg):
    n = namedtuple('l2_patch_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2_patch_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_PATCH_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2_PATCH_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_tunnel_add_del_decode(msg):
    n = namedtuple('sr_tunnel_add_del', 'vl_msg_id, client_index, context, is_add, name, src_address, dst_address, dst_mask_width, inner_vrf_id, outer_vrf_id, flags_net_byte_order, n_segments, n_tags, segs_and_tags, policy_name')
    if not n:
        return None
    
    tr = unpack('>HIIB64s16s16sBIIHBB64s', msg[:184])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],msg[120:],tr[14],))
    if not r:
        return None
    return r
    
def sr_tunnel_add_del(is_add, name, src_address, dst_address, dst_mask_width, inner_vrf_id, outer_vrf_id, flags_net_byte_order, n_segments, n_tags, segs_and_tags, policy_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_TUNNEL_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64s16s16sBIIHBB64s', VL_API_SR_TUNNEL_ADD_DEL, 0, context, is_add, name, src_address, dst_address, dst_mask_width, inner_vrf_id, outer_vrf_id, flags_net_byte_order, n_segments, n_tags, segs_and_tags) + policy_name)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_tunnel_add_del_reply_decode(msg):
    n = namedtuple('sr_tunnel_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sr_tunnel_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_TUNNEL_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SR_TUNNEL_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_policy_add_del_decode(msg):
    n = namedtuple('sr_policy_add_del', 'vl_msg_id, client_index, context, is_add, name, tunnel_names')
    if not n:
        return None
    
    tr = unpack('>HIIB64s', msg[:75])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],msg[75:],))
    if not r:
        return None
    return r
    
def sr_policy_add_del(is_add, name, tunnel_names, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_POLICY_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64s', VL_API_SR_POLICY_ADD_DEL, 0, context, is_add, name) + tunnel_names)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_policy_add_del_reply_decode(msg):
    n = namedtuple('sr_policy_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sr_policy_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_POLICY_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SR_POLICY_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_multicast_map_add_del_decode(msg):
    n = namedtuple('sr_multicast_map_add_del', 'vl_msg_id, client_index, context, is_add, multicast_address, policy_name')
    if not n:
        return None
    
    tr = unpack('>HIIB16s64s', msg[:91])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def sr_multicast_map_add_del(is_add, multicast_address, policy_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_MULTICAST_MAP_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB16s64s', VL_API_SR_MULTICAST_MAP_ADD_DEL, 0, context, is_add, multicast_address, policy_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sr_multicast_map_add_del_reply_decode(msg):
    n = namedtuple('sr_multicast_map_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sr_multicast_map_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SR_MULTICAST_MAP_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SR_MULTICAST_MAP_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_vpath_decode(msg):
    n = namedtuple('sw_interface_set_vpath', 'vl_msg_id, client_index, context, sw_if_index, enable')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def sw_interface_set_vpath(sw_if_index, enable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_VPATH)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_SW_INTERFACE_SET_VPATH, 0, context, sw_if_index, enable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_vpath_reply_decode(msg):
    n = namedtuple('sw_interface_set_vpath_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_vpath_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_VPATH_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_VPATH_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_ethernet_add_del_tunnel_decode(msg):
    n = namedtuple('mpls_ethernet_add_del_tunnel', 'vl_msg_id, client_index, context, vrf_id, tx_sw_if_index, is_add, l2_only, dst_mac_address, adj_address, adj_address_length')
    if not n:
        return None
    
    tr = unpack('>HIIIIBB6s4sB', msg[:31])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def mpls_ethernet_add_del_tunnel(vrf_id, tx_sw_if_index, is_add, l2_only, dst_mac_address, adj_address, adj_address_length, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBB6s4sB', VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL, 0, context, vrf_id, tx_sw_if_index, is_add, l2_only, dst_mac_address, adj_address, adj_address_length))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_ethernet_add_del_tunnel_reply_decode(msg):
    n = namedtuple('mpls_ethernet_add_del_tunnel_reply', 'vl_msg_id, context, retval, tunnel_sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def mpls_ethernet_add_del_tunnel_reply(tunnel_sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_REPLY, 0, context, tunnel_sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_ethernet_add_del_tunnel_2_decode(msg):
    n = namedtuple('mpls_ethernet_add_del_tunnel_2', 'vl_msg_id, client_index, context, inner_vrf_id, outer_vrf_id, resolve_attempts, resolve_opaque, resolve_if_needed, is_add, l2_only, adj_address, adj_address_length, next_hop_ip4_address_in_outer_vrf')
    if not n:
        return None
    
    tr = unpack('>HIIIIIIBBB4sB4s', msg[:38])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],))
    if not r:
        return None
    return r
    
def mpls_ethernet_add_del_tunnel_2(inner_vrf_id, outer_vrf_id, resolve_attempts, resolve_opaque, resolve_if_needed, is_add, l2_only, adj_address, adj_address_length, next_hop_ip4_address_in_outer_vrf, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIIBBB4sB4s', VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2, 0, context, inner_vrf_id, outer_vrf_id, resolve_attempts, resolve_opaque, resolve_if_needed, is_add, l2_only, adj_address, adj_address_length, next_hop_ip4_address_in_outer_vrf))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def mpls_ethernet_add_del_tunnel_2_reply_decode(msg):
    n = namedtuple('mpls_ethernet_add_del_tunnel_2_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def mpls_ethernet_add_del_tunnel_2_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_l2_xconnect_decode(msg):
    n = namedtuple('sw_interface_set_l2_xconnect', 'vl_msg_id, client_index, context, rx_sw_if_index, tx_sw_if_index, enable')
    if not n:
        return None
    
    tr = unpack('>HIIIIB', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def sw_interface_set_l2_xconnect(rx_sw_if_index, tx_sw_if_index, enable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_L2_XCONNECT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIB', VL_API_SW_INTERFACE_SET_L2_XCONNECT, 0, context, rx_sw_if_index, tx_sw_if_index, enable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_l2_xconnect_reply_decode(msg):
    n = namedtuple('sw_interface_set_l2_xconnect_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_l2_xconnect_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_L2_XCONNECT_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_L2_XCONNECT_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_l2_bridge_decode(msg):
    n = namedtuple('sw_interface_set_l2_bridge', 'vl_msg_id, client_index, context, rx_sw_if_index, bd_id, shg, bvi, enable')
    if not n:
        return None
    
    tr = unpack('>HIIIIBBB', msg[:21])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def sw_interface_set_l2_bridge(rx_sw_if_index, bd_id, shg, bvi, enable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_L2_BRIDGE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBBB', VL_API_SW_INTERFACE_SET_L2_BRIDGE, 0, context, rx_sw_if_index, bd_id, shg, bvi, enable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_set_l2_bridge_reply_decode(msg):
    n = namedtuple('sw_interface_set_l2_bridge_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_set_l2_bridge_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_SET_L2_BRIDGE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_SET_L2_BRIDGE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2fib_add_del_decode(msg):
    n = namedtuple('l2fib_add_del', 'vl_msg_id, client_index, context, mac, bd_id, sw_if_index, is_add, static_mac, filter_mac')
    if not n:
        return None
    
    tr = unpack('>HIIQIIBBB', msg[:29])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def l2fib_add_del(mac, bd_id, sw_if_index, is_add, static_mac, filter_mac, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2FIB_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIQIIBBB', VL_API_L2FIB_ADD_DEL, 0, context, mac, bd_id, sw_if_index, is_add, static_mac, filter_mac))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2fib_add_del_reply_decode(msg):
    n = namedtuple('l2fib_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2fib_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2FIB_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2FIB_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_flags_decode(msg):
    n = namedtuple('l2_flags', 'vl_msg_id, client_index, context, sw_if_index, is_set, feature_bitmap')
    if not n:
        return None
    
    tr = unpack('>HIIIBI', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def l2_flags(sw_if_index, is_set, feature_bitmap, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FLAGS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBI', VL_API_L2_FLAGS, 0, context, sw_if_index, is_set, feature_bitmap))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_flags_reply_decode(msg):
    n = namedtuple('l2_flags_reply', 'vl_msg_id, context, retval, resulting_feature_bitmap')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def l2_flags_reply(resulting_feature_bitmap, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FLAGS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_L2_FLAGS_REPLY, 0, context, resulting_feature_bitmap))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_flags_decode(msg):
    n = namedtuple('bridge_flags', 'vl_msg_id, client_index, context, bd_id, is_set, feature_bitmap')
    if not n:
        return None
    
    tr = unpack('>HIIIBI', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def bridge_flags(bd_id, is_set, feature_bitmap, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_FLAGS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBI', VL_API_BRIDGE_FLAGS, 0, context, bd_id, is_set, feature_bitmap))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_flags_reply_decode(msg):
    n = namedtuple('bridge_flags_reply', 'vl_msg_id, context, retval, resulting_feature_bitmap')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def bridge_flags_reply(resulting_feature_bitmap, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_FLAGS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_BRIDGE_FLAGS_REPLY, 0, context, resulting_feature_bitmap))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bd_ip_mac_add_del_decode(msg):
    n = namedtuple('bd_ip_mac_add_del', 'vl_msg_id, client_index, context, bd_id, is_add, is_ipv6, ip_address, mac_address')
    if not n:
        return None
    
    tr = unpack('>HIIIBB16s6s', msg[:38])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def bd_ip_mac_add_del(bd_id, is_add, is_ipv6, ip_address, mac_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BD_IP_MAC_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBB16s6s', VL_API_BD_IP_MAC_ADD_DEL, 0, context, bd_id, is_add, is_ipv6, ip_address, mac_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bd_ip_mac_add_del_reply_decode(msg):
    n = namedtuple('bd_ip_mac_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def bd_ip_mac_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_BD_IP_MAC_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_BD_IP_MAC_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_add_del_table_decode(msg):
    n = namedtuple('classify_add_del_table', 'vl_msg_id, client_index, context, is_add, table_index, nbuckets, memory_size, skip_n_vectors, match_n_vectors, next_table_index, miss_next_index, mask')
    if not n:
        return None
    
    tr = unpack('>HIIBIIIIIII', msg[:39])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],msg[39:],))
    if not r:
        return None
    return r
    
def classify_add_del_table(is_add, table_index, nbuckets, memory_size, skip_n_vectors, match_n_vectors, next_table_index, miss_next_index, mask, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_ADD_DEL_TABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIIIIIII', VL_API_CLASSIFY_ADD_DEL_TABLE, 0, context, is_add, table_index, nbuckets, memory_size, skip_n_vectors, match_n_vectors, next_table_index, miss_next_index) + mask)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_add_del_table_reply_decode(msg):
    n = namedtuple('classify_add_del_table_reply', 'vl_msg_id, context, retval, new_table_index, skip_n_vectors, match_n_vectors')
    if not n:
        return None
    
    tr = unpack('>HIiIII', msg[:22])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def classify_add_del_table_reply(new_table_index, skip_n_vectors, match_n_vectors, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_ADD_DEL_TABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiIII', VL_API_CLASSIFY_ADD_DEL_TABLE_REPLY, 0, context, new_table_index, skip_n_vectors, match_n_vectors))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_add_del_session_decode(msg):
    n = namedtuple('classify_add_del_session', 'vl_msg_id, client_index, context, is_add, table_index, hit_next_index, opaque_index, advance, match')
    if not n:
        return None
    
    tr = unpack('>HIIBIIIi', msg[:27])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],msg[27:],))
    if not r:
        return None
    return r
    
def classify_add_del_session(is_add, table_index, hit_next_index, opaque_index, advance, match, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_ADD_DEL_SESSION)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIIIi', VL_API_CLASSIFY_ADD_DEL_SESSION, 0, context, is_add, table_index, hit_next_index, opaque_index, advance) + match)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_add_del_session_reply_decode(msg):
    n = namedtuple('classify_add_del_session_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def classify_add_del_session_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_ADD_DEL_SESSION_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_CLASSIFY_ADD_DEL_SESSION_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_set_interface_ip_table_decode(msg):
    n = namedtuple('classify_set_interface_ip_table', 'vl_msg_id, client_index, context, is_ipv6, sw_if_index, table_index')
    if not n:
        return None
    
    tr = unpack('>HIIBII', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def classify_set_interface_ip_table(is_ipv6, sw_if_index, table_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBII', VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE, 0, context, is_ipv6, sw_if_index, table_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_set_interface_ip_table_reply_decode(msg):
    n = namedtuple('classify_set_interface_ip_table_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def classify_set_interface_ip_table_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_set_interface_l2_tables_decode(msg):
    n = namedtuple('classify_set_interface_l2_tables', 'vl_msg_id, client_index, context, sw_if_index, ip4_table_index, ip6_table_index, other_table_index')
    if not n:
        return None
    
    tr = unpack('>HIIIIII', msg[:26])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def classify_set_interface_l2_tables(sw_if_index, ip4_table_index, ip6_table_index, other_table_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIII', VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES, 0, context, sw_if_index, ip4_table_index, ip6_table_index, other_table_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def classify_set_interface_l2_tables_reply_decode(msg):
    n = namedtuple('classify_set_interface_l2_tables_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def classify_set_interface_l2_tables_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def get_node_index_decode(msg):
    n = namedtuple('get_node_index', 'vl_msg_id, client_index, context, node_name')
    if not n:
        return None
    
    tr = unpack('>HII64s', msg[:74])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def get_node_index(node_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GET_NODE_INDEX)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s', VL_API_GET_NODE_INDEX, 0, context, node_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def get_node_index_reply_decode(msg):
    n = namedtuple('get_node_index_reply', 'vl_msg_id, context, retval, node_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def get_node_index_reply(node_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GET_NODE_INDEX_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_GET_NODE_INDEX_REPLY, 0, context, node_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def add_node_next_decode(msg):
    n = namedtuple('add_node_next', 'vl_msg_id, client_index, context, node_name, next_name')
    if not n:
        return None
    
    tr = unpack('>HII64s64s', msg[:138])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def add_node_next(node_name, next_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_ADD_NODE_NEXT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s64s', VL_API_ADD_NODE_NEXT, 0, context, node_name, next_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def add_node_next_reply_decode(msg):
    n = namedtuple('add_node_next_reply', 'vl_msg_id, context, retval, next_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def add_node_next_reply(next_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_ADD_NODE_NEXT_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_ADD_NODE_NEXT_REPLY, 0, context, next_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_config_2_decode(msg):
    n = namedtuple('dhcp_proxy_config_2', 'vl_msg_id, client_index, context, rx_vrf_id, server_vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address')
    if not n:
        return None
    
    tr = unpack('>HIIIIBBB16s16s', msg[:53])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def dhcp_proxy_config_2(rx_vrf_id, server_vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_CONFIG_2)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBBB16s16s', VL_API_DHCP_PROXY_CONFIG_2, 0, context, rx_vrf_id, server_vrf_id, is_ipv6, is_add, insert_circuit_id, dhcp_server, dhcp_src_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_proxy_config_2_reply_decode(msg):
    n = namedtuple('dhcp_proxy_config_2_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def dhcp_proxy_config_2_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_PROXY_CONFIG_2_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DHCP_PROXY_CONFIG_2_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_create_tunnel_decode(msg):
    n = namedtuple('l2tpv3_create_tunnel', 'vl_msg_id, client_index, context, client_address, our_address, is_ipv6, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present')
    if not n:
        return None
    
    tr = unpack('>HII16s16sBIIQQB', msg[:68])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],))
    if not r:
        return None
    return r
    
def l2tpv3_create_tunnel(client_address, our_address, is_ipv6, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_CREATE_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII16s16sBIIQQB', VL_API_L2TPV3_CREATE_TUNNEL, 0, context, client_address, our_address, is_ipv6, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_create_tunnel_reply_decode(msg):
    n = namedtuple('l2tpv3_create_tunnel_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def l2tpv3_create_tunnel_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_CREATE_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_L2TPV3_CREATE_TUNNEL_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_set_tunnel_cookies_decode(msg):
    n = namedtuple('l2tpv3_set_tunnel_cookies', 'vl_msg_id, client_index, context, sw_if_index, new_local_cookie, new_remote_cookie')
    if not n:
        return None
    
    tr = unpack('>HIIIQQ', msg[:30])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def l2tpv3_set_tunnel_cookies(sw_if_index, new_local_cookie, new_remote_cookie, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_SET_TUNNEL_COOKIES)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIQQ', VL_API_L2TPV3_SET_TUNNEL_COOKIES, 0, context, sw_if_index, new_local_cookie, new_remote_cookie))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_set_tunnel_cookies_reply_decode(msg):
    n = namedtuple('l2tpv3_set_tunnel_cookies_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2tpv3_set_tunnel_cookies_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_SET_TUNNEL_COOKIES_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2TPV3_SET_TUNNEL_COOKIES_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_if_l2tpv3_tunnel_details_decode(msg):
    n = namedtuple('sw_if_l2tpv3_tunnel_details', 'vl_msg_id, context, sw_if_index, interface_name, client_address, our_address, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present')
    if not n:
        return None
    
    tr = unpack('>HII64s16s16sIIQQQB', msg[:139])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8:10],tr[10],tr[11],))
    if not r:
        return None
    return r
    
def sw_if_l2tpv3_tunnel_details(interface_name, client_address, our_address, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_IF_L2TPV3_TUNNEL_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s16s16sIIQQQB', VL_API_SW_IF_L2TPV3_TUNNEL_DETAILS, 0, context, interface_name, client_address, our_address, local_session_id, remote_session_id, local_cookie, remote_cookie, l2_sublayer_present))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_if_l2tpv3_tunnel_dump_decode(msg):
    n = namedtuple('sw_if_l2tpv3_tunnel_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_if_l2tpv3_tunnel_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_IF_L2TPV3_TUNNEL_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_SW_IF_L2TPV3_TUNNEL_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_fib_clear_table_decode(msg):
    n = namedtuple('l2_fib_clear_table', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2_fib_clear_table(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FIB_CLEAR_TABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_L2_FIB_CLEAR_TABLE, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_fib_clear_table_reply_decode(msg):
    n = namedtuple('l2_fib_clear_table_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2_fib_clear_table_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FIB_CLEAR_TABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2_FIB_CLEAR_TABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_interface_efp_filter_decode(msg):
    n = namedtuple('l2_interface_efp_filter', 'vl_msg_id, client_index, context, sw_if_index, enable_disable')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def l2_interface_efp_filter(sw_if_index, enable_disable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_INTERFACE_EFP_FILTER)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_L2_INTERFACE_EFP_FILTER, 0, context, sw_if_index, enable_disable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_interface_efp_filter_reply_decode(msg):
    n = namedtuple('l2_interface_efp_filter_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2_interface_efp_filter_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_INTERFACE_EFP_FILTER_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2_INTERFACE_EFP_FILTER_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_interface_enable_disable_decode(msg):
    n = namedtuple('l2tpv3_interface_enable_disable', 'vl_msg_id, client_index, context, enable_disable, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIIBI', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def l2tpv3_interface_enable_disable(enable_disable, sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBI', VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE, 0, context, enable_disable, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_interface_enable_disable_reply_decode(msg):
    n = namedtuple('l2tpv3_interface_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2tpv3_interface_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_set_lookup_key_decode(msg):
    n = namedtuple('l2tpv3_set_lookup_key', 'vl_msg_id, client_index, context, key')
    if not n:
        return None
    
    tr = unpack('>HIIB', msg[:11])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def l2tpv3_set_lookup_key(key, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_SET_LOOKUP_KEY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB', VL_API_L2TPV3_SET_LOOKUP_KEY, 0, context, key))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2tpv3_set_lookup_key_reply_decode(msg):
    n = namedtuple('l2tpv3_set_lookup_key_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2tpv3_set_lookup_key_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2TPV3_SET_LOOKUP_KEY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2TPV3_SET_LOOKUP_KEY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_add_del_tunnel_decode(msg):
    n = namedtuple('vxlan_add_del_tunnel', 'vl_msg_id, client_index, context, is_add, is_ipv6, src_address, dst_address, encap_vrf_id, decap_next_index, vni')
    if not n:
        return None
    
    tr = unpack('>HIIBB16s16sIII', msg[:56])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def vxlan_add_del_tunnel(is_add, is_ipv6, src_address, dst_address, encap_vrf_id, decap_next_index, vni, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_ADD_DEL_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBB16s16sIII', VL_API_VXLAN_ADD_DEL_TUNNEL, 0, context, is_add, is_ipv6, src_address, dst_address, encap_vrf_id, decap_next_index, vni))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_add_del_tunnel_reply_decode(msg):
    n = namedtuple('vxlan_add_del_tunnel_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def vxlan_add_del_tunnel_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_ADD_DEL_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_VXLAN_ADD_DEL_TUNNEL_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_tunnel_dump_decode(msg):
    n = namedtuple('vxlan_tunnel_dump', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def vxlan_tunnel_dump(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_TUNNEL_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIII', VL_API_VXLAN_TUNNEL_DUMP, 0, context, sw_if_index))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_tunnel_details_decode(msg):
    n = namedtuple('vxlan_tunnel_details', 'vl_msg_id, context, sw_if_index, src_address, dst_address, encap_vrf_id, decap_next_index, vni, is_ipv6')
    if not n:
        return None
    
    tr = unpack('>HII16s16sIIIB', msg[:55])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def vxlan_tunnel_details(src_address, dst_address, encap_vrf_id, decap_next_index, vni, is_ipv6, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_TUNNEL_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII16s16sIIIB', VL_API_VXLAN_TUNNEL_DETAILS, 0, context, src_address, dst_address, encap_vrf_id, decap_next_index, vni, is_ipv6))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def gre_add_del_tunnel_decode(msg):
    n = namedtuple('gre_add_del_tunnel', 'vl_msg_id, client_index, context, is_add, src_address, dst_address, outer_table_id')
    if not n:
        return None
    
    tr = unpack('>HIIBIII', msg[:23])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def gre_add_del_tunnel(is_add, src_address, dst_address, outer_table_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GRE_ADD_DEL_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIII', VL_API_GRE_ADD_DEL_TUNNEL, 0, context, is_add, src_address, dst_address, outer_table_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def gre_add_del_tunnel_reply_decode(msg):
    n = namedtuple('gre_add_del_tunnel_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def gre_add_del_tunnel_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GRE_ADD_DEL_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_GRE_ADD_DEL_TUNNEL_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def gre_tunnel_dump_decode(msg):
    n = namedtuple('gre_tunnel_dump', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def gre_tunnel_dump(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GRE_TUNNEL_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIII', VL_API_GRE_TUNNEL_DUMP, 0, context, sw_if_index))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def gre_tunnel_details_decode(msg):
    n = namedtuple('gre_tunnel_details', 'vl_msg_id, context, sw_if_index, src_address, dst_address, outer_table_id')
    if not n:
        return None
    
    tr = unpack('>HIIIII', msg[:22])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def gre_tunnel_details(src_address, dst_address, outer_table_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GRE_TUNNEL_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIII', VL_API_GRE_TUNNEL_DETAILS, 0, context, src_address, dst_address, outer_table_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_interface_vlan_tag_rewrite_decode(msg):
    n = namedtuple('l2_interface_vlan_tag_rewrite', 'vl_msg_id, client_index, context, sw_if_index, vtr_op, push_dot1q, tag1, tag2')
    if not n:
        return None
    
    tr = unpack('>HIIIIIII', msg[:30])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def l2_interface_vlan_tag_rewrite(sw_if_index, vtr_op, push_dot1q, tag1, tag2, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_INTERFACE_VLAN_TAG_REWRITE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIII', VL_API_L2_INTERFACE_VLAN_TAG_REWRITE, 0, context, sw_if_index, vtr_op, push_dot1q, tag1, tag2))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_interface_vlan_tag_rewrite_reply_decode(msg):
    n = namedtuple('l2_interface_vlan_tag_rewrite_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def l2_interface_vlan_tag_rewrite_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_INTERFACE_VLAN_TAG_REWRITE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_L2_INTERFACE_VLAN_TAG_REWRITE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_vhost_user_if_decode(msg):
    n = namedtuple('create_vhost_user_if', 'vl_msg_id, client_index, context, is_server, sock_filename, renumber, custom_dev_instance, use_custom_mac, mac_address')
    if not n:
        return None
    
    tr = unpack('>HIIB256sBIB6s', msg[:279])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def create_vhost_user_if(is_server, sock_filename, renumber, custom_dev_instance, use_custom_mac, mac_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_VHOST_USER_IF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB256sBIB6s', VL_API_CREATE_VHOST_USER_IF, 0, context, is_server, sock_filename, renumber, custom_dev_instance, use_custom_mac, mac_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_vhost_user_if_reply_decode(msg):
    n = namedtuple('create_vhost_user_if_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def create_vhost_user_if_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_VHOST_USER_IF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_CREATE_VHOST_USER_IF_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def modify_vhost_user_if_decode(msg):
    n = namedtuple('modify_vhost_user_if', 'vl_msg_id, client_index, context, sw_if_index, is_server, sock_filename, renumber, custom_dev_instance')
    if not n:
        return None
    
    tr = unpack('>HIIIB256sBI', msg[:276])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def modify_vhost_user_if(sw_if_index, is_server, sock_filename, renumber, custom_dev_instance, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MODIFY_VHOST_USER_IF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB256sBI', VL_API_MODIFY_VHOST_USER_IF, 0, context, sw_if_index, is_server, sock_filename, renumber, custom_dev_instance))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def modify_vhost_user_if_reply_decode(msg):
    n = namedtuple('modify_vhost_user_if_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def modify_vhost_user_if_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MODIFY_VHOST_USER_IF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MODIFY_VHOST_USER_IF_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def delete_vhost_user_if_decode(msg):
    n = namedtuple('delete_vhost_user_if', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def delete_vhost_user_if(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DELETE_VHOST_USER_IF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_DELETE_VHOST_USER_IF, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def delete_vhost_user_if_reply_decode(msg):
    n = namedtuple('delete_vhost_user_if_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def delete_vhost_user_if_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DELETE_VHOST_USER_IF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DELETE_VHOST_USER_IF_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_subif_decode(msg):
    n = namedtuple('create_subif', 'vl_msg_id, client_index, context, sw_if_index, sub_id, no_tags, one_tag, two_tags, dot1ad, exact_match, default_sub, outer_vlan_id_any, inner_vlan_id_any, outer_vlan_id, inner_vlan_id')
    if not n:
        return None
    
    tr = unpack('>HIIIIBBBBBBBBHH', msg[:30])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],))
    if not r:
        return None
    return r
    
def create_subif(sw_if_index, sub_id, no_tags, one_tag, two_tags, dot1ad, exact_match, default_sub, outer_vlan_id_any, inner_vlan_id_any, outer_vlan_id, inner_vlan_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_SUBIF)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBBBBBBBBHH', VL_API_CREATE_SUBIF, 0, context, sw_if_index, sub_id, no_tags, one_tag, two_tags, dot1ad, exact_match, default_sub, outer_vlan_id_any, inner_vlan_id_any, outer_vlan_id, inner_vlan_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def create_subif_reply_decode(msg):
    n = namedtuple('create_subif_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def create_subif_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_CREATE_SUBIF_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_CREATE_SUBIF_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def show_version_decode(msg):
    n = namedtuple('show_version', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def show_version(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SHOW_VERSION)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_SHOW_VERSION, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def show_version_reply_decode(msg):
    n = namedtuple('show_version_reply', 'vl_msg_id, context, retval, program, version, build_date, build_directory')
    if not n:
        return None
    
    tr = unpack('>HIi32s32s32s256s', msg[:362])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def show_version_reply(program, version, build_date, build_directory, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SHOW_VERSION_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi32s32s32s256s', VL_API_SHOW_VERSION_REPLY, 0, context, program, version, build_date, build_directory))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_vhost_user_details_decode(msg):
    n = namedtuple('sw_interface_vhost_user_details', 'vl_msg_id, context, sw_if_index, interface_name, virtio_net_hdr_sz, features, is_server, sock_filename, num_regions, sock_errno')
    if not n:
        return None
    
    tr = unpack('>HII64sIQB256sIi', msg[:351])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def sw_interface_vhost_user_details(interface_name, virtio_net_hdr_sz, features, is_server, sock_filename, num_regions, sock_errno, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_VHOST_USER_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sIQB256sIi', VL_API_SW_INTERFACE_VHOST_USER_DETAILS, 0, context, interface_name, virtio_net_hdr_sz, features, is_server, sock_filename, num_regions, sock_errno))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_vhost_user_dump_decode(msg):
    n = namedtuple('sw_interface_vhost_user_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_vhost_user_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_VHOST_USER_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_SW_INTERFACE_VHOST_USER_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_address_details_decode(msg):
    n = namedtuple('ip_address_details', 'vl_msg_id, client_index, context, ip, prefix_length')
    if not n:
        return None
    
    tr = unpack('>HII16sB', msg[:27])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def ip_address_details(ip, prefix_length, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_ADDRESS_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII16sB', VL_API_IP_ADDRESS_DETAILS, 0, context, ip, prefix_length))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_address_dump_decode(msg):
    n = namedtuple('ip_address_dump', 'vl_msg_id, client_index, context, sw_if_index, is_ipv6')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def ip_address_dump(sw_if_index, is_ipv6, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_ADDRESS_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIIIB', VL_API_IP_ADDRESS_DUMP, 0, context, sw_if_index, is_ipv6))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_details_decode(msg):
    n = namedtuple('ip_details', 'vl_msg_id, sw_if_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ip_details(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_IP_DETAILS, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip_dump_decode(msg):
    n = namedtuple('ip_dump', 'vl_msg_id, client_index, context, is_ipv6')
    if not n:
        return None
    
    tr = unpack('>HIIB', msg[:11])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def ip_dump(is_ipv6, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIIB', VL_API_IP_DUMP, 0, context, is_ipv6))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_fib_table_entry_decode(msg):
    n = namedtuple('l2_fib_table_entry', 'vl_msg_id, context, bd_id, mac, sw_if_index, static_mac, filter_mac, bvi_mac')
    if not n:
        return None
    
    tr = unpack('>HIIQIBBB', msg[:25])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def l2_fib_table_entry(mac, sw_if_index, static_mac, filter_mac, bvi_mac, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FIB_TABLE_ENTRY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIQIBBB', VL_API_L2_FIB_TABLE_ENTRY, 0, context, mac, sw_if_index, static_mac, filter_mac, bvi_mac))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def l2_fib_table_dump_decode(msg):
    n = namedtuple('l2_fib_table_dump', 'vl_msg_id, client_index, context, bd_id')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def l2_fib_table_dump(bd_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_L2_FIB_TABLE_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIII', VL_API_L2_FIB_TABLE_DUMP, 0, context, bd_id))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_gpe_add_del_tunnel_decode(msg):
    n = namedtuple('vxlan_gpe_add_del_tunnel', 'vl_msg_id, client_index, context, local, remote, encap_vrf_id, decap_vrf_id, protocol, vni, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIIIBIB', msg[:32])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def vxlan_gpe_add_del_tunnel(local, remote, encap_vrf_id, decap_vrf_id, protocol, vni, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_GPE_ADD_DEL_TUNNEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIIBIB', VL_API_VXLAN_GPE_ADD_DEL_TUNNEL, 0, context, local, remote, encap_vrf_id, decap_vrf_id, protocol, vni, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def vxlan_gpe_add_del_tunnel_reply_decode(msg):
    n = namedtuple('vxlan_gpe_add_del_tunnel_reply', 'vl_msg_id, context, retval, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIiI', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def vxlan_gpe_add_del_tunnel_reply(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_VXLAN_GPE_ADD_DEL_TUNNEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiI', VL_API_VXLAN_GPE_ADD_DEL_TUNNEL_REPLY, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_locator_set_decode(msg):
    n = namedtuple('lisp_add_del_locator_set', 'vl_msg_id, client_index, context, is_add, locator_set_name')
    if not n:
        return None
    
    tr = unpack('>HIIB64s', msg[:75])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def lisp_add_del_locator_set(is_add, locator_set_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCATOR_SET)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64s', VL_API_LISP_ADD_DEL_LOCATOR_SET, 0, context, is_add, locator_set_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_locator_set_reply_decode(msg):
    n = namedtuple('lisp_add_del_locator_set_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_add_del_locator_set_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCATOR_SET_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ADD_DEL_LOCATOR_SET_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_locator_decode(msg):
    n = namedtuple('lisp_add_del_locator', 'vl_msg_id, client_index, context, is_add, locator_set_name, sw_if_index, priority, weight')
    if not n:
        return None
    
    tr = unpack('>HIIB64sIBB', msg[:81])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def lisp_add_del_locator(is_add, locator_set_name, sw_if_index, priority, weight, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCATOR)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64sIBB', VL_API_LISP_ADD_DEL_LOCATOR, 0, context, is_add, locator_set_name, sw_if_index, priority, weight))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_locator_reply_decode(msg):
    n = namedtuple('lisp_add_del_locator_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_add_del_locator_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCATOR_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ADD_DEL_LOCATOR_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_local_eid_decode(msg):
    n = namedtuple('lisp_add_del_local_eid', 'vl_msg_id, client_index, context, is_add, is_ipv6, ip_address, prefix_len, locator_set_name')
    if not n:
        return None
    
    tr = unpack('>HIIBB16sB64s', msg[:93])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def lisp_add_del_local_eid(is_add, is_ipv6, ip_address, prefix_len, locator_set_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCAL_EID)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBB16sB64s', VL_API_LISP_ADD_DEL_LOCAL_EID, 0, context, is_add, is_ipv6, ip_address, prefix_len, locator_set_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_local_eid_reply_decode(msg):
    n = namedtuple('lisp_add_del_local_eid_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_add_del_local_eid_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_LOCAL_EID_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ADD_DEL_LOCAL_EID_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_add_del_fwd_entry_decode(msg):
    n = namedtuple('lisp_gpe_add_del_fwd_entry', 'vl_msg_id, client_index, context, is_add, eid_is_ipv6, eid_ip_address, eid_prefix_len, address_is_ipv6, source_ip_address, destination_ip_address')
    if not n:
        return None
    
    tr = unpack('>HIIBB16sBB16s16s', msg[:62])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def lisp_gpe_add_del_fwd_entry(is_add, eid_is_ipv6, eid_ip_address, eid_prefix_len, address_is_ipv6, source_ip_address, destination_ip_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBB16sBB16s16s', VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY, 0, context, is_add, eid_is_ipv6, eid_ip_address, eid_prefix_len, address_is_ipv6, source_ip_address, destination_ip_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_add_del_fwd_entry_reply_decode(msg):
    n = namedtuple('lisp_gpe_add_del_fwd_entry_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_gpe_add_del_fwd_entry_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_map_resolver_decode(msg):
    n = namedtuple('lisp_add_del_map_resolver', 'vl_msg_id, client_index, context, is_add, is_ipv6, ip_address')
    if not n:
        return None
    
    tr = unpack('>HIIBB16s', msg[:28])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def lisp_add_del_map_resolver(is_add, is_ipv6, ip_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_MAP_RESOLVER)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBB16s', VL_API_LISP_ADD_DEL_MAP_RESOLVER, 0, context, is_add, is_ipv6, ip_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_map_resolver_reply_decode(msg):
    n = namedtuple('lisp_add_del_map_resolver_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_add_del_map_resolver_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_MAP_RESOLVER_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ADD_DEL_MAP_RESOLVER_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_enable_disable_decode(msg):
    n = namedtuple('lisp_gpe_enable_disable', 'vl_msg_id, client_index, context, is_en')
    if not n:
        return None
    
    tr = unpack('>HIIB', msg[:11])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def lisp_gpe_enable_disable(is_en, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB', VL_API_LISP_GPE_ENABLE_DISABLE, 0, context, is_en))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_enable_disable_reply_decode(msg):
    n = namedtuple('lisp_gpe_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_gpe_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_GPE_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_enable_disable_decode(msg):
    n = namedtuple('lisp_enable_disable', 'vl_msg_id, client_index, context, is_en')
    if not n:
        return None
    
    tr = unpack('>HIIB', msg[:11])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def lisp_enable_disable(is_en, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB', VL_API_LISP_ENABLE_DISABLE, 0, context, is_en))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_enable_disable_reply_decode(msg):
    n = namedtuple('lisp_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_add_del_iface_decode(msg):
    n = namedtuple('lisp_gpe_add_del_iface', 'vl_msg_id, client_index, context, is_add, table_id, vni')
    if not n:
        return None
    
    tr = unpack('>HIIBII', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def lisp_gpe_add_del_iface(is_add, table_id, vni, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ADD_DEL_IFACE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBII', VL_API_LISP_GPE_ADD_DEL_IFACE, 0, context, is_add, table_id, vni))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_add_del_iface_reply_decode(msg):
    n = namedtuple('lisp_gpe_add_del_iface_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_gpe_add_del_iface_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_ADD_DEL_IFACE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_GPE_ADD_DEL_IFACE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_remote_mapping_decode(msg):
    n = namedtuple('lisp_add_del_remote_mapping', 'vl_msg_id, client_index, context, is_add, vni, action, eid_is_ip4, deid, seid, deid_len, seid_len, rloc_num, rlocs')
    if not n:
        return None
    
    tr = unpack('>HIIBIBB16s16sBBI', msg[:55])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],msg[55:],))
    if not r:
        return None
    return r
    
def lisp_add_del_remote_mapping(is_add, vni, action, eid_is_ip4, deid, seid, deid_len, seid_len, rloc_num, rlocs, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_REMOTE_MAPPING)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIBB16s16sBBI', VL_API_LISP_ADD_DEL_REMOTE_MAPPING, 0, context, is_add, vni, action, eid_is_ip4, deid, seid, deid_len, seid_len, rloc_num) + rlocs)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_add_del_remote_mapping_reply_decode(msg):
    n = namedtuple('lisp_add_del_remote_mapping_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_add_del_remote_mapping_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ADD_DEL_REMOTE_MAPPING_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_LISP_ADD_DEL_REMOTE_MAPPING_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_locator_set_details_decode(msg):
    n = namedtuple('lisp_locator_set_details', 'vl_msg_id, context, local, locator_set_name, sw_if_index, is_ipv6, ip_address, prefix_len, priority, weight')
    if not n:
        return None
    
    tr = unpack('>HIB64sIB16sBBB', msg[:95])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def lisp_locator_set_details(locator_set_name, sw_if_index, is_ipv6, ip_address, prefix_len, priority, weight, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_LOCATOR_SET_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIB64sIB16sBBB', VL_API_LISP_LOCATOR_SET_DETAILS, 0, context, locator_set_name, sw_if_index, is_ipv6, ip_address, prefix_len, priority, weight))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_locator_set_dump_decode(msg):
    n = namedtuple('lisp_locator_set_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_locator_set_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_LOCATOR_SET_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_LISP_LOCATOR_SET_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_local_eid_table_details_decode(msg):
    n = namedtuple('lisp_local_eid_table_details', 'vl_msg_id, context, locator_set_name, eid_is_ipv6, eid_ip_address, eid_prefix_len')
    if not n:
        return None
    
    tr = unpack('>HI64sB16sB', msg[:88])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def lisp_local_eid_table_details(eid_is_ipv6, eid_ip_address, eid_prefix_len, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_LOCAL_EID_TABLE_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HI64sB16sB', VL_API_LISP_LOCAL_EID_TABLE_DETAILS, 0, context, eid_is_ipv6, eid_ip_address, eid_prefix_len))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_local_eid_table_dump_decode(msg):
    n = namedtuple('lisp_local_eid_table_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_local_eid_table_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_LOCAL_EID_TABLE_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_LISP_LOCAL_EID_TABLE_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_tunnel_details_decode(msg):
    n = namedtuple('lisp_gpe_tunnel_details', 'vl_msg_id, context, tunnels, is_ipv6, source_ip, destination_ip, encap_fib_id, decap_fib_id, dcap_next, lisp_ver, next_protocol, flags, ver_res, res, iid')
    if not n:
        return None
    
    tr = unpack('>HIIB16s16sIIIBBBBBI', msg[:64])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],))
    if not r:
        return None
    return r
    
def lisp_gpe_tunnel_details(is_ipv6, source_ip, destination_ip, encap_fib_id, decap_fib_id, dcap_next, lisp_ver, next_protocol, flags, ver_res, res, iid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_TUNNEL_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB16s16sIIIBBBBBI', VL_API_LISP_GPE_TUNNEL_DETAILS, 0, context, is_ipv6, source_ip, destination_ip, encap_fib_id, decap_fib_id, dcap_next, lisp_ver, next_protocol, flags, ver_res, res, iid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_gpe_tunnel_dump_decode(msg):
    n = namedtuple('lisp_gpe_tunnel_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_gpe_tunnel_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_GPE_TUNNEL_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_LISP_GPE_TUNNEL_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_map_resolver_details_decode(msg):
    n = namedtuple('lisp_map_resolver_details', 'vl_msg_id, context, is_ipv6, ip_address')
    if not n:
        return None
    
    tr = unpack('>HIB16s', msg[:23])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def lisp_map_resolver_details(ip_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_MAP_RESOLVER_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIB16s', VL_API_LISP_MAP_RESOLVER_DETAILS, 0, context, ip_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_map_resolver_dump_decode(msg):
    n = namedtuple('lisp_map_resolver_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_map_resolver_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_MAP_RESOLVER_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_LISP_MAP_RESOLVER_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_enable_disable_status_details_decode(msg):
    n = namedtuple('lisp_enable_disable_status_details', 'vl_msg_id, context, feature_status, gpe_status')
    if not n:
        return None
    
    tr = unpack('>HIBB', msg[:8])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def lisp_enable_disable_status_details(gpe_status, async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ENABLE_DISABLE_STATUS_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIBB', VL_API_LISP_ENABLE_DISABLE_STATUS_DETAILS, 0, context, gpe_status))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def lisp_enable_disable_status_dump_decode(msg):
    n = namedtuple('lisp_enable_disable_status_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def lisp_enable_disable_status_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_LISP_ENABLE_DISABLE_STATUS_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_LISP_ENABLE_DISABLE_STATUS_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def interface_name_renumber_decode(msg):
    n = namedtuple('interface_name_renumber', 'vl_msg_id, client_index, context, sw_if_index, new_show_dev_instance')
    if not n:
        return None
    
    tr = unpack('>HIIII', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def interface_name_renumber(sw_if_index, new_show_dev_instance, async = False):
    global waiting_for_reply
    context = get_context(VL_API_INTERFACE_NAME_RENUMBER)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII', VL_API_INTERFACE_NAME_RENUMBER, 0, context, sw_if_index, new_show_dev_instance))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def interface_name_renumber_reply_decode(msg):
    n = namedtuple('interface_name_renumber_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def interface_name_renumber_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_INTERFACE_NAME_RENUMBER_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_INTERFACE_NAME_RENUMBER_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_ip4_arp_events_decode(msg):
    n = namedtuple('want_ip4_arp_events', 'vl_msg_id, client_index, context, enable_disable, pid, address')
    if not n:
        return None
    
    tr = unpack('>HIIBII', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def want_ip4_arp_events(enable_disable, pid, address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_IP4_ARP_EVENTS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBII', VL_API_WANT_IP4_ARP_EVENTS, 0, context, enable_disable, pid, address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def want_ip4_arp_events_reply_decode(msg):
    n = namedtuple('want_ip4_arp_events_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def want_ip4_arp_events_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_WANT_IP4_ARP_EVENTS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_WANT_IP4_ARP_EVENTS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ip4_arp_event_decode(msg):
    n = namedtuple('ip4_arp_event', 'vl_msg_id, client_index, context, address, pid, sw_if_index, new_mac')
    if not n:
        return None
    
    tr = unpack('>HIIIII6s', msg[:28])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def ip4_arp_event(address, pid, sw_if_index, new_mac, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IP4_ARP_EVENT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIII6s', VL_API_IP4_ARP_EVENT, 0, context, address, pid, sw_if_index, new_mac))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_domain_add_del_decode(msg):
    n = namedtuple('bridge_domain_add_del', 'vl_msg_id, client_index, context, bd_id, flood, uu_flood, forward, learn, arp_term, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIBBBBBB', msg[:20])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def bridge_domain_add_del(bd_id, flood, uu_flood, forward, learn, arp_term, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_DOMAIN_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIBBBBBB', VL_API_BRIDGE_DOMAIN_ADD_DEL, 0, context, bd_id, flood, uu_flood, forward, learn, arp_term, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_domain_add_del_reply_decode(msg):
    n = namedtuple('bridge_domain_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def bridge_domain_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_DOMAIN_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_BRIDGE_DOMAIN_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_domain_dump_decode(msg):
    n = namedtuple('bridge_domain_dump', 'vl_msg_id, client_index, context, bd_id')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def bridge_domain_dump(bd_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_DOMAIN_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIII', VL_API_BRIDGE_DOMAIN_DUMP, 0, context, bd_id))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_domain_details_decode(msg):
    n = namedtuple('bridge_domain_details', 'vl_msg_id, context, bd_id, flood, uu_flood, forward, learn, arp_term, bvi_sw_if_index, n_sw_ifs')
    if not n:
        return None
    
    tr = unpack('>HIIBBBBBII', msg[:23])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def bridge_domain_details(flood, uu_flood, forward, learn, arp_term, bvi_sw_if_index, n_sw_ifs, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_DOMAIN_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBBBBBII', VL_API_BRIDGE_DOMAIN_DETAILS, 0, context, flood, uu_flood, forward, learn, arp_term, bvi_sw_if_index, n_sw_ifs))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def bridge_domain_sw_if_details_decode(msg):
    n = namedtuple('bridge_domain_sw_if_details', 'vl_msg_id, context, bd_id, sw_if_index, shg')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def bridge_domain_sw_if_details(sw_if_index, shg, async = False):
    global waiting_for_reply
    context = get_context(VL_API_BRIDGE_DOMAIN_SW_IF_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_BRIDGE_DOMAIN_SW_IF_DETAILS, 0, context, sw_if_index, shg))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_client_config_decode(msg):
    n = namedtuple('dhcp_client_config', 'vl_msg_id, client_index, context, sw_if_index, hostname, is_add, want_dhcp_event, pid')
    if not n:
        return None
    
    tr = unpack('>HIII64sBBI', msg[:84])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def dhcp_client_config(sw_if_index, hostname, is_add, want_dhcp_event, pid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_CLIENT_CONFIG)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII64sBBI', VL_API_DHCP_CLIENT_CONFIG, 0, context, sw_if_index, hostname, is_add, want_dhcp_event, pid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_client_config_reply_decode(msg):
    n = namedtuple('dhcp_client_config_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def dhcp_client_config_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_CLIENT_CONFIG_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_DHCP_CLIENT_CONFIG_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def input_acl_set_interface_decode(msg):
    n = namedtuple('input_acl_set_interface', 'vl_msg_id, client_index, context, sw_if_index, ip4_table_index, ip6_table_index, l2_table_index, is_add')
    if not n:
        return None
    
    tr = unpack('>HIIIIIIB', msg[:27])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def input_acl_set_interface(sw_if_index, ip4_table_index, ip6_table_index, l2_table_index, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_INPUT_ACL_SET_INTERFACE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIIIB', VL_API_INPUT_ACL_SET_INTERFACE, 0, context, sw_if_index, ip4_table_index, ip6_table_index, l2_table_index, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def input_acl_set_interface_reply_decode(msg):
    n = namedtuple('input_acl_set_interface_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def input_acl_set_interface_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_INPUT_ACL_SET_INTERFACE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_INPUT_ACL_SET_INTERFACE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_spd_add_del_decode(msg):
    n = namedtuple('ipsec_spd_add_del', 'vl_msg_id, client_index, context, is_add, spd_id')
    if not n:
        return None
    
    tr = unpack('>HIIBI', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def ipsec_spd_add_del(is_add, spd_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SPD_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBI', VL_API_IPSEC_SPD_ADD_DEL, 0, context, is_add, spd_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_spd_add_del_reply_decode(msg):
    n = namedtuple('ipsec_spd_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ipsec_spd_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SPD_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IPSEC_SPD_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_interface_add_del_spd_decode(msg):
    n = namedtuple('ipsec_interface_add_del_spd', 'vl_msg_id, client_index, context, is_add, sw_if_index, spd_id')
    if not n:
        return None
    
    tr = unpack('>HIIBII', msg[:19])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def ipsec_interface_add_del_spd(is_add, sw_if_index, spd_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_INTERFACE_ADD_DEL_SPD)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBII', VL_API_IPSEC_INTERFACE_ADD_DEL_SPD, 0, context, is_add, sw_if_index, spd_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_interface_add_del_spd_reply_decode(msg):
    n = namedtuple('ipsec_interface_add_del_spd_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ipsec_interface_add_del_spd_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_INTERFACE_ADD_DEL_SPD_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IPSEC_INTERFACE_ADD_DEL_SPD_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_spd_add_del_entry_decode(msg):
    n = namedtuple('ipsec_spd_add_del_entry', 'vl_msg_id, client_index, context, is_add, spd_id, priority, is_outbound, is_ipv6, is_ip_any, remote_address_start, remote_address_stop, local_address_start, local_address_stop, protocol, remote_port_start, remote_port_stop, local_port_start, local_port_stop, policy, sa_id')
    if not n:
        return None
    
    tr = unpack('>HIIBIiBBB16s16s16s16sBHHHHBI', msg[:100])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],tr[15],tr[16],tr[17],tr[18],tr[19],))
    if not r:
        return None
    return r
    
def ipsec_spd_add_del_entry(is_add, spd_id, priority, is_outbound, is_ipv6, is_ip_any, remote_address_start, remote_address_stop, local_address_start, local_address_stop, protocol, remote_port_start, remote_port_stop, local_port_start, local_port_stop, policy, sa_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SPD_ADD_DEL_ENTRY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIiBBB16s16s16s16sBHHHHBI', VL_API_IPSEC_SPD_ADD_DEL_ENTRY, 0, context, is_add, spd_id, priority, is_outbound, is_ipv6, is_ip_any, remote_address_start, remote_address_stop, local_address_start, local_address_stop, protocol, remote_port_start, remote_port_stop, local_port_start, local_port_stop, policy, sa_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_spd_add_del_entry_reply_decode(msg):
    n = namedtuple('ipsec_spd_add_del_entry_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ipsec_spd_add_del_entry_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SPD_ADD_DEL_ENTRY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IPSEC_SPD_ADD_DEL_ENTRY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_sad_add_del_entry_decode(msg):
    n = namedtuple('ipsec_sad_add_del_entry', 'vl_msg_id, client_index, context, is_add, sad_id, spi, protocol, crypto_algorithm, crypto_key_length, crypto_key, integrity_algorithm, integrity_key_length, integrity_key, use_extended_sequence_number, is_tunnel, is_tunnel_ipv6, tunnel_src_address, tunnel_dst_address')
    if not n:
        return None
    
    tr = unpack('>HIIBIIBBB128sBB128sBBB16s16s', msg[:315])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],tr[15],tr[16],tr[17],))
    if not r:
        return None
    return r
    
def ipsec_sad_add_del_entry(is_add, sad_id, spi, protocol, crypto_algorithm, crypto_key_length, crypto_key, integrity_algorithm, integrity_key_length, integrity_key, use_extended_sequence_number, is_tunnel, is_tunnel_ipv6, tunnel_src_address, tunnel_dst_address, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SAD_ADD_DEL_ENTRY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIBIIBBB128sBB128sBBB16s16s', VL_API_IPSEC_SAD_ADD_DEL_ENTRY, 0, context, is_add, sad_id, spi, protocol, crypto_algorithm, crypto_key_length, crypto_key, integrity_algorithm, integrity_key_length, integrity_key, use_extended_sequence_number, is_tunnel, is_tunnel_ipv6, tunnel_src_address, tunnel_dst_address))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_sad_add_del_entry_reply_decode(msg):
    n = namedtuple('ipsec_sad_add_del_entry_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ipsec_sad_add_del_entry_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SAD_ADD_DEL_ENTRY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IPSEC_SAD_ADD_DEL_ENTRY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_sa_set_key_decode(msg):
    n = namedtuple('ipsec_sa_set_key', 'vl_msg_id, client_index, context, sa_id, crypto_key_length, crypto_key, integrity_key_length, integrity_key')
    if not n:
        return None
    
    tr = unpack('>HIIIB128sB128s', msg[:272])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def ipsec_sa_set_key(sa_id, crypto_key_length, crypto_key, integrity_key_length, integrity_key, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SA_SET_KEY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB128sB128s', VL_API_IPSEC_SA_SET_KEY, 0, context, sa_id, crypto_key_length, crypto_key, integrity_key_length, integrity_key))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ipsec_sa_set_key_reply_decode(msg):
    n = namedtuple('ipsec_sa_set_key_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ipsec_sa_set_key_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IPSEC_SA_SET_KEY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IPSEC_SA_SET_KEY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_add_del_decode(msg):
    n = namedtuple('ikev2_profile_add_del', 'vl_msg_id, client_index, context, name, is_add')
    if not n:
        return None
    
    tr = unpack('>HII64sB', msg[:75])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def ikev2_profile_add_del(name, is_add, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sB', VL_API_IKEV2_PROFILE_ADD_DEL, 0, context, name, is_add))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_add_del_reply_decode(msg):
    n = namedtuple('ikev2_profile_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ikev2_profile_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IKEV2_PROFILE_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_auth_decode(msg):
    n = namedtuple('ikev2_profile_set_auth', 'vl_msg_id, client_index, context, name, auth_method, is_hex, data_len, data')
    if not n:
        return None
    
    tr = unpack('>HII64sBBI', msg[:80])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],msg[80:],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_auth(name, auth_method, is_hex, data_len, data, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_AUTH)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sBBI', VL_API_IKEV2_PROFILE_SET_AUTH, 0, context, name, auth_method, is_hex, data_len) + data)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_auth_reply_decode(msg):
    n = namedtuple('ikev2_profile_set_auth_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_auth_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_AUTH_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IKEV2_PROFILE_SET_AUTH_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_id_decode(msg):
    n = namedtuple('ikev2_profile_set_id', 'vl_msg_id, client_index, context, name, is_local, id_type, data_len, data')
    if not n:
        return None
    
    tr = unpack('>HII64sBBI', msg[:80])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],msg[80:],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_id(name, is_local, id_type, data_len, data, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_ID)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sBBI', VL_API_IKEV2_PROFILE_SET_ID, 0, context, name, is_local, id_type, data_len) + data)

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_id_reply_decode(msg):
    n = namedtuple('ikev2_profile_set_id_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_id_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_ID_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IKEV2_PROFILE_SET_ID_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_ts_decode(msg):
    n = namedtuple('ikev2_profile_set_ts', 'vl_msg_id, client_index, context, name, is_local, proto, start_port, end_port, start_addr, end_addr')
    if not n:
        return None
    
    tr = unpack('>HII64sBBHHII', msg[:88])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_ts(name, is_local, proto, start_port, end_port, start_addr, end_addr, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_TS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sBBHHII', VL_API_IKEV2_PROFILE_SET_TS, 0, context, name, is_local, proto, start_port, end_port, start_addr, end_addr))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_profile_set_ts_reply_decode(msg):
    n = namedtuple('ikev2_profile_set_ts_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ikev2_profile_set_ts_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_PROFILE_SET_TS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IKEV2_PROFILE_SET_TS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_set_local_key_decode(msg):
    n = namedtuple('ikev2_set_local_key', 'vl_msg_id, client_index, context, key_file')
    if not n:
        return None
    
    tr = unpack('>HII256s', msg[:266])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def ikev2_set_local_key(key_file, async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_SET_LOCAL_KEY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII256s', VL_API_IKEV2_SET_LOCAL_KEY, 0, context, key_file))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def ikev2_set_local_key_reply_decode(msg):
    n = namedtuple('ikev2_set_local_key_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def ikev2_set_local_key_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_IKEV2_SET_LOCAL_KEY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_IKEV2_SET_LOCAL_KEY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def dhcp_compl_event_decode(msg):
    n = namedtuple('dhcp_compl_event', 'vl_msg_id, client_index, pid, hostname, is_ipv6, host_address, router_address, host_mac')
    if not n:
        return None
    
    tr = unpack('>HII64sB16s16s6s', msg[:113])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def dhcp_compl_event(hostname, is_ipv6, host_address, router_address, host_mac, async = False):
    global waiting_for_reply
    context = get_context(VL_API_DHCP_COMPL_EVENT)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64sB16s16s6s', VL_API_DHCP_COMPL_EVENT, 0, context, hostname, is_ipv6, host_address, router_address, host_mac))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_add_domain_decode(msg):
    n = namedtuple('map_add_domain', 'vl_msg_id, client_index, context, ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_prefix_len, ea_bits_len, psid_offset, psid_length, is_translation, mtu')
    if not n:
        return None
    
    tr = unpack('>HII16s4s16sBBBBBBBH', msg[:55])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],))
    if not r:
        return None
    return r
    
def map_add_domain(ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_prefix_len, ea_bits_len, psid_offset, psid_length, is_translation, mtu, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_ADD_DOMAIN)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII16s4s16sBBBBBBBH', VL_API_MAP_ADD_DOMAIN, 0, context, ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_prefix_len, ea_bits_len, psid_offset, psid_length, is_translation, mtu))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_add_domain_reply_decode(msg):
    n = namedtuple('map_add_domain_reply', 'vl_msg_id, context, index, retval')
    if not n:
        return None
    
    tr = unpack('>HIIi', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def map_add_domain_reply(retval, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_ADD_DOMAIN_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIi', VL_API_MAP_ADD_DOMAIN_REPLY, 0, context, retval))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_del_domain_decode(msg):
    n = namedtuple('map_del_domain', 'vl_msg_id, client_index, context, index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def map_del_domain(index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_DEL_DOMAIN)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_MAP_DEL_DOMAIN, 0, context, index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_del_domain_reply_decode(msg):
    n = namedtuple('map_del_domain_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def map_del_domain_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_DEL_DOMAIN_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MAP_DEL_DOMAIN_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_add_del_rule_decode(msg):
    n = namedtuple('map_add_del_rule', 'vl_msg_id, client_index, context, index, is_add, ip6_dst, psid')
    if not n:
        return None
    
    tr = unpack('>HIIII16sH', msg[:36])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],))
    if not r:
        return None
    return r
    
def map_add_del_rule(index, is_add, ip6_dst, psid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_ADD_DEL_RULE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIII16sH', VL_API_MAP_ADD_DEL_RULE, 0, context, index, is_add, ip6_dst, psid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_add_del_rule_reply_decode(msg):
    n = namedtuple('map_add_del_rule_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def map_add_del_rule_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_ADD_DEL_RULE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_MAP_ADD_DEL_RULE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_domain_dump_decode(msg):
    n = namedtuple('map_domain_dump', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def map_domain_dump(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_DOMAIN_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HII', VL_API_MAP_DOMAIN_DUMP, 0, context, ))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_domain_details_decode(msg):
    n = namedtuple('map_domain_details', 'vl_msg_id, context, domain_index, ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_len, ea_bits_len, psid_offset, psid_length, flags, mtu, is_translation')
    if not n:
        return None
    
    tr = unpack('>HII16s4s16sBBBBBBBHB', msg[:56])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],tr[12],tr[13],tr[14],))
    if not r:
        return None
    return r
    
def map_domain_details(ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_len, ea_bits_len, psid_offset, psid_length, flags, mtu, is_translation, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_DOMAIN_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII16s4s16sBBBBBBBHB', VL_API_MAP_DOMAIN_DETAILS, 0, context, ip6_prefix, ip4_prefix, ip6_src, ip6_prefix_len, ip4_prefix_len, ip6_src_len, ea_bits_len, psid_offset, psid_length, flags, mtu, is_translation))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_rule_dump_decode(msg):
    n = namedtuple('map_rule_dump', 'vl_msg_id, client_index, context, domain_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def map_rule_dump(domain_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_RULE_DUMP)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    results[context]['m'] = True
    vpp_api.write(pack('>HIII', VL_API_MAP_RULE_DUMP, 0, context, domain_index))
    vpp_api.write(pack('>HII', VL_API_CONTROL_PING, 0, context))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_rule_details_decode(msg):
    n = namedtuple('map_rule_details', 'vl_msg_id, context, ip6_dst, psid')
    if not n:
        return None
    
    tr = unpack('>HI16sH', msg[:24])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def map_rule_details(psid, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_RULE_DETAILS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HI16sH', VL_API_MAP_RULE_DETAILS, 0, context, psid))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_summary_stats_decode(msg):
    n = namedtuple('map_summary_stats', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def map_summary_stats(async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_SUMMARY_STATS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_MAP_SUMMARY_STATS, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def map_summary_stats_reply_decode(msg):
    n = namedtuple('map_summary_stats_reply', 'vl_msg_id, context, retval, total_bindings, total_pkts, total_bytes, total_ip4_fragments, total_security_check')
    if not n:
        return None
    
    tr = unpack('>HIiQQQQQQQQ', msg[:74])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4:6],tr[6:8],tr[8],tr[9:11],))
    if not r:
        return None
    return r
    
def map_summary_stats_reply(total_bindings, total_pkts, total_bytes, total_ip4_fragments, total_security_check, async = False):
    global waiting_for_reply
    context = get_context(VL_API_MAP_SUMMARY_STATS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiQQQQQQQQ', VL_API_MAP_SUMMARY_STATS_REPLY, 0, context, total_bindings, total_pkts, total_bytes, total_ip4_fragments, total_security_check))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cop_interface_enable_disable_decode(msg):
    n = namedtuple('cop_interface_enable_disable', 'vl_msg_id, client_index, context, sw_if_index, enable_disable')
    if not n:
        return None
    
    tr = unpack('>HIIIB', msg[:15])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],))
    if not r:
        return None
    return r
    
def cop_interface_enable_disable(sw_if_index, enable_disable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_COP_INTERFACE_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIB', VL_API_COP_INTERFACE_ENABLE_DISABLE, 0, context, sw_if_index, enable_disable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cop_interface_enable_disable_reply_decode(msg):
    n = namedtuple('cop_interface_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def cop_interface_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_COP_INTERFACE_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_COP_INTERFACE_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cop_whitelist_enable_disable_decode(msg):
    n = namedtuple('cop_whitelist_enable_disable', 'vl_msg_id, client_index, context, sw_if_index, fib_id, ip4, ip6, default_cop')
    if not n:
        return None
    
    tr = unpack('>HIIIIBBB', msg[:21])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],))
    if not r:
        return None
    return r
    
def cop_whitelist_enable_disable(sw_if_index, fib_id, ip4, ip6, default_cop, async = False):
    global waiting_for_reply
    context = get_context(VL_API_COP_WHITELIST_ENABLE_DISABLE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIIIBBB', VL_API_COP_WHITELIST_ENABLE_DISABLE, 0, context, sw_if_index, fib_id, ip4, ip6, default_cop))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def cop_whitelist_enable_disable_reply_decode(msg):
    n = namedtuple('cop_whitelist_enable_disable_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def cop_whitelist_enable_disable_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_COP_WHITELIST_ENABLE_DISABLE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_COP_WHITELIST_ENABLE_DISABLE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def get_node_graph_decode(msg):
    n = namedtuple('get_node_graph', 'vl_msg_id, client_index, context')
    if not n:
        return None
    
    tr = unpack('>HII', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def get_node_graph(async = False):
    global waiting_for_reply
    context = get_context(VL_API_GET_NODE_GRAPH)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII', VL_API_GET_NODE_GRAPH, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def get_node_graph_reply_decode(msg):
    n = namedtuple('get_node_graph_reply', 'vl_msg_id, context, retval, reply_in_shmem')
    if not n:
        return None
    
    tr = unpack('>HIiQ', msg[:18])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def get_node_graph_reply(reply_in_shmem, async = False):
    global waiting_for_reply
    context = get_context(VL_API_GET_NODE_GRAPH_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIiQ', VL_API_GET_NODE_GRAPH_REPLY, 0, context, reply_in_shmem))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_clear_stats_decode(msg):
    n = namedtuple('sw_interface_clear_stats', 'vl_msg_id, client_index, context, sw_if_index')
    if not n:
        return None
    
    tr = unpack('>HIII', msg[:14])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def sw_interface_clear_stats(sw_if_index, async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_CLEAR_STATS)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIII', VL_API_SW_INTERFACE_CLEAR_STATS, 0, context, sw_if_index))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def sw_interface_clear_stats_reply_decode(msg):
    n = namedtuple('sw_interface_clear_stats_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def sw_interface_clear_stats_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_SW_INTERFACE_CLEAR_STATS_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_SW_INTERFACE_CLEAR_STATS_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_add_decode(msg):
    n = namedtuple('trace_profile_add', 'vl_msg_id, client_index, context, id, trace_type, trace_num_elt, trace_ppc, trace_tsp, trace_app_data, pow_enable, node_id')
    if not n:
        return None
    
    tr = unpack('>HIIHBBBBIBI', msg[:25])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],))
    if not r:
        return None
    return r
    
def trace_profile_add(id, trace_type, trace_num_elt, trace_ppc, trace_tsp, trace_app_data, pow_enable, node_id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_ADD)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIHBBBBIBI', VL_API_TRACE_PROFILE_ADD, 0, context, id, trace_type, trace_num_elt, trace_ppc, trace_tsp, trace_app_data, pow_enable, node_id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_add_reply_decode(msg):
    n = namedtuple('trace_profile_add_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def trace_profile_add_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_ADD_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_TRACE_PROFILE_ADD_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_apply_decode(msg):
    n = namedtuple('trace_profile_apply', 'vl_msg_id, client_index, context, id, dest_ipv6, prefix_length, vrf_id, trace_op, enable')
    if not n:
        return None
    
    tr = unpack('>HIIH16sIIBB', msg[:38])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],))
    if not r:
        return None
    return r
    
def trace_profile_apply(id, dest_ipv6, prefix_length, vrf_id, trace_op, enable, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_APPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIH16sIIBB', VL_API_TRACE_PROFILE_APPLY, 0, context, id, dest_ipv6, prefix_length, vrf_id, trace_op, enable))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_apply_reply_decode(msg):
    n = namedtuple('trace_profile_apply_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def trace_profile_apply_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_APPLY_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_TRACE_PROFILE_APPLY_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_del_decode(msg):
    n = namedtuple('trace_profile_del', 'vl_msg_id, client_index, context, id')
    if not n:
        return None
    
    tr = unpack('>HIIH', msg[:12])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def trace_profile_del(id, async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIH', VL_API_TRACE_PROFILE_DEL, 0, context, id))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def trace_profile_del_reply_decode(msg):
    n = namedtuple('trace_profile_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def trace_profile_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_TRACE_PROFILE_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_TRACE_PROFILE_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def af_packet_create_decode(msg):
    n = namedtuple('af_packet_create', 'vl_msg_id, client_index, context, host_if_name, hw_addr, use_random_hw_addr')
    if not n:
        return None
    
    tr = unpack('>HII64s6sB', msg[:81])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],))
    if not r:
        return None
    return r
    
def af_packet_create(host_if_name, hw_addr, use_random_hw_addr, async = False):
    global waiting_for_reply
    context = get_context(VL_API_AF_PACKET_CREATE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s6sB', VL_API_AF_PACKET_CREATE, 0, context, host_if_name, hw_addr, use_random_hw_addr))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def af_packet_create_reply_decode(msg):
    n = namedtuple('af_packet_create_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def af_packet_create_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_AF_PACKET_CREATE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_AF_PACKET_CREATE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def af_packet_delete_decode(msg):
    n = namedtuple('af_packet_delete', 'vl_msg_id, client_index, context, host_if_name')
    if not n:
        return None
    
    tr = unpack('>HII64s', msg[:74])
    r = n._make((tr[0],tr[1],tr[2],tr[3],))
    if not r:
        return None
    return r
    
def af_packet_delete(host_if_name, async = False):
    global waiting_for_reply
    context = get_context(VL_API_AF_PACKET_DELETE)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HII64s', VL_API_AF_PACKET_DELETE, 0, context, host_if_name))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def af_packet_delete_reply_decode(msg):
    n = namedtuple('af_packet_delete_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def af_packet_delete_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_AF_PACKET_DELETE_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_AF_PACKET_DELETE_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def policer_add_del_decode(msg):
    n = namedtuple('policer_add_del', 'vl_msg_id, client_index, context, is_add, name, cir, eir, cb, eb, rate_type, round_type, type')
    if not n:
        return None
    
    tr = unpack('>HIIB64sIIQQBBB', msg[:102])
    r = n._make((tr[0],tr[1],tr[2],tr[3],tr[4],tr[5],tr[6],tr[7],tr[8],tr[9],tr[10],tr[11],))
    if not r:
        return None
    return r
    
def policer_add_del(is_add, name, cir, eir, cb, eb, rate_type, round_type, type, async = False):
    global waiting_for_reply
    context = get_context(VL_API_POLICER_ADD_DEL)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIIB64sIIQQBBB', VL_API_POLICER_ADD_DEL, 0, context, is_add, name, cir, eir, cb, eb, rate_type, round_type, type))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
def policer_add_del_reply_decode(msg):
    n = namedtuple('policer_add_del_reply', 'vl_msg_id, context, retval')
    if not n:
        return None
    
    tr = unpack('>HIi', msg[:10])
    r = n._make((tr[0],tr[1],tr[2],))
    if not r:
        return None
    return r
    
def policer_add_del_reply(async = False):
    global waiting_for_reply
    context = get_context(VL_API_POLICER_ADD_DEL_REPLY)

    results[context] = {}
    results[context]['e'] = threading.Event()
    results[context]['e'].clear()
    results[context]['r'] = []
    waiting_for_reply = True
    
    vpp_api.write(pack('>HIi', VL_API_POLICER_ADD_DEL_REPLY, 0, context, ))

    if not async:
        results[context]['e'].wait(5)
        return results[context]['r']
    return context
    
api_func_table = [0] * 10000
api_func_table[VL_API_WANT_INTERFACE_EVENTS] = want_interface_events_decode
api_func_table[VL_API_WANT_INTERFACE_EVENTS_REPLY] = want_interface_events_reply_decode
api_func_table[VL_API_SW_INTERFACE_DETAILS] = sw_interface_details_decode
api_func_table[VL_API_SW_INTERFACE_SET_FLAGS] = sw_interface_set_flags_decode
api_func_table[VL_API_SW_INTERFACE_SET_FLAGS_REPLY] = sw_interface_set_flags_reply_decode
api_func_table[VL_API_SW_INTERFACE_DUMP] = sw_interface_dump_decode
api_func_table[VL_API_SW_INTERFACE_ADD_DEL_ADDRESS] = sw_interface_add_del_address_decode
api_func_table[VL_API_SW_INTERFACE_ADD_DEL_ADDRESS_REPLY] = sw_interface_add_del_address_reply_decode
api_func_table[VL_API_SW_INTERFACE_SET_TABLE] = sw_interface_set_table_decode
api_func_table[VL_API_SW_INTERFACE_SET_TABLE_REPLY] = sw_interface_set_table_reply_decode
api_func_table[VL_API_TAP_CONNECT] = tap_connect_decode
api_func_table[VL_API_TAP_CONNECT_REPLY] = tap_connect_reply_decode
api_func_table[VL_API_TAP_MODIFY] = tap_modify_decode
api_func_table[VL_API_TAP_MODIFY_REPLY] = tap_modify_reply_decode
api_func_table[VL_API_TAP_DELETE] = tap_delete_decode
api_func_table[VL_API_TAP_DELETE_REPLY] = tap_delete_reply_decode
api_func_table[VL_API_SW_INTERFACE_TAP_DUMP] = sw_interface_tap_dump_decode
api_func_table[VL_API_SW_INTERFACE_TAP_DETAILS] = sw_interface_tap_details_decode
api_func_table[VL_API_CREATE_VLAN_SUBIF] = create_vlan_subif_decode
api_func_table[VL_API_CREATE_VLAN_SUBIF_REPLY] = create_vlan_subif_reply_decode
api_func_table[VL_API_IP_ADD_DEL_ROUTE] = ip_add_del_route_decode
api_func_table[VL_API_IP_ADD_DEL_ROUTE_REPLY] = ip_add_del_route_reply_decode
api_func_table[VL_API_MPLS_GRE_ADD_DEL_TUNNEL] = mpls_gre_add_del_tunnel_decode
api_func_table[VL_API_MPLS_GRE_ADD_DEL_TUNNEL_REPLY] = mpls_gre_add_del_tunnel_reply_decode
api_func_table[VL_API_MPLS_ADD_DEL_ENCAP] = mpls_add_del_encap_decode
api_func_table[VL_API_MPLS_ADD_DEL_ENCAP_REPLY] = mpls_add_del_encap_reply_decode
api_func_table[VL_API_MPLS_ADD_DEL_DECAP] = mpls_add_del_decap_decode
api_func_table[VL_API_MPLS_ADD_DEL_DECAP_REPLY] = mpls_add_del_decap_reply_decode
api_func_table[VL_API_PROXY_ARP_ADD_DEL] = proxy_arp_add_del_decode
api_func_table[VL_API_PROXY_ARP_ADD_DEL_REPLY] = proxy_arp_add_del_reply_decode
api_func_table[VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE] = proxy_arp_intfc_enable_disable_decode
api_func_table[VL_API_PROXY_ARP_INTFC_ENABLE_DISABLE_REPLY] = proxy_arp_intfc_enable_disable_reply_decode
api_func_table[VL_API_IP_NEIGHBOR_ADD_DEL] = ip_neighbor_add_del_decode
api_func_table[VL_API_IP_NEIGHBOR_ADD_DEL_REPLY] = ip_neighbor_add_del_reply_decode
api_func_table[VL_API_RESET_VRF] = reset_vrf_decode
api_func_table[VL_API_RESET_VRF_REPLY] = reset_vrf_reply_decode
api_func_table[VL_API_IS_ADDRESS_REACHABLE] = is_address_reachable_decode
api_func_table[VL_API_WANT_STATS] = want_stats_decode
api_func_table[VL_API_WANT_STATS_REPLY] = want_stats_reply_decode
api_func_table[VL_API_VNET_INTERFACE_COUNTERS] = vnet_interface_counters_decode
api_func_table[VL_API_VNET_IP4_FIB_COUNTERS] = vnet_ip4_fib_counters_decode
api_func_table[VL_API_VNET_IP6_FIB_COUNTERS] = vnet_ip6_fib_counters_decode
api_func_table[VL_API_VNET_GET_SUMMARY_STATS] = vnet_get_summary_stats_decode
api_func_table[VL_API_VNET_SUMMARY_STATS_REPLY] = vnet_summary_stats_reply_decode
api_func_table[VL_API_OAM_EVENT] = oam_event_decode
api_func_table[VL_API_WANT_OAM_EVENTS] = want_oam_events_decode
api_func_table[VL_API_WANT_OAM_EVENTS_REPLY] = want_oam_events_reply_decode
api_func_table[VL_API_OAM_ADD_DEL] = oam_add_del_decode
api_func_table[VL_API_OAM_ADD_DEL_REPLY] = oam_add_del_reply_decode
api_func_table[VL_API_RESET_FIB] = reset_fib_decode
api_func_table[VL_API_RESET_FIB_REPLY] = reset_fib_reply_decode
api_func_table[VL_API_DHCP_PROXY_CONFIG] = dhcp_proxy_config_decode
api_func_table[VL_API_DHCP_PROXY_CONFIG_REPLY] = dhcp_proxy_config_reply_decode
api_func_table[VL_API_DHCP_PROXY_SET_VSS] = dhcp_proxy_set_vss_decode
api_func_table[VL_API_DHCP_PROXY_SET_VSS_REPLY] = dhcp_proxy_set_vss_reply_decode
api_func_table[VL_API_SET_IP_FLOW_HASH] = set_ip_flow_hash_decode
api_func_table[VL_API_SET_IP_FLOW_HASH_REPLY] = set_ip_flow_hash_reply_decode
api_func_table[VL_API_SW_INTERFACE_IP6ND_RA_CONFIG] = sw_interface_ip6nd_ra_config_decode
api_func_table[VL_API_SW_INTERFACE_IP6ND_RA_CONFIG_REPLY] = sw_interface_ip6nd_ra_config_reply_decode
api_func_table[VL_API_SW_INTERFACE_IP6ND_RA_PREFIX] = sw_interface_ip6nd_ra_prefix_decode
api_func_table[VL_API_SW_INTERFACE_IP6ND_RA_PREFIX_REPLY] = sw_interface_ip6nd_ra_prefix_reply_decode
api_func_table[VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE] = sw_interface_ip6_enable_disable_decode
api_func_table[VL_API_SW_INTERFACE_IP6_ENABLE_DISABLE_REPLY] = sw_interface_ip6_enable_disable_reply_decode
api_func_table[VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS] = sw_interface_ip6_set_link_local_address_decode
api_func_table[VL_API_SW_INTERFACE_IP6_SET_LINK_LOCAL_ADDRESS_REPLY] = sw_interface_ip6_set_link_local_address_reply_decode
api_func_table[VL_API_SW_INTERFACE_SET_UNNUMBERED] = sw_interface_set_unnumbered_decode
api_func_table[VL_API_SW_INTERFACE_SET_UNNUMBERED_REPLY] = sw_interface_set_unnumbered_reply_decode
api_func_table[VL_API_CREATE_LOOPBACK] = create_loopback_decode
api_func_table[VL_API_CREATE_LOOPBACK_REPLY] = create_loopback_reply_decode
api_func_table[VL_API_DELETE_LOOPBACK] = delete_loopback_decode
api_func_table[VL_API_DELETE_LOOPBACK_REPLY] = delete_loopback_reply_decode
api_func_table[VL_API_CONTROL_PING] = control_ping_decode
api_func_table[VL_API_CONTROL_PING_REPLY] = control_ping_reply_decode
api_func_table[VL_API_CLI_REQUEST] = cli_request_decode
api_func_table[VL_API_CLI_REPLY] = cli_reply_decode
api_func_table[VL_API_SET_ARP_NEIGHBOR_LIMIT] = set_arp_neighbor_limit_decode
api_func_table[VL_API_SET_ARP_NEIGHBOR_LIMIT_REPLY] = set_arp_neighbor_limit_reply_decode
api_func_table[VL_API_L2_PATCH_ADD_DEL] = l2_patch_add_del_decode
api_func_table[VL_API_L2_PATCH_ADD_DEL_REPLY] = l2_patch_add_del_reply_decode
api_func_table[VL_API_SR_TUNNEL_ADD_DEL] = sr_tunnel_add_del_decode
api_func_table[VL_API_SR_TUNNEL_ADD_DEL_REPLY] = sr_tunnel_add_del_reply_decode
api_func_table[VL_API_SR_POLICY_ADD_DEL] = sr_policy_add_del_decode
api_func_table[VL_API_SR_POLICY_ADD_DEL_REPLY] = sr_policy_add_del_reply_decode
api_func_table[VL_API_SR_MULTICAST_MAP_ADD_DEL] = sr_multicast_map_add_del_decode
api_func_table[VL_API_SR_MULTICAST_MAP_ADD_DEL_REPLY] = sr_multicast_map_add_del_reply_decode
api_func_table[VL_API_SW_INTERFACE_SET_VPATH] = sw_interface_set_vpath_decode
api_func_table[VL_API_SW_INTERFACE_SET_VPATH_REPLY] = sw_interface_set_vpath_reply_decode
api_func_table[VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL] = mpls_ethernet_add_del_tunnel_decode
api_func_table[VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_REPLY] = mpls_ethernet_add_del_tunnel_reply_decode
api_func_table[VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2] = mpls_ethernet_add_del_tunnel_2_decode
api_func_table[VL_API_MPLS_ETHERNET_ADD_DEL_TUNNEL_2_REPLY] = mpls_ethernet_add_del_tunnel_2_reply_decode
api_func_table[VL_API_SW_INTERFACE_SET_L2_XCONNECT] = sw_interface_set_l2_xconnect_decode
api_func_table[VL_API_SW_INTERFACE_SET_L2_XCONNECT_REPLY] = sw_interface_set_l2_xconnect_reply_decode
api_func_table[VL_API_SW_INTERFACE_SET_L2_BRIDGE] = sw_interface_set_l2_bridge_decode
api_func_table[VL_API_SW_INTERFACE_SET_L2_BRIDGE_REPLY] = sw_interface_set_l2_bridge_reply_decode
api_func_table[VL_API_L2FIB_ADD_DEL] = l2fib_add_del_decode
api_func_table[VL_API_L2FIB_ADD_DEL_REPLY] = l2fib_add_del_reply_decode
api_func_table[VL_API_L2_FLAGS] = l2_flags_decode
api_func_table[VL_API_L2_FLAGS_REPLY] = l2_flags_reply_decode
api_func_table[VL_API_BRIDGE_FLAGS] = bridge_flags_decode
api_func_table[VL_API_BRIDGE_FLAGS_REPLY] = bridge_flags_reply_decode
api_func_table[VL_API_BD_IP_MAC_ADD_DEL] = bd_ip_mac_add_del_decode
api_func_table[VL_API_BD_IP_MAC_ADD_DEL_REPLY] = bd_ip_mac_add_del_reply_decode
api_func_table[VL_API_CLASSIFY_ADD_DEL_TABLE] = classify_add_del_table_decode
api_func_table[VL_API_CLASSIFY_ADD_DEL_TABLE_REPLY] = classify_add_del_table_reply_decode
api_func_table[VL_API_CLASSIFY_ADD_DEL_SESSION] = classify_add_del_session_decode
api_func_table[VL_API_CLASSIFY_ADD_DEL_SESSION_REPLY] = classify_add_del_session_reply_decode
api_func_table[VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE] = classify_set_interface_ip_table_decode
api_func_table[VL_API_CLASSIFY_SET_INTERFACE_IP_TABLE_REPLY] = classify_set_interface_ip_table_reply_decode
api_func_table[VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES] = classify_set_interface_l2_tables_decode
api_func_table[VL_API_CLASSIFY_SET_INTERFACE_L2_TABLES_REPLY] = classify_set_interface_l2_tables_reply_decode
api_func_table[VL_API_GET_NODE_INDEX] = get_node_index_decode
api_func_table[VL_API_GET_NODE_INDEX_REPLY] = get_node_index_reply_decode
api_func_table[VL_API_ADD_NODE_NEXT] = add_node_next_decode
api_func_table[VL_API_ADD_NODE_NEXT_REPLY] = add_node_next_reply_decode
api_func_table[VL_API_DHCP_PROXY_CONFIG_2] = dhcp_proxy_config_2_decode
api_func_table[VL_API_DHCP_PROXY_CONFIG_2_REPLY] = dhcp_proxy_config_2_reply_decode
api_func_table[VL_API_L2TPV3_CREATE_TUNNEL] = l2tpv3_create_tunnel_decode
api_func_table[VL_API_L2TPV3_CREATE_TUNNEL_REPLY] = l2tpv3_create_tunnel_reply_decode
api_func_table[VL_API_L2TPV3_SET_TUNNEL_COOKIES] = l2tpv3_set_tunnel_cookies_decode
api_func_table[VL_API_L2TPV3_SET_TUNNEL_COOKIES_REPLY] = l2tpv3_set_tunnel_cookies_reply_decode
api_func_table[VL_API_SW_IF_L2TPV3_TUNNEL_DETAILS] = sw_if_l2tpv3_tunnel_details_decode
api_func_table[VL_API_SW_IF_L2TPV3_TUNNEL_DUMP] = sw_if_l2tpv3_tunnel_dump_decode
api_func_table[VL_API_L2_FIB_CLEAR_TABLE] = l2_fib_clear_table_decode
api_func_table[VL_API_L2_FIB_CLEAR_TABLE_REPLY] = l2_fib_clear_table_reply_decode
api_func_table[VL_API_L2_INTERFACE_EFP_FILTER] = l2_interface_efp_filter_decode
api_func_table[VL_API_L2_INTERFACE_EFP_FILTER_REPLY] = l2_interface_efp_filter_reply_decode
api_func_table[VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE] = l2tpv3_interface_enable_disable_decode
api_func_table[VL_API_L2TPV3_INTERFACE_ENABLE_DISABLE_REPLY] = l2tpv3_interface_enable_disable_reply_decode
api_func_table[VL_API_L2TPV3_SET_LOOKUP_KEY] = l2tpv3_set_lookup_key_decode
api_func_table[VL_API_L2TPV3_SET_LOOKUP_KEY_REPLY] = l2tpv3_set_lookup_key_reply_decode
api_func_table[VL_API_VXLAN_ADD_DEL_TUNNEL] = vxlan_add_del_tunnel_decode
api_func_table[VL_API_VXLAN_ADD_DEL_TUNNEL_REPLY] = vxlan_add_del_tunnel_reply_decode
api_func_table[VL_API_VXLAN_TUNNEL_DUMP] = vxlan_tunnel_dump_decode
api_func_table[VL_API_VXLAN_TUNNEL_DETAILS] = vxlan_tunnel_details_decode
api_func_table[VL_API_GRE_ADD_DEL_TUNNEL] = gre_add_del_tunnel_decode
api_func_table[VL_API_GRE_ADD_DEL_TUNNEL_REPLY] = gre_add_del_tunnel_reply_decode
api_func_table[VL_API_GRE_TUNNEL_DUMP] = gre_tunnel_dump_decode
api_func_table[VL_API_GRE_TUNNEL_DETAILS] = gre_tunnel_details_decode
api_func_table[VL_API_L2_INTERFACE_VLAN_TAG_REWRITE] = l2_interface_vlan_tag_rewrite_decode
api_func_table[VL_API_L2_INTERFACE_VLAN_TAG_REWRITE_REPLY] = l2_interface_vlan_tag_rewrite_reply_decode
api_func_table[VL_API_CREATE_VHOST_USER_IF] = create_vhost_user_if_decode
api_func_table[VL_API_CREATE_VHOST_USER_IF_REPLY] = create_vhost_user_if_reply_decode
api_func_table[VL_API_MODIFY_VHOST_USER_IF] = modify_vhost_user_if_decode
api_func_table[VL_API_MODIFY_VHOST_USER_IF_REPLY] = modify_vhost_user_if_reply_decode
api_func_table[VL_API_DELETE_VHOST_USER_IF] = delete_vhost_user_if_decode
api_func_table[VL_API_DELETE_VHOST_USER_IF_REPLY] = delete_vhost_user_if_reply_decode
api_func_table[VL_API_CREATE_SUBIF] = create_subif_decode
api_func_table[VL_API_CREATE_SUBIF_REPLY] = create_subif_reply_decode
api_func_table[VL_API_SHOW_VERSION] = show_version_decode
api_func_table[VL_API_SHOW_VERSION_REPLY] = show_version_reply_decode
api_func_table[VL_API_SW_INTERFACE_VHOST_USER_DETAILS] = sw_interface_vhost_user_details_decode
api_func_table[VL_API_SW_INTERFACE_VHOST_USER_DUMP] = sw_interface_vhost_user_dump_decode
api_func_table[VL_API_IP_ADDRESS_DETAILS] = ip_address_details_decode
api_func_table[VL_API_IP_ADDRESS_DUMP] = ip_address_dump_decode
api_func_table[VL_API_IP_DETAILS] = ip_details_decode
api_func_table[VL_API_IP_DUMP] = ip_dump_decode
api_func_table[VL_API_L2_FIB_TABLE_ENTRY] = l2_fib_table_entry_decode
api_func_table[VL_API_L2_FIB_TABLE_DUMP] = l2_fib_table_dump_decode
api_func_table[VL_API_VXLAN_GPE_ADD_DEL_TUNNEL] = vxlan_gpe_add_del_tunnel_decode
api_func_table[VL_API_VXLAN_GPE_ADD_DEL_TUNNEL_REPLY] = vxlan_gpe_add_del_tunnel_reply_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCATOR_SET] = lisp_add_del_locator_set_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCATOR_SET_REPLY] = lisp_add_del_locator_set_reply_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCATOR] = lisp_add_del_locator_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCATOR_REPLY] = lisp_add_del_locator_reply_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCAL_EID] = lisp_add_del_local_eid_decode
api_func_table[VL_API_LISP_ADD_DEL_LOCAL_EID_REPLY] = lisp_add_del_local_eid_reply_decode
api_func_table[VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY] = lisp_gpe_add_del_fwd_entry_decode
api_func_table[VL_API_LISP_GPE_ADD_DEL_FWD_ENTRY_REPLY] = lisp_gpe_add_del_fwd_entry_reply_decode
api_func_table[VL_API_LISP_ADD_DEL_MAP_RESOLVER] = lisp_add_del_map_resolver_decode
api_func_table[VL_API_LISP_ADD_DEL_MAP_RESOLVER_REPLY] = lisp_add_del_map_resolver_reply_decode
api_func_table[VL_API_LISP_GPE_ENABLE_DISABLE] = lisp_gpe_enable_disable_decode
api_func_table[VL_API_LISP_GPE_ENABLE_DISABLE_REPLY] = lisp_gpe_enable_disable_reply_decode
api_func_table[VL_API_LISP_ENABLE_DISABLE] = lisp_enable_disable_decode
api_func_table[VL_API_LISP_ENABLE_DISABLE_REPLY] = lisp_enable_disable_reply_decode
api_func_table[VL_API_LISP_GPE_ADD_DEL_IFACE] = lisp_gpe_add_del_iface_decode
api_func_table[VL_API_LISP_GPE_ADD_DEL_IFACE_REPLY] = lisp_gpe_add_del_iface_reply_decode
api_func_table[VL_API_LISP_ADD_DEL_REMOTE_MAPPING] = lisp_add_del_remote_mapping_decode
api_func_table[VL_API_LISP_ADD_DEL_REMOTE_MAPPING_REPLY] = lisp_add_del_remote_mapping_reply_decode
api_func_table[VL_API_LISP_LOCATOR_SET_DETAILS] = lisp_locator_set_details_decode
api_func_table[VL_API_LISP_LOCATOR_SET_DUMP] = lisp_locator_set_dump_decode
api_func_table[VL_API_LISP_LOCAL_EID_TABLE_DETAILS] = lisp_local_eid_table_details_decode
api_func_table[VL_API_LISP_LOCAL_EID_TABLE_DUMP] = lisp_local_eid_table_dump_decode
api_func_table[VL_API_LISP_GPE_TUNNEL_DETAILS] = lisp_gpe_tunnel_details_decode
api_func_table[VL_API_LISP_GPE_TUNNEL_DUMP] = lisp_gpe_tunnel_dump_decode
api_func_table[VL_API_LISP_MAP_RESOLVER_DETAILS] = lisp_map_resolver_details_decode
api_func_table[VL_API_LISP_MAP_RESOLVER_DUMP] = lisp_map_resolver_dump_decode
api_func_table[VL_API_LISP_ENABLE_DISABLE_STATUS_DETAILS] = lisp_enable_disable_status_details_decode
api_func_table[VL_API_LISP_ENABLE_DISABLE_STATUS_DUMP] = lisp_enable_disable_status_dump_decode
api_func_table[VL_API_INTERFACE_NAME_RENUMBER] = interface_name_renumber_decode
api_func_table[VL_API_INTERFACE_NAME_RENUMBER_REPLY] = interface_name_renumber_reply_decode
api_func_table[VL_API_WANT_IP4_ARP_EVENTS] = want_ip4_arp_events_decode
api_func_table[VL_API_WANT_IP4_ARP_EVENTS_REPLY] = want_ip4_arp_events_reply_decode
api_func_table[VL_API_IP4_ARP_EVENT] = ip4_arp_event_decode
api_func_table[VL_API_BRIDGE_DOMAIN_ADD_DEL] = bridge_domain_add_del_decode
api_func_table[VL_API_BRIDGE_DOMAIN_ADD_DEL_REPLY] = bridge_domain_add_del_reply_decode
api_func_table[VL_API_BRIDGE_DOMAIN_DUMP] = bridge_domain_dump_decode
api_func_table[VL_API_BRIDGE_DOMAIN_DETAILS] = bridge_domain_details_decode
api_func_table[VL_API_BRIDGE_DOMAIN_SW_IF_DETAILS] = bridge_domain_sw_if_details_decode
api_func_table[VL_API_DHCP_CLIENT_CONFIG] = dhcp_client_config_decode
api_func_table[VL_API_DHCP_CLIENT_CONFIG_REPLY] = dhcp_client_config_reply_decode
api_func_table[VL_API_INPUT_ACL_SET_INTERFACE] = input_acl_set_interface_decode
api_func_table[VL_API_INPUT_ACL_SET_INTERFACE_REPLY] = input_acl_set_interface_reply_decode
api_func_table[VL_API_IPSEC_SPD_ADD_DEL] = ipsec_spd_add_del_decode
api_func_table[VL_API_IPSEC_SPD_ADD_DEL_REPLY] = ipsec_spd_add_del_reply_decode
api_func_table[VL_API_IPSEC_INTERFACE_ADD_DEL_SPD] = ipsec_interface_add_del_spd_decode
api_func_table[VL_API_IPSEC_INTERFACE_ADD_DEL_SPD_REPLY] = ipsec_interface_add_del_spd_reply_decode
api_func_table[VL_API_IPSEC_SPD_ADD_DEL_ENTRY] = ipsec_spd_add_del_entry_decode
api_func_table[VL_API_IPSEC_SPD_ADD_DEL_ENTRY_REPLY] = ipsec_spd_add_del_entry_reply_decode
api_func_table[VL_API_IPSEC_SAD_ADD_DEL_ENTRY] = ipsec_sad_add_del_entry_decode
api_func_table[VL_API_IPSEC_SAD_ADD_DEL_ENTRY_REPLY] = ipsec_sad_add_del_entry_reply_decode
api_func_table[VL_API_IPSEC_SA_SET_KEY] = ipsec_sa_set_key_decode
api_func_table[VL_API_IPSEC_SA_SET_KEY_REPLY] = ipsec_sa_set_key_reply_decode
api_func_table[VL_API_IKEV2_PROFILE_ADD_DEL] = ikev2_profile_add_del_decode
api_func_table[VL_API_IKEV2_PROFILE_ADD_DEL_REPLY] = ikev2_profile_add_del_reply_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_AUTH] = ikev2_profile_set_auth_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_AUTH_REPLY] = ikev2_profile_set_auth_reply_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_ID] = ikev2_profile_set_id_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_ID_REPLY] = ikev2_profile_set_id_reply_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_TS] = ikev2_profile_set_ts_decode
api_func_table[VL_API_IKEV2_PROFILE_SET_TS_REPLY] = ikev2_profile_set_ts_reply_decode
api_func_table[VL_API_IKEV2_SET_LOCAL_KEY] = ikev2_set_local_key_decode
api_func_table[VL_API_IKEV2_SET_LOCAL_KEY_REPLY] = ikev2_set_local_key_reply_decode
api_func_table[VL_API_DHCP_COMPL_EVENT] = dhcp_compl_event_decode
api_func_table[VL_API_MAP_ADD_DOMAIN] = map_add_domain_decode
api_func_table[VL_API_MAP_ADD_DOMAIN_REPLY] = map_add_domain_reply_decode
api_func_table[VL_API_MAP_DEL_DOMAIN] = map_del_domain_decode
api_func_table[VL_API_MAP_DEL_DOMAIN_REPLY] = map_del_domain_reply_decode
api_func_table[VL_API_MAP_ADD_DEL_RULE] = map_add_del_rule_decode
api_func_table[VL_API_MAP_ADD_DEL_RULE_REPLY] = map_add_del_rule_reply_decode
api_func_table[VL_API_MAP_DOMAIN_DUMP] = map_domain_dump_decode
api_func_table[VL_API_MAP_DOMAIN_DETAILS] = map_domain_details_decode
api_func_table[VL_API_MAP_RULE_DUMP] = map_rule_dump_decode
api_func_table[VL_API_MAP_RULE_DETAILS] = map_rule_details_decode
api_func_table[VL_API_MAP_SUMMARY_STATS] = map_summary_stats_decode
api_func_table[VL_API_MAP_SUMMARY_STATS_REPLY] = map_summary_stats_reply_decode
api_func_table[VL_API_COP_INTERFACE_ENABLE_DISABLE] = cop_interface_enable_disable_decode
api_func_table[VL_API_COP_INTERFACE_ENABLE_DISABLE_REPLY] = cop_interface_enable_disable_reply_decode
api_func_table[VL_API_COP_WHITELIST_ENABLE_DISABLE] = cop_whitelist_enable_disable_decode
api_func_table[VL_API_COP_WHITELIST_ENABLE_DISABLE_REPLY] = cop_whitelist_enable_disable_reply_decode
api_func_table[VL_API_GET_NODE_GRAPH] = get_node_graph_decode
api_func_table[VL_API_GET_NODE_GRAPH_REPLY] = get_node_graph_reply_decode
api_func_table[VL_API_SW_INTERFACE_CLEAR_STATS] = sw_interface_clear_stats_decode
api_func_table[VL_API_SW_INTERFACE_CLEAR_STATS_REPLY] = sw_interface_clear_stats_reply_decode
api_func_table[VL_API_TRACE_PROFILE_ADD] = trace_profile_add_decode
api_func_table[VL_API_TRACE_PROFILE_ADD_REPLY] = trace_profile_add_reply_decode
api_func_table[VL_API_TRACE_PROFILE_APPLY] = trace_profile_apply_decode
api_func_table[VL_API_TRACE_PROFILE_APPLY_REPLY] = trace_profile_apply_reply_decode
api_func_table[VL_API_TRACE_PROFILE_DEL] = trace_profile_del_decode
api_func_table[VL_API_TRACE_PROFILE_DEL_REPLY] = trace_profile_del_reply_decode
api_func_table[VL_API_AF_PACKET_CREATE] = af_packet_create_decode
api_func_table[VL_API_AF_PACKET_CREATE_REPLY] = af_packet_create_reply_decode
api_func_table[VL_API_AF_PACKET_DELETE] = af_packet_delete_decode
api_func_table[VL_API_AF_PACKET_DELETE_REPLY] = af_packet_delete_reply_decode
api_func_table[VL_API_POLICER_ADD_DEL] = policer_add_del_decode
api_func_table[VL_API_POLICER_ADD_DEL_REPLY] = policer_add_del_reply_decode
