# VPP-mTCP
make mTCP a VPP TCP stack

As VPP is still lack of TCP stack, this repo is trying to integrate VPP with mTCP as both of the stacks are base on the DPDK. I avoid
mempry copy and trying to make least performance loss.

how to install 
1.editor the EXPORT.sh file, change the MTCP_PATH to your mTCP folder
2.source EXPORT.sh
3.cd build-root, ./bootstrap
4.cd ..
5.make build

if the error "mtcp.h: no such file or directory" is reported, please check the vlib/Makefile.in, add -I$(MTCP_INCLUDE_PATH) -I$(MTCP_PATH)/io_engine/include/ to AM_CFLAGS

