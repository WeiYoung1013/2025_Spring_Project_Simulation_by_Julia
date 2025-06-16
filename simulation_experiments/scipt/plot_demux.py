import numpy as np
import matplotlib.pyplot as plt
import re
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'scipt', 'demux.txt')

# 读取数据文件
def parse_log(filename):
    # 初始化数据字典
    t_o2_o1 = {1.1: [], 1.15: [], 1.2: []}  # 第一个输出端口
    t_o3_o1 = {1.8: [], 1.85: [], 1.9: []}  # 第二个输出端口
    
    print(f"正在解析文件...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.startswith('T'):
            try:
                # 使用正则表达式提取波长和值
                wavelength = float(re.search(r'λ=(\d+\.?\d*)', line).group(1))
                value = float(line.split(':')[-1].strip())
                
                if 'o2@0,o1@0' in line and wavelength in t_o2_o1:
                    t_o2_o1[wavelength].append(value)
                elif 'o3@0,o1@0' in line and wavelength in t_o3_o1:
                    t_o3_o1[wavelength].append(value)
            except Exception as e:
                print(f"解析错误: {e} at line: {line}")
                continue

    iterations = list(range(1, len(t_o2_o1[1.1]) + 1))
    
    print(f"数据点数量:")
    print(f"o2@0,o1@0 (Short Wavelength Port): {[len(t_o2_o1[w]) for w in [1.1, 1.15, 1.2]]}")
    print(f"o3@0,o1@0 (Long Wavelength Port): {[len(t_o3_o1[w]) for w in [1.8, 1.85, 1.9]]}")
    
    return iterations, t_o2_o1, t_o3_o1

# 绘图函数
def plot_training_results(iterations, t_o2_o1, t_o3_o1):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    colors2 = ['#96CEB4', '#FFEEAD', '#D4A5A5']
    markers = ['o', 's', '^']
    
    # 根据数据点数量决定是否采样
    sample_rate = 5 if len(iterations) > 20 else 1
    
    # 绘制短波长端口
    wavelengths1 = [1.1, 1.15, 1.2]
    for wavelength, color, marker in zip(wavelengths1, colors1, markers):
        if len(t_o2_o1[wavelength]) > 0:
            x_data = iterations[:len(t_o2_o1[wavelength])][::sample_rate]
            y_data = t_o2_o1[wavelength][::sample_rate]
            ax1.plot(x_data, y_data, 
                    color=color, marker=marker, linestyle='-', 
                    label=f'λ={wavelength}μm', markersize=25)
    
    ax1.set_xlabel('Iteration', fontsize=40)
    ax1.set_ylabel('Transmission', fontsize=40)
    if any(len(t_o2_o1[w]) > 0 for w in wavelengths1):
        ax1.legend(fontsize=25)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_ylim(0, 1.1)
    ax1.tick_params(axis='both', labelsize=40)
    
    # 绘制长波长端口
    wavelengths2 = [1.8, 1.85, 1.9]
    for wavelength, color, marker in zip(wavelengths2, colors2, markers):
        if len(t_o3_o1[wavelength]) > 0:
            x_data = iterations[:len(t_o3_o1[wavelength])][::sample_rate]
            y_data = t_o3_o1[wavelength][::sample_rate]
            ax2.plot(x_data, y_data,
                    color=color, marker=marker, linestyle='-',
                    label=f'λ={wavelength}μm', markersize=25)
    ax2.set_xlabel('Iteration', fontsize=40)
    if any(len(t_o3_o1[w]) > 0 for w in wavelengths2):
        ax2.legend(fontsize=25)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_ylim(0, 1.1)
    ax2.tick_params(axis='both', labelsize=40)
    
    plt.tight_layout()
    plt.savefig('demux_training_results.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print(f"正在读取日志文件: {log_file}")
    iterations, t_o2_o1, t_o3_o1 = parse_log(log_file)
    print("正在生成图表...")
    plot_training_results(iterations, t_o2_o1, t_o3_o1)
    print("图表已保存为 demux_training_results.png") 