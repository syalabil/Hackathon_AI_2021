from peekingduck.pipeline.nodes import output
from peekingduck.runner import Runner
from peekingduck.pipeline.nodes.input import recorded
from peekingduck.pipeline.nodes.model import yolo
from peekingduck.pipeline.nodes.draw import bbox , legend
from peekingduck.pipeline.nodes.dabble import bbox_count
from peekingduck.pipeline.nodes.output import media_writer, csv_writer

def api(url):
    input_dir = url
    stats_to_track = ['bbox_labels','count']
    detect_ids = [46,47,49]
    # Initialise the nodes
    input_node = recorded.Node(input_dir=input_dir)
    yolo_node = yolo.Node(detect_ids = detect_ids)
    legend_node = legend.Node()
    draw_node = bbox.Node()
    # Run it in the runner
    runner = Runner(nodes=[input_node, yolo_node,legend_node,draw_node])
    runner.run()

    #Inspect the data
    product = runner.pipeline.data['bbox_labels']

    return product
 
    




