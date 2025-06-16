import numpy as np
import matplotlib.pyplot as plt
import json

def plot_ring_analysis(data_file):
    # 读取JSON数据
    print("正在读取数据...")
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # 创建图表
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建2x2的子图布局
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    
    # 1. 绘制传输谱 (Flux)
    wavelengths = np.linspace(1.5, 1.6, len(data['flux']['2,1']))  # 假设波长范围1.5-1.6μm
    ax1.plot(wavelengths, data['flux']['2,1'], 'b-', label='Through Port', linewidth=2)
    ax1.plot(wavelengths, data['flux']['3,1'], 'r-', label='Drop Port', linewidth=2)
    ax1.set_xlabel('波长 (μm)', fontsize=14)
    ax1.set_ylabel('传输率', fontsize=14)
    ax1.set_title('传输谱', fontsize=16)
    ax1.grid(True)
    ax1.legend(fontsize=12)

    # 2. 绘制S参数幅度
    s_params = data['S']['o2@0,o1@0']
    s_mag = [np.sqrt(p['re']**2 + p['im']**2) for p in s_params]
    ax2.plot(wavelengths, s_mag, 'g-', linewidth=2)
    ax2.set_xlabel('波长 (μm)', fontsize=14)
    ax2.set_ylabel('|S21|', fontsize=14)
    ax2.set_title('S参数幅度', fontsize=16)
    ax2.grid(True)

    # 3. 绘制S参数相位
    s_phase = [np.arctan2(p['im'], p['re']) * 180 / np.pi for p in s_params]
    ax3.plot(wavelengths, s_phase, 'r-', linewidth=2)
    ax3.set_xlabel('波长 (μm)', fontsize=14)
    ax3.set_ylabel('相位 (度)', fontsize=14)
    ax3.set_title('S参数相位', fontsize=16)
    ax3.grid(True)

    # 4. 绘制dB标度的传输特性
    ax4.plot(wavelengths, data['dB']['o2@0,o1@0'], 'b-', label='Through Port', linewidth=2)
    ax4.plot(wavelengths, data['dB']['o3@0,o1@0'], 'r-', label='Drop Port', linewidth=2)
    ax4.set_xlabel('波长 (μm)', fontsize=14)
    ax4.set_ylabel('传输率 (dB)', fontsize=14)
    ax4.set_title('传输特性(dB)', fontsize=16)
    ax4.grid(True)
    ax4.legend(fontsize=12)

    plt.tight_layout()
    
    # 保存图片
    output_file = 'ring_resonator_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"分析结果已保存为: {output_file}")
    plt.close()

if __name__ == '__main__':
    # 使用solution.json作为数据源
    data_file = 'solution.json'
    print(f"正在处理文件: {data_file}")
    
    # 绘制分析图
    plot_ring_analysis(data_file) 