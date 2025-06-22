# SUFE 选课助手

$$
\textcolor{red}{
    本项目仅作为研究使用，请勿依赖本项目。\\
    选课相关事宜最终解释权归学校教务处所有。
}
$$

本人从学长那里得到了一份选课助手，一看是`exe`，Hex 编辑器再一看有`MEIPASS`，确定是 `pyinstaller` 打包的。

使用 [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) 提取出`pyc`文件，发现 python 版本是 3.11。

尝试使用 [uncompyle6](https://github.com/rocky/python-uncompyle6) 反编译，失败；尝试使用 [pylingual](https://pylingual.io/) 反编译，成功。
