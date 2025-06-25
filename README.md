# IMG-Convert
经常使用OpenWrt虚拟机，但是总是要手搓转换，感觉挺麻烦的，于是做了一个这个小程序。
使用转换程序将img文件转换为其他磁盘格式

-安装Python环境

-cmd中执行 pip install pyinstaller 安装pyinstaller

-下载源代码

-到代码根目录打开cmd，执行 pyinstaller --onefile --add-data "qemu;qemu" main.py 生成dist文件夹下的exe程序

-点击exe程序即可开始转换
