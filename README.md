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

## 使用

下载该仓库的压缩包并解压，打开`bin`文件夹，参考示例，创建修改配置文件`config.json`并保存后，双击`exe`文件运行即可。

这个脚本并没有什么黑进教务处系统直接选课的不干净手段。通过查看反编译的代码，我们可以发现，它只不过是模仿我们刷新选课页面、查看剩余名额、有名额就选课这个动作，只不过能够每时每刻都蹲在那里查看罢了。

关于配置文件，我们需要更改的只有`profileId`、`wanted_course_ids`和`cookies_raw`三个字段：

+ `profileId`
  + 进入选课页面，发现网址有 `...?electionProfile.id={numbers}` 字样，这个`{numbers}` 就是 `profileId`；
  + 记得加双引号。
+ `wanted_course_ids`
  + 点进想要选的课程的教学任务信息，发现网址有 `...lesson.id={numbers}`字样，这个`{numbers}` 就是一个`id`；
  + 将你想要选的课程的`id`都放到`wanted_course_ids`中；
  + 记得加双引号。
+ `cookies_raw`
  + 使用开发者工具获得；
  + 因为不同浏览器的操作方法不一，这里不一一讲述，请自行搜索尝试。

关于格式，请参考 `bin/config(Example).json` 文件；更详细的格式信息请自行搜索`json`文件相关知识。