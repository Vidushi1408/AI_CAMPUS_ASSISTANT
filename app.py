import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="AI Smart Campus Navigation", page_icon="🧭", layout="wide")

st.title("🧭 AI Smart Campus Navigation System")
st.markdown("Navigate the CHRIST Delhi NCR Campus Smartly 🚀")

# CREATE CAMPUS GRAPH
G = nx.Graph()

edges = [

("Main Gate","Block A",40),
("Main Gate","Block B",40),

("Block A","Cafeteria",10),
("Block A","Library",10),
("Block A","Medical House",12),
("Block A","Main Auditorium",15),
("Block A","Sports Area",20),

("Block B","CCD",10),
("Block B","Rooftop Cafe",12),
("Block B","Mini Auditorium",15),
("Block B","Dominos",18),

("Block A","Block B",25)

]

G.add_weighted_edges_from(edges)

locations = list(G.nodes)

# SIDEBAR CONTROLS
st.sidebar.header("📍 Navigation Controls")

start = st.sidebar.selectbox("Start Location", locations)
destination = st.sidebar.selectbox("Destination", locations)

speed = st.sidebar.slider("Walking Speed (m/min)", 40,100,70)

# GRAPH DRAW FUNCTION
def draw_graph(path=None):

    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(8,6))

    nx.draw(G, pos,
            with_labels=True,
            node_color="skyblue",
            node_size=2500,
            font_size=9,
            ax=ax)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,ax=ax)

    if path:
        edges = list(zip(path,path[1:]))
        nx.draw_networkx_edges(G,pos,
                               edgelist=edges,
                               width=5,
                               edge_color="red",
                               ax=ax)

    st.pyplot(fig)

# MAIN LAYOUT
col1, col2 = st.columns([1,2])

with col1:

    st.subheader("🚀 Smart Route Finder")

    if st.button("Find Best Route"):

        path = nx.shortest_path(G,start,destination,weight="weight")
        distance = nx.shortest_path_length(G,start,destination,weight="weight")

        time = round(distance/speed,2)

        st.success("Best Route Found!")

        st.write("### 📍 Route")
        st.write(" ➜ ".join(path))

        st.write("### 📏 Distance")
        st.write(distance,"meters")

        st.write("### ⏱ Estimated Walking Time")
        st.write(time,"minutes")

        draw_graph(path)

    st.divider()

    if st.button("🌳 Show Minimum Spanning Tree"):

        mst = nx.minimum_spanning_tree(G)

        st.write("Minimum Spanning Tree Connections:")

        st.write(list(mst.edges(data=True)))

        pos = nx.spring_layout(mst)

        fig, ax = plt.subplots(figsize=(6,5))

        nx.draw(mst,pos,
                with_labels=True,
                node_color="lightgreen",
                node_size=2500,
                ax=ax)

        labels = nx.get_edge_attributes(mst,'weight')
        nx.draw_networkx_edge_labels(mst,pos,edge_labels=labels,ax=ax)

        st.pyplot(fig)

with col2:

    st.subheader("🗺 Campus Map")

    draw_graph()

st.divider()

# AI SMART RECOMMENDATION

st.subheader("🤖 AI Smart Recommendation")

data = pd.DataFrame({
"location":["Cafeteria","Library","CCD","Rooftop Cafe","Sports Area"],
"crowd":[90,40,70,60,50]
})

least_crowded = data.loc[data["crowd"].idxmin()]

st.info(f"💡 AI Suggests visiting **{least_crowded['location']}** now because it has the lowest crowd level.")

st.write("### Crowd Data")
st.dataframe(data)