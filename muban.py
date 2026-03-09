import os
import sys

# 尝试导入高级 YAML 库（为了完美保留你的注释和排版）
try:
    from ruamel.yaml import YAML
except ImportError:
    print("❌ 缺少必要的依赖库！")
    print("👉 请先在终端运行: pip install ruamel.yaml")
    sys.exit(1)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def update_node_config(file_path):
    print(f"\n🚀 正在载入配置模板: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.load(f)
        except Exception as e:
            print(f"❌ YAML 解析失败: {e}")
            return

    if 'proxies' not in config:
        print("❌ 配置中没有找到 proxies (节点定义)，请检查模板文件。")
        return

    print("\n📝 请输入新的 VPS 节点信息:")
    print("💡 提示：如果某一项不需要修改（想保留原样），直接按【回车键】跳过即可。\n")

    new_v4_ip = input("🌐 1. 新的 IPv4 地址 (例: 1.2.3.4): ").strip()
    new_v6_ip = input("🌐 2. 新的 IPv6 地址 (例: 2607:...): ").strip()
    new_uuid = input("🔑 3. 新的 UUID (vless/tuic 通用): ").strip()
    new_pub_key = input("🛡️  4. 新的 Reality Public-Key: ").strip()
    new_short_id = input("🛡️  5. 新的 Reality Short-ID: ").strip()
    new_sni = input("🎭 6. 新的伪装域名 SNI (例: amd.com): ").strip()
    new_tuic_pwd = input("🔒 7. 新的 TUIC 密码: ").strip()

    update_count = 0

    # 开始批量精准替换
    for proxy in config['proxies']:
        name = proxy.get('name', '')
        
        # 1. 替换 IP (根据节点名称区分 v4 还是 v6)
        if 'ipv4' in name and new_v4_ip:
            proxy['server'] = new_v4_ip
            update_count += 1
        elif 'ipv6' in name and new_v6_ip:
            # 自动为 IPv6 地址添加安全的配置格式
            proxy['server'] = new_v6_ip
            update_count += 1

        # 2. 替换通用认证信息
        if new_uuid and 'uuid' in proxy:
            proxy['uuid'] = new_uuid
            update_count += 1
            
        if new_tuic_pwd and 'password' in proxy:
            proxy['password'] = new_tuic_pwd
            update_count += 1

        # 3. 替换伪装域名 (VLESS 叫 servername，TUIC 叫 sni)
        if new_sni:
            if 'servername' in proxy:
                proxy['servername'] = new_sni
                update_count += 1
            if 'sni' in proxy:
                proxy['sni'] = new_sni
                update_count += 1
                
        # 4. 替换 Reality 特有参数
        if 'reality-opts' in proxy:
            if new_pub_key:
                proxy['reality-opts']['public-key'] = new_pub_key
                update_count += 1
            if new_short_id:
                proxy['reality-opts']['short-id'] = new_short_id
                update_count += 1

    if update_count > 0:
        # 保存为新文件，不覆盖原模板
        out_file = "new_" + os.path.basename(file_path)
        with open(out_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        print(f"\n🎉 太棒了！一共为你自动修改了 {update_count} 处参数。")
        print(f"✅ 新的配置文件已生成: 【 {out_file} 】")
        print("👉 你现在可以直接将它导入 Mihomo 使用了！")
    else:
        print("\nℹ️ 你没有输入任何新信息，文件未作修改。")

if __name__ == "__main__":
    # 默认读取你的模板文件名
    template_file = "muban.yaml" 
    
    # 也可以通过命令行参数传入文件名
    if len(sys.argv) > 1:
        template_file = sys.argv[1]

    if os.path.exists(template_file):
        update_node_config(template_file)
    else:
        print(f"❌ 找不到模板文件: {template_file}")
        print("👉 请确保脚本和 YAML 配置文件在同一个文件夹下。")