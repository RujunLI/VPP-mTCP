# VPP-mTCP
make mTCP a VPP TCP stack

As VPP is still lack of TCP stack, this repo is trying to integrate VPP with mTCP as both of the stacks are base on the DPDK. 
I avoid memory copy and trying to make least performance loss.

how to install VPP

1.editor the EXPORT.sh file, change the MTCP_PATH to your mTCP folder

2.source EXPORT.sh

3.cd build-root, ./bootstrap

4.cd ..

5.make build


if the error "mtcp.h: no such file or directory" is reported, please check the vlib/Makefile.in, add -I$(MTCP_INCLUDE_PATH) -I$(MTCP_PATH)/io_engine/include/ to AM_CFLAGS

how to install mTCP:

1. first you should change VPP_LITE_PATH to your vpp_lite install path

2. source EXPOET.sh

3. cd dpdk-16.11/tools, ./dpdk-setup.sh

   Press [13] to compile the package
   
   Press [16] to install the driver
   
   Press [20] to setup 1024 2MB hugepages
   
   Press [22] to register the Ethernet ports
   
   Press [33] to quit the tool
   
4. set the NIC ip address (please make sure that which NIC is bound to DPDK, in    ubuntu system, the NIC will keep the same name as in kernel)

5. cd apps/example, input ./epserver -p your_web_directory -f epserver.conf -N core_number


if still exists problem, please refer to README to figure out how to install mtcp

this is based on VPP 16.04 and mTCP code
