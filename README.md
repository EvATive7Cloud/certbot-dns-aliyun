# certbot-dns-aliyun

## 原理

当我们使用 certbot 申请**通配符**证书时，需要手动添加 TXT 记录。每个 certbot 申请的证书有效期为 3 个月，虽然 certbot 提供了自动续期命令，但是当我们把自动续期命令配置为定时任务时，我们无法手动添加新的 TXT 记录用于 certbot 验证。

好在 certbot 提供了一个 hook，可以编写一个脚本。在续期的时候让脚本调用 DNS 服务商的 API 接口动态添加 TXT 记录，验证完成后再删除此记录。

## 安装

1. 安装 aliyun cli 工具  
   安装完成后需要配置[凭证信息](https://help.aliyun.com/document_detail/110341.html)

2. clone 本仓库并添加到环境变量PATH

1. `pip install -r requirements.txt`

3. 申请证书

   测试是否能正确申请：

   ```sh
   certbot certonly -d *.example.com --manual --preferred-challenges dns --manual-auth-hook "alidns.bat" --manual-cleanup-hook "alidns.bat clean" --dry-run
   ```

   正式申请时去掉 `--dry-run` 参数：

   ```sh
   certbot certonly -d *.example.com --manual --preferred-challenges dns --manual-auth-hook "alidns.bat" --manual-cleanup-hook "alidns.bat clean"
   ```

4. 证书续期

   ```sh
   certbot renew --manual --preferred-challenges dns --manual-auth-hook "alidns" --manual-cleanup-hook "alidns clean" --dry-run
   ```

   如果以上命令没有错误，把 `--dry-run` 参数去掉。
