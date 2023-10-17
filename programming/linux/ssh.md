---
title: SSH (Secure SHell)
---

本文参考了[鳥哥](http://linux.vbird.org/vbird/)的《[文字介面連線伺服器：SSH 伺服器](http://linux.vbird.org/linux_server/0310telnetssh.php#ssh_server)》。
原文以 CentOS 6 为例讲解，本文根据 Ubuntu 16.04 LTS 的特点做了一些修改。
对于不同的 Linux 发行版，大多数命令是一致的，只在『软件包管理命令』等细节上略有区别。

# SSH 加密通信原理

『SSH (**S**ecure **SH**ell)』是一种用于远程访问 Linux 主机的 CLI 软件。
它通过对通信数据加密与解密，使得本地主机可以『安全地 (securely)』访问远程主机上的『终端 (shell)』，从而使用其资源。

SSH 对数据的加密与解密主要是依靠成对的『公钥 (public key)』和『私钥 (private key)』来实现的：

- A 将自己的公钥提供给 B。
- B 利用 A 的公钥对数据进行加密，再将加密过的数据发送给 A。
- A 利用自己的私钥，对 B 发送过来的加密数据进行解密。

建立 SSH 连接主要包括以下几步：

1. 服务端开启 SSH 服务，检查 `/etc/ssh/ssh_host_key` 等文件是否存在。如果不存在，则创建这些文件。
2. 客户端发送连接请求。
3. 服务端接到请求后，将自己的公钥（明文）发送给客户端。
4. 客户端将收到的服务端公钥与 `~/.ssh/known_hosts` 中的记录进行对比：
   - 如果是首次连接，则新建一条记录。
   - 否则检查是否与已有的记录一致：
     - 如果一致，则继续连接。
     - 否则发出警告（认为服务端被别人伪装了）并退出。
5. 客户端随机生成自己的公钥和私钥，并将公钥（明文）传送给服务端。
6. 当服务端和客户端分别拥有自己的公私钥和对方的公钥后，便建立了 SSH 连接，可以开始互相传送数据。

# 在服务端开启 SSH 服务

```shell
# 检查 SSH 服务的状态：
systemctl status ssh
# 如果需要, 安装 SSH 服务端软件：
sudo apt install openssh-server
# 开启 SSH 服务：
sudo systemctl start ssh
sudo systemctl enable ssh
# 再次检查 SSH 服务的状态：
systemctl status ssh
```

应当返回如下内容（其中 `active (running)` 为绿色）：

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-06-05 12:12:06 CST; 22h ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 841 (sshd)
      Tasks: 1 (limit: 19009)
     Memory: 6.2M
     CGroup: /system.slice/ssh.service
             └─841 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Warning: some journal files were not opened due to insufficient permissions.

```

# 从客户端登入远程主机

## 从 Linux 主机访问远程 Linux 主机

```shell
# 如果需要，安装 SSH 客户端软件：
sudo apt install openssh-server
```
登入远程主机上的指定用户：
```shell
ssh user@address
# 按提示输入正确的密码后，即可登入远程主机。
```
或者，登入远程主机后，在远程主机上运行某程序：
```shell
# 等程序执行完成后，才切换回本地终端：
ssh user@address do_something
# 不等程序执行完，立即切换回本地终端：
ssh -f user@address do_something
```
输入 `exit` 则结束本次 SSH 连接，但一般不会关闭远程主机。若要关闭远程主机，则需输入远程用户密码：

```shell
ssh user@address sudo -S poweroff
```

## 从 Windows 主机访问远程 Linux 主机

首先需要在 Windows 主机上安装 SSH 客户端软件，例如 [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/)。
启动后，在地址栏输入远程 Linux 主机的『IP 地址』和『端口号（默认为 `22`）』，然后会弹出一个虚拟终端，在以下提示信息后面输入用户名，并按提示输入密码，即可建立 SSH 连接：

``` shell
login as:
```

## 修改远程 Linux 主机上当前用户的密码

建立远程连接后，在终端中输入以下命令：

```shell
passwd
```

然后根据提示输入原密码和新密码，这样在下次连接时就需要使用新密码了。

# 传输文件

## Secure File Transfer Program (SFTP)

与 `ssh` 命令类似，登入远程主机上的指定用户：

```shell
sftp user@address
# 按提示输入正确的密码后，即可登入远程主机。
# 终端提示符变为：
sftp> 
```

在 `sftp>` 后，可以输入一般的 shell 命令：

```shell
sftp>  pwd  # 在远程主机上执行
sftp> lpwd  # 在本地主机上执行
```

传输文件需用以下命令：

```bash
# 上传到指定远程目录：
sftp> put local_file remote_dir
# 上传到当前远程目录：
sftp> put local_file
# 下载到指定本地目录：
sftp> get remote_file local_dir
# 上传到当前本地目录：
sftp> get local_file
```

## Secure Copy Program (SCP)

```shell
# 上传：
scp    local_file user@address:dir
scp -r local_dir  user@address:dir
# 下载：
scp    user@address:file local_dir
scp -r user@address:dir  local_dir
# 指定端口：
scp -r -P port user@address:dir local_dir
```

# 免密访问

默认情况下，每次建立 SSH 连接都需要输入远程主机上指定用户的密码。
当需要频繁建立连接时，我们希望免去这一步骤。
这一需求可以通过『将客户端公钥写入服务端的 `~/.ssh/authorized_keys` 文件中』来实现。

## 客户端
首先，在客户端制作密钥：

```shell
# 切换到 ~/.ssh 目录：
cd ~/.ssh
# 生成 SSH 密钥：
ssh-keygen  # 根据提示
    # 先输入文件名（可按一次 [Enter] 以接受默认设置）
    # 再输入通行码（可按两次 [Enter] 以接受默认设置）
# 将公钥文件 id_rsa.pub 传送给服务端指定用户：
scp id_rsa.pub user@address:~  # 需要输入服务端密码
```

## 服务端

然后，在服务端添加授权信息：

```shell
# 切换到 ~ 目录
cd ~
# 检查 ~/.ssh 是否存在
ls .ssh
# 如果不存在，建立该目录，并设置权限
mkdir .ssh
chmod 700 .ssh
# 将客户端公钥添加进 authorized_keys
cat id_rsa.pub >> .ssh/authorized_keys
rm id_rsa.pub
# 更改 authorized_keys 的访问权限
chmod 644 .ssh/authorized_keys 
```

作为特例，如果希望能够通过 SSH 免密访问本地主机上的当前用户，只需在本地主机上开启 SSH 服务，并将当前用户的公钥写入自己的 `~/.ssh/authorized_keys` 文件。

## 测试

至此，应当可以从客户端通过 `ssh` 命令免密登入远程主机上的该用户，或者通过 `scp` 命令免密上传或下载数据。

⚠️ 若不成功，则需要在每次启动客户端 shell 时开启『认证代理 (authentication agent)』：

```shell
eval `ssh-agent`       # 启动认证代理
ssh-add ~/.ssh/id_rsa  # 加入私钥
ssh-add -l             # 列出已加入的私钥
```

上述命令可置于 `~/.bashrc` 或 `~/.zshrc` 中，以便每次启动 shell 时自动加载。

## [Remote Development using SSH](https://code.visualstudio.com/docs/remote/ssh)

执行完以上步骤后，在本地 `~/.ssh/config` 文件中添加以下内容，即可免密连接到远程主机上的指定用户：

```
Host <connection-name>
  HostName <remote-address>
  Port 22
  User <remote-user-name>
  IdentityFile ~/.ssh/<private-key-name>
```

# 非默认端口

在服务器的 `/etc/ssh/sshd_config` 文件中加入以下两行：

```shell
Port 22    # 默认端口
Port 1024  # 新开端口
```

并重启 SSH 服务：

```shell
sudo service sshd restart
```

在客户端选择目标端口：

```shell
ssh username@hostname_or_ipaddress  # 通过默认端口连接
ssh -p 1024 username@hostname_or_ipaddress  # 通过特定端口连接
```

# 在远程主机运行任务

使用场景：借助 SSH 在远程主机启动某个（耗时较长的）任务后，允许当前 SSH 连接挂起或断开。

```shell
# nohup := no hang up
nohup command [options]    # 在远程主机的前台运行任务
nohup command [options] &  # 在远程主机的后台运行任务
```

