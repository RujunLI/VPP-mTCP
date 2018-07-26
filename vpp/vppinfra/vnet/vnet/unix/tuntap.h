/* 
 *------------------------------------------------------------------
 * tuntap.h - kernel stack (reverse) punt/inject path
 *
 * Copyright (c) 2009 Cisco and/or its affiliates.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *------------------------------------------------------------------
 */

/*
 * Call from some VLIB_INIT_FUNCTION to set the Linux kernel
 * inject node name.
 */
#include <sys/uio.h>
#include <sys/types.h>
#include <vlib/vlib.h>

//extern volatile int flag1; 
//extern volatile int flag2;
//extern volatile int flag3;
//extern uword i_rx;
//extern vlib_main_t * vm;

//volatile int flag1;
//volatile int flag2;
//volatile int flag3;
//uword i_rx;
//vlib_main_t * vm;


//extern tuntap_main_t * tm;

//tuntap_main_t * tm;
typedef struct {
  u32 sw_if_index;
  u8 is_v6;
  u8 addr[16];
} subif_address_t;

typedef struct {
  /* Vector of iovecs for readv/writev calls. */
  struct iovec * iovecs;

  /* Vector of VLIB rx buffers to use.  We allocate them in blocks
     of VLIB_FRAME_SIZE (256). */
  u32 * rx_buffers;

  /* File descriptors for /dev/net/tun and provisioning socket. */
  int dev_net_tun_fd, dev_tap_fd;

  /* Create a "tap" [ethernet] encaps device */
  int is_ether;

  /* 1 if a "normal" routed intfc, 0 if a punt/inject interface */

  int have_normal_interface;

  /* tap device destination MAC address. Required, or Linux drops pkts */
  u8 ether_dst_mac[6];

  /* Interface MTU in bytes and # of default sized buffers. */
  u32 mtu_bytes, mtu_buffers;

  /* Linux interface name for tun device. */
  char * tun_name;

  /* Pool of subinterface addresses */
  subif_address_t *subifs;

  /* Hash for subif addresses */
  mhash_t subif_mhash;

  u32 unix_file_index;

  /* For the "normal" interface, if configured */
  u32 hw_if_index, sw_if_index;

} tuntap_main_t;

void register_tuntap_inject_node_name (char *name);

int vnet_tap_connect (vlib_main_t * vm, u8 * intfc_name,
                      u8 *hwaddr_arg, u32 * sw_if_indexp);
int vnet_tap_connect_renumber (vlib_main_t * vm, u8 * intfc_name,
                      u8 *hwaddr_arg, u32 * sw_if_indexp,
                      u8 renumber, u32 custom_dev_instance);

int vnet_tap_delete(vlib_main_t *vm, u32 sw_if_index);

int vnet_tap_modify (vlib_main_t * vm, u32 orig_sw_if_index,
                     u8 * intfc_name, u8 *hwaddr_arg,
                     u32 * sw_if_indexp,
                     u8 renumber, u32 custom_dev_instance);
