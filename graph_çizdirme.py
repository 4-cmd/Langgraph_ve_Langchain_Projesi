def graph_cizdirme(png_data):
    try:
        with open("graph.png", "wb") as f:
            f.write(png_data)
            print("Graph has been drawn and saved as graph.png")
    except Exception as e:
        print(f"An error occurred while drawing the graph: {e}")