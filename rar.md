用法:     rar <command> -<switch 1> -<switch N> <archive> <files...>
               <@listfiles...> <path_to_extract\>

<Commands>
  a             添加文件到压缩文档
  c             添加压缩文档注释
  ch            更改压缩文档参数
  cw            写入压缩文档注释到文件
  d             从压缩文档删除文件
  e             提取文件不带压缩路径
  f             刷新压缩文档中的文件
  i[par]=<str>  在压缩文档里查找字符串
  k             锁定压缩文档
  l[t[a],b]     列出压缩文档内容 [technical[all], bare]
  m[f]          移动到压缩文档 [仅文件]
  p             打印文件到 stdout
  r             修复压缩文档
  rc            重新构建丢失的卷
  rn            重命名归档的文件
  rr[N]         添加数据恢复记录
  rv[N]         创建恢复卷
  s[name|-]     转换压缩文档到或从 SFX
  t             测试压缩文档的文件
  u             更新压缩文档中的文件
  v[t[a],b]     详细列出压缩文档的内容 [technical[all],bare]
  x             解压文件带完整路径

<Switches>
  -             停止参数扫描
  @[+]          禁用 [enable] 文件列表
  ac            压缩或解压后清除压缩文档属性
  ad[1,2]       备选目标路径
  ag[format]    使用当前日期生成压缩文档名称
  ai            忽略文件属性
  ao            添加文件带有压缩文档属性集
  ap<path>      设置压缩文档内部的路径
  as            同步压缩文档内容
  c-            禁用内容显示
  cfg-          禁用读取配置
  cl            转换名称为小写
  cu            转换名称为大写
  df            压缩后删除文件
  dh            打开共享的文件
  dr            删除文件到回收站
  ds            为固实压缩禁用名称排序
  dw            压缩后删除文件
  e[+]<attr>    设置文件排除和包含属性
  ed            不要添加空目录
  ep            从名称里排除路径
  ep1           从名称里排除根目录
  ep2           扩展路径为完整路径
  ep3           扩展路径为完整路径包括驱动器盘符
  ep4<path>     从名称中排除路径前缀
  f             刷新文件
  hp[password]  加密文件数据及文件头
  ht[b|c]       设置哈希类型 [BLAKE2,CRC32] 用于文件校验和
  id[c,d,n,p,q] 显示或禁用消息
  ieml[addr]    通过电邮发送压缩文档
  ierr          发送所有压缩文档到 stderr
  ilog[name]    记录错误日志到文件
  inul          禁用所有消息
  ioff[n]       完成一个操作后关闭电脑
  isnd[-]       控制通知声音
  iver          显示版本号
  k             锁定压缩文档
  kb            保留损坏的已解压文件
  log[f][=name] 将名称写入日志文件
  m<0..5>       设置压缩等级 (0-store...3-default...5-maximal)
  ma[4|5]       指定压缩格式的版本
  mc<par>       设置高级压缩参数
  md<n>[k,m,g]  词典大小单位为 KB, MB 或 GB
  me[par]       设置加密参数
  ms[ext;ext]   指定要存储的文件类型
  mt<threads>   设置线程数
  n<file>       额外管理器包含文件
  n@            从 stdin 读取额外的过滤器掩码
  n@<list>      从列表文件读取额外的过滤器掩码
  o[+|-]        设置覆盖模式
  oc            设置 NTFS 压缩属性
  oh            保存硬链接为链接而不是文件
  oi[0-4][:min] 将相同的文件保存为参考
  ol[a]         将符号链接处理为链接 [absolute paths]
  oni           允许潜在的不兼容名称
  op<path>      设置解压文件的输出路径
  or            自动重命名文件
  os            保存 NTFS 流
  ow            保存或恢复文件拥有者和组
  p[password]   设置密码
  qo[-|+]       添加快速打开信息 [none|force]
  r             递归子目录
  r-            禁用递归
  r0            递归子目录仅用于通配符名称
  ri<P>[:<S>]   设置优先级 (0-默认,1-最小.15-最大) 和休眠时间单位为 ms
  rr[N]         添加数据恢复记录
  rv[N]         创建恢复卷
  s[<N>,v[-],e] 创建固实压缩文档
  s-            禁用固实压缩文档
  sc<chr>[obj]  指定字符集
  sfx[name]     创建 SFX 压缩文档
  si[name]      从标准输入读取数据 (stdin)
  sl<size>      处理小于指定大小的文件
  sm<size>      处理大于指定大小的文件
  t             压缩后测试
  ta[mcao]<d>   处理那些在日期 <d> YYYYMMDDHHMMSS 之后修改过的文件
  tb[mcao]<d>   处理那些在日期 <d> YYYYMMDDHHMMSS 之前修改过的文件
  tk            保留原来的压缩时间
  tl            设置压缩时间为最近的文件
  tn[mcao]<t>   处理那些时间比 <t> 更新的文件
  to[mcao]<t>   处理那些时间比 <t> 更老的文件
  ts[m,c,a,p]   保存或恢复时间（修改日期，创建日期，访问日期，保留日期）
  u             更新文件
  v<size>[k,b]  创建卷大小为=<size>*1000 [*1024, *1]
  vd            创建卷之前删除磁盘内容
  ver[n]        文件版本控制
  vn            使用旧式的卷命名规则
  vp            每个卷之前暂停
  w<path>       指定工作目录
  x<file>       排除特定文件
  x@            读取文件名以便从 stdin 排除
  x@<list>      排除在特定列表文件里列出的文件
  y             对所有问题回答是
  z[file]       从文件读取压缩文档注释