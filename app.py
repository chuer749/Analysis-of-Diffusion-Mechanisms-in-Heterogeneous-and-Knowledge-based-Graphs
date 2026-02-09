import streamlit as st
import torch
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# --- 1. 页面配置 ---
st.set_page_config(layout="wide", page_title="零售异质图决策工作站")

@st.cache_data
def load_graph_data():
    """使用相对路径加载数据，增强可移植性"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "data", "hetero_graph_v2.pt")
    
    if not os.path.exists(path):
        st.error(f"❌ 未找到数据文件！请确保文件位于: {path}")
        return None
    return torch.load(path, weights_only=False)

def run_app():
    data = load_graph_data()
    if data is None: return
    
    maps = data['maps']
    store_map = maps['store']
    num_stores = len(store_map)

    # --- 2. 侧边栏：工业级检索 ---
    st.sidebar.title("🚀 海量数据检索")
    st.sidebar.write(f"当前图中包含店铺总数: **{num_stores:,}**")
    
    # 获取第一个 ID 作为默认值
    default_id = str(next(iter(store_map.keys())))
    search_id = st.sidebar.text_input("请输入店铺原始 ID", value=default_id)
    
    # 兼容性 ID 匹配逻辑
    current_store_idx = None
    if search_id in store_map:
        current_store_idx = store_map[search_id]
    elif search_id.isdigit() and int(search_id) in store_map:
        current_store_idx = store_map[int(search_id)]
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎚️ 可视化微调")
    discount_impact = st.sidebar.slider("折扣敏感度", 1.0, 15.0, 5.0)
    limit_nodes = st.sidebar.slider("展示关联商品上限", 10, 200, 50)
    
    show_cat = st.sidebar.checkbox("开启：品类关联层", value=True)
    show_weather = st.sidebar.checkbox("开启：天气环境层", value=True)

    if current_store_idx is None:
        st.sidebar.warning(f"⚠️ ID '{search_id}' 不在名录中。")
        return

    # --- 3. 构建可视化 ---
    st.title(f"🔗 店铺 {search_id} 的知识子图")
    
    net = Network(height="780px", width="100%", bgcolor="#111111", font_color="white")

    # 店铺节点
    v_rate = float(data['x_store'][current_store_idx, 0])
    atv_val = float(data['x_store'][current_store_idx, 1])
    net.add_node(f"S_{current_store_idx}", label=f"店铺 {search_id}", 
                 title=f"ATV: {atv_val:.2f}\nVIP率: {v_rate:.2%}", 
                 color="#FFA500", size=55)

    # 边提取
    p2s, p2c = data['edges']['p2s'], data['edges']['p2c']
    mask = (p2s[0] == current_store_idx)
    connected_p = p2s[1][mask]
    
    for i, p_idx_tensor in enumerate(connected_p):
        if i >= limit_nodes: break
        
        p_idx = p_idx_tensor.item()
        disc = float(data['x_prod'][p_idx, 0])
        qty = int(data['x_prod'][p_idx, 1])
        p_size = 20 + (qty * 0.4) + (disc * 10 * discount_impact)
        
        # 【此处已修改】节点命名改为：商品_xx
        p_node_id = f"P_{p_idx}"
        net.add_node(p_node_id, label=f"商品_{p_idx}", 
                     title=f"销量: {qty}\n折扣: {disc}", 
                     color="#00BFFF", size=p_size)
        net.add_edge(f"S_{current_store_idx}", p_node_id, color="#444444")

        if show_cat:
            cat_links = p2c[0][p2c[1] == p_idx]
            for c_idx in cat_links:
                c_idx = c_idx.item()
                # 兼容性处理品类映射
                c_name = list(maps['cat'].keys())[list(maps['cat'].values()).index(c_idx)]
                net.add_node(f"C_{c_name}", label=c_name, color="#32CD32", size=25, shape="diamond")
                net.add_edge(p_node_id, f"C_{c_name}", color="#32CD32", dashes=True)

    # 天气关联
    if show_weather:
        s2w = data['edges']['s2w']
        weather_links = s2w[1][s2w[0] == current_store_idx]
        for w_idx in weather_links:
            w_idx = w_idx.item()
            w_name = list(maps['weather'].keys())[list(maps['weather'].values()).index(w_idx)]
            net.add_node(f"W_{w_name}", label=w_name, color="#FF69B4", size=45, shape="star")
            net.add_edge(f"S_{current_store_idx}", f"W_{w_name}", color="#FF69B4", width=3)

    net.set_options('{"physics": {"enabled": true, "barnesHut": {"gravitationalConstant": -20000}}}')
    
    net.save_graph("large_scale_view.html")
    with open("large_scale_view.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=800)

if __name__ == "__main__":
    run_app()